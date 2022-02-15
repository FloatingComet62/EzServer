import callbackfunctions
import middleware

pages = [
    # [PATH, FILE_TYPE, HTML_FILE, CALLBACK_FUNCTION.__name__, MIDDLEWARE_FUNCTION.__name__]
    ["/", "text/html", ["src\pages\main.html"]],
    ["/home", "text/html", ["src\pages\home.html", "src\pages\\failed.html"], "", middleware.homePage.__name__],
    ["/exit", "text/html", ["src\pages\exit.html", "src\pages\\failed.html"], callbackfunctions.exitPage.__name__, middleware.exitPage.__name__],
]