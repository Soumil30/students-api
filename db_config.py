from flask_mysqldb import MySQL
import os


def configure_database(app):
    app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
    app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
    app.config['JSON_SORT_KEYS'] = False

    return MySQL(app)
