from flask import Blueprint, render_template

# from projects.py_flask_core.config import Config
# upload_url = f"{Config.UPLOAD_URL}/upload"

# extract name
(_, name, *__) = __name__.split(".")
print(f"{name}:__name__", __name__)

foo_blueprint = Blueprint(name, __name__, template_folder='templates', static_folder='static')


@foo_blueprint.route('/')
def index():
    print("home:index")

    colors = ["Red", "Green", "Blue"]
    return render_template(f"{name}/index.html", colors=colors)

# @app.route('/greet/<string:name>')
# def greet(name: str):
#     return f"Hello {name}"


# @app.route('/home')
# def home():
#     return redirect(url_for('bar'))


# @app.route('/save-bar', methods=["POST"])
# def save_bar():
#     if request.method == 'POST':
#         name = request.form['name']
#         print(name)
#     return render_template('bar.html')
