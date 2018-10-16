from . import home


@home.route("/")
def index():
    return "<h1 style='color:blue'>前台</h1>"
