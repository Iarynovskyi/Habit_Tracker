from flask import Flask
from routes import pages
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv('MONGO_URI'))
    app.db = client['Habits']

    app.register_blueprint(pages)

    return app
