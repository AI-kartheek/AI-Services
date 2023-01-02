from flask import Blueprint, render_template, send_from_directory

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("main/home.html", title="home")

## url for downloading output csv files
@main.route("/download/<file_name>")
def download_file(file_name):
    return send_from_directory('static/download', file_name)