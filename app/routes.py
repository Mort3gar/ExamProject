from app import app
from flask import render_template, request

@app.route('/', methods=["GET", "POST"])
def welcome_page():
    if request.method == 'GET':
        return render_template("welcome.html")