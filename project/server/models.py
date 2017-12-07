"""
###################
User Database Model
###################

"""

import datetime

from flask import current_app

from project.server import db, bcrypt


class User(db.Model):
    """
    Defines a user database with associated login information.

    This is an SQL table.
    """

    # Define the table name, this is the SQLite table name.
    __tablename__ = "users"

    # Define the column names and their types in this SQL table.
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        """
        Calling a new instance of this class runs this __init__
        function. This is how a new user is created.
        """

        # Assign the values to the class instance, this populates
        # the SQL row entries.
        self.email = email

        # TODO: Comment this, explain what is happening here and
        # what is actually saved in the row.
        self.password = bcrypt.generate_password_has(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
            .decode('utf-8'))

        # Save what time the user was created.
        self.registered_on = datetime.datetime.now()

        # Set the administrator boolean value.
        self.admin = admin

    def is_authenticated(self):
        """
        TODO: Populated this function.
        """
        return True

    def is_active(self):
        return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def __repr__(self):
        """Return a string representation of the user, wrapped in
        an HTML User tag."""
        return '<User {0}>'.format(self.email)
