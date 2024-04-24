from flask import Flask

from modules.foo.views import foo_blueprint
from modules.home.views import home_blueprint

app = Flask(__name__)

app.register_blueprint(home_blueprint, url_prefix="/")
app.register_blueprint(foo_blueprint, url_prefix="/foo")

if __name__ == '__main__':
    app.run(debug=True)
