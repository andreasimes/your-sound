# need to import flask 
# run pip install Flask

import os
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()