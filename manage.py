import unittest
import coverage
import click
import os
from threading import Thread

# from flask_script import Manager
from flask_migrate import Migrate#, MigrateCommand

from project.server import create_app, db
from project.server.models import User

# Import Bokeh application.
from bokeh.server.server import Server
from bokeh.application.handlers.directory import DirectoryHandler

# code coverage
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

app = create_app()
migrate = Migrate(app, db)
# manager = Manager(app)

# migrations
# manager.add_command('db', MigrateCommand)


def start_bokeh_server():
    """
    Starts a bokeh server so that they can be accessed.
    """
    demo_path = os.path.abspath('project/server/bokeh_apps/bokehDemo/')
    demo_app = DirectoryHandler(filename=demo_path)
    bokeh_server = Server(
        # The list of bokeh applications to run, and their
        # associated URLs.
        applications={
            '/bokeh_demo_application': demo_app,
        },
        allow_websocket_origin=["localhost:8000"]
    )

    # Start the server.
    bokeh_server.start()
    bokeh_server.io_loop.start()


# @manager.command
@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


# @manager.command
@app.cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


# @manager.command
@app.cli.command()
def create_db():
    """Creates the db tables."""
    db.create_all()


# @manager.command
@app.cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


# @manager.command
@app.cli.command()
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()


# @manager.command
@app.cli.command()
def create_data():
    """Creates sample data."""
    pass


@app.cli.command()
def deploy():
    """
    CLI function to deploy the entire server.
    """
    # Start the bokeh server.
    Thread(target=start_bokeh_server).start()

    # Start the flask server
    app.run(port=8000)
