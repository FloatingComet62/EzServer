import callbackfunctions
import middleware

pages = [
    # [PATH, FILE_TYPE, HTML_FILE, CALLBACK_FUNCTION.__name__, MIDDLEWARE_FUNCTION.__name__]
    ["/", "html", ["src\pages\main.html"]],
    ["/home", "html", ["src\pages\home.html", "src\pages\\failed.html"], "", middleware.homePage.__name__],
    ["/exit", "html", ["src\pages\exit.html", "src\pages\\failed.html"], callbackfunctions.exitPage.__name__, middleware.exitPage.__name__],
]