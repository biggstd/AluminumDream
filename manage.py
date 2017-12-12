import unittest
import coverage
import click
import os

from flask_migrate import Migrate

from project.server import create_app, db
from project.server.models import User

from bokeh.command.util import build_single_handler_application
# from project.server.bokeh_apps import BokehDemo
# from bokeh.application.handlers.directory import DirectoryHandler

from bokeh.server.server import Server

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


@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""
    click.echo('Testing the application...')
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command()
def cov():
    """Runs the unit tests with coverage."""
    click.echo('Running unit tests with coverage...')
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


@app.cli.command()
def create_db():
    """Creates the db tables."""
    click.echo('Testing the database table creation...')
    db.create_all()


@app.cli.command()
def drop_db():
    """Drops the db tables."""
    click.echo('Dropping database tables...')
    db.drop_all()


@app.cli.command()
def create_admin():
    """Creates the admin user."""
    click.echo('Creating an admin user...')
    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()


@app.cli.command()
def create_data():
    """Creates sample data."""
    click.echo('NOT IMPLEMENTED Creating sample data...')
    pass


def start_bokeh_server():
    """
    Create and start a bokeh server with a series of
    applications.
    """
    app_path = os.path.abspath("project/server/bokeh_apps/bokehDemo/")
    print(app_path)
    server = Server(
        {'/bokehDemo': build_single_handler_application(app_path)},
        allow_websocket_origin=["localhost:5000"]
    )
    server.start()
    server.io_loop.start()


@app.cli.command()
def bokeh_server():
    """Creates sample data."""
    click.echo('Starting Bokeh Server...')
    start_bokeh_server()


if __name__ == '__main__':
    app.run(port=5000)
    start_bokeh_server()
