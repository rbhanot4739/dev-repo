from flask import render_template, Blueprint

core = Blueprint('core', __name__, template_folder='templates')


@core.route("/", methods=['GET', ])
def home():
    return render_template("core_home.html")


@core.route("/about", methods=['GET'])
def about():
    return render_template("core_about.html")
