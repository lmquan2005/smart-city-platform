from flask import Flask, render_template
from database.repository import get_latest_weather

app = Flask(__name__)

@app.route("/")
def index():

    weather = get_latest_weather()

    return render_template(
        "index.html",
        weather=weather
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )