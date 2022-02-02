import callbackfunctions
import middleware

pages = [
    # [PATH, HTML_FILE, MIDDLEWARE_FUNCTION.__name__ CALLBACK_FUNCTION.__name__]
    ["/", ['src\pages\home.html', 'src\pages\failed.html'], "", middleware.homePage.__name__],
    ["/exit", ['src\pages\exit.html', 'src\pages\failed.html'], callbackfunctions.exitPage.__name__, middleware.exitPage.__name__],
]