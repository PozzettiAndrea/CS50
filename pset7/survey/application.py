import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    message = "Please complete the form correctly"
    if request.form.get("first_name") == "" or request.form.get("last_name") == "" or request.form.get("language") == "" or request.form.get("mexperience") == "":
        return render_template("error.html", message=message)
    else:
        with open("survey.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow((request.form.get("first_name"), request.form.get("last_name"),
                             request.form.get("language"), request.form.get("mexperience")))

    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open('survey.csv', 'r') as file:
        read = csv.reader(file)
        soldiers = list(read)

    return render_template("sheet.html", soldiers=soldiers)
