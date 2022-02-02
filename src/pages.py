import callbackfunctions
import middleware

pages = [
    # [PATH, HTML_FILE, CSS, CALLBACK_FUNCTION.__name__, MIDDLEWARE_FUNCTION.__name__]
    ["/", ["src\pages\main.html"], ["src\static\\main.css"]],
    ["/home", ["src\pages\home.html", "src\pages\\failed.html"], [], "", middleware.homePage.__name__],
    ["/exit", ["src\pages\exit.html", "src\pages\\failed.html"], [], callbackfunctions.exitPage.__name__, middleware.exitPage.__name__],
]