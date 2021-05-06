from app import app
from app import views
from flask import send_from_directory
import os
from config import Config


@app.route('/')
@app.route('/index')
def index():
    return 'Ok'

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.static_folder, filename)
