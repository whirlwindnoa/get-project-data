from flask import Flask, render_template, request
from getdata import fetchdata 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch", methods=["POST"])
def fetch():
    data = fetchdata(request.form["id"])

    if data is None:
        return render_template("index.html", status="ERROR")

    return render_template("index.html", status="OK", data=data)
 
if __name__ == "__main__":
    app.run()