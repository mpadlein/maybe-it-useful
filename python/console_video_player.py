import os
import sys
import time
import multiprocessing
import cv2
from pydub import AudioSegment
from pydub.playback import play



DEFAULT_MAX_FRAMES = 800
DEFAULT_FRAME_WIDTH = 32
DEFAULT_FRAME_HEIGHT = 32


class ANSI:
    SET_TERMINAL_SIZE = '\033[8;{rows};{cols}t'
    INVISIBLE_CURSOR = '\033[?25l'
    SET_BACKGROUND_RGB = '\033[48;2;{};{};{}m  '
    SET_CURSOR_HOME = '\033[H'
    RESET = '\033[0m'



class AudioPlayer(multiprocessing.Process):
    def __init__(self, file) -> None:
        self.audio = AudioSegment.from_file(file)
        super(AudioPlayer, self).__init__()

    def run(self):
        play(self.audio)



class ConsoleVideoPlayer:
    fps: int
    video_capture: cv2.VideoCapture
    max_frames: int
    frame_width: int
    frame_height: int
    frames: list[str]


    def __init__(self, file, max_frames=DEFAULT_MAX_FRAMES, frame_width=DEFAULT_FRAME_WIDTH, frame_height=DEFAULT_FRAME_HEIGHT) -> None:
        self.video_capture = cv2.VideoCapture(file)
        self.audio_player = AudioPlayer(file)
        self.max_frames = max_frames
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = ['']*self.max_frames
        self._setup()


    def _setup(self):
        self._set_frame_rate()
        os.system('')


    def play(self):
        sys.stdout.write(ANSI.SET_TERMINAL_SIZE.format(rows=self.frame_height, cols=self.frame_width*2))
        sys.stdout.write(ANSI.INVISIBLE_CURSOR)
        
        self.audio_player.start()

        start = time.perf_counter()
        delay = 1/self.fps
        for i, frame in enumerate(self.frames):
            time.sleep(max(0,(start + delay*i) - time.perf_counter()))
            sys.stdout.write(ANSI.SET_CURSOR_HOME)
            sys.stdout.write(frame)

        self.audio_player.kill()


    def render(self):  
        max_frames = self.max_frames
        success,image = self.video_capture.read()

        for i in range(max_frames):
            success,image = self.video_capture.read()
            if not success: break

            print(f'Rendering frame: {i}/{max_frames}\r', end='')
            mat = cv2.resize(image, (self.frame_width, self.frame_height))            
            frame = self._mat_to_frame(mat)
            self.frames[i] = frame


    def _mat_to_frame(self, mat):
        frame = ''
        for row in mat:
            s = ''
            for r,g,b in row:
                s += ANSI.SET_BACKGROUND_RGB.format(r,g,b)
            frame += s + '\n'
        frame = frame.rstrip()
        return frame


    def _set_frame_rate(self):
        (major_ver, _, _) = (cv2.__version__).split('.')
        if int(major_ver)<3:
            self.fps = self.video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
        else :
            self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)



if __name__ == '__main__':
    """ 
    pip install pydub opencv-python 
    download ffmpeg and set env path: http://www.ffmpeg.org/download.html
    """

    VIDEO_FILE = 'rr.mp4'
    console_video_player = ConsoleVideoPlayer(VIDEO_FILE)

    console_video_player.render()

    input('Render complete. Press enter to continue...')
    console_video_player.play()

    input()
