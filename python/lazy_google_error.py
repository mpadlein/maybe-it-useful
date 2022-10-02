import sys
import traceback


_OPEN_URL_IN_BROWSER = False
def exc_handler(exc_type, exc, *args):
    print("".join(traceback.format_exception(exc_type, exc, exc.__traceback__)))
    q = f'python {exc_type.__name__}  {exc} site:stackoverflow.com'
    q = q.replace(' ', '+')
    url = f'https://www.google.com/search?q={q}'

    if _OPEN_URL_IN_BROWSER:
        import webbrowser
        webbrowser.open(url)
    else:
        print(f'-->  {url}\n')

sys.excepthook = exc_handler
