from flask import render_template, Blueprint

from threading import Thread
from bokeh.embed import server_document
from bokeh.server.server import Server

# Import bokeh applicaitons.
from ..bokeh_apps import bokehDemo


main_blueprint = Blueprint('main', __name__,)


def bk_worker():
    server = Server(
        {'/bokeh-demo': bokehDemo},
        allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/bokeh-demo")
def bokeh_demo():
    Thread(target=bk_worker).start()
    script = server_document('http://localhost:5006/bokeh-demo')
    return render_template("main/bokeh_app.html", script=script)
