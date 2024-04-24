from flask import Blueprint, render_template

# extract name
(_, name, *__) = __name__.split(".")
print(f"{name}:__name__", __name__)

home_blueprint = Blueprint(name, __name__, template_folder='templates')


@home_blueprint.route('/')
def index():
    print("home:index")
    return render_template(f"{name}/index.html")
