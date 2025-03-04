import time
from flask import Flask
import os
import threading
from flask_jwt_extended import JWTManager
import requests
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key' 

@app.route("/")
def hello_world():    
    return "<p>Hello, World!</p>"

from controller.auth import *
from controller.tips import *
from controller.ai import *