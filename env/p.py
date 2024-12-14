from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Create an instance of the Flask application
app = Flask(__name__)

# Configuration of the database using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://amalnekh:amalsalma@localhost/gestion_Bibliothèque')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize SQLAlchemy
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return "Hello, World!"

# Run the application if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
