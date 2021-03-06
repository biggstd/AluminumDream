from flask import render_template, Blueprint
from bokeh.embed import server_document

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/bokeh-demo/", methods=['GET'])
def bokeh_demo():
    script = server_document(url='http://localhost:5006/bokehDemo')
    print('Bokeh route called.')
    print(script)
    return render_template("main/bokeh_app.html", script=script)
