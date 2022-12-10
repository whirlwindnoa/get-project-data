from flask import Flask, render_template, request
from getdata import fetchdata

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch", methods=["POST"])
async def fetch():
    data = await fetchdata(request.form["id"])

    return await render_template("index.html", status="OK", likes=data[0])
 
if __name__ == "__main__":
    app.run()