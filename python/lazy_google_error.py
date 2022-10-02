import sys
import traceback

_OPEN_URL_IN_BROWSER = False
def exc_handler(exc_type, exc, *args):
    print("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
    q = f'python {type(exc).__name__} {exc} site:stackoverflow.com'
    url = f'https://www.google.com/search?q={q}'
    url = url.replace(' ', '%20')

    if _OPEN_URL_IN_BROWSER:
        import webbrowser
        webbrowser.open(url)
    else:
        print(f'-->  {url}\n')

sys.excepthook = exc_handler
