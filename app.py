import os
import subprocess
import sys
import threading
from datetime import datetime

from flask import Flask, abort, jsonify, render_template, request, send_file
import math

from config.config import RAW_DATA_PATH
from database.repository import (
    count_weather,
    get_all_cities,
    get_dashboard_summary,
    get_latest_weather,
    get_temperature_by_city,
    get_weather_history,
)

app = Flask(__name__)

HISTORY_PER_PAGE = 10

etl_status = {
    "running": False,
    "message": "Chưa chạy ETL",
    "completed": False,
    "success": None,
    "last_updated": None,
}
status_lock = threading.Lock()


def execute_etl():
    with status_lock:
        etl_status.update({
            "running": True,
            "message": "Đang chạy ETL...",
            "completed": False,
            "success": None,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    try:
        subprocess.run([sys.executable, "main.py"], check=True)
        with status_lock:
            etl_status.update({
                "running": False,
                "message": "ETL hoàn tất.",
                "completed": True,
                "success": True,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
    except Exception as e:
        with status_lock:
            etl_status.update({
                "running": False,
                "message": f"ETL thất bại: {e}",
                "completed": True,
                "success": False,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })


@app.route("/run-etl", methods=["GET", "POST"])
def run_etl():
    with status_lock:
        if not etl_status["running"]:
            threading.Thread(target=execute_etl, daemon=True).start()

        return jsonify(etl_status)


@app.route("/etl-status")
def etl_status_endpoint():
    with status_lock:
        return jsonify(etl_status)


def parse_history_filters(all_cities):
    city_filter = request.args.get("city", "").strip()
    date_filter = request.args.get("date", "").strip()

    if city_filter and city_filter not in all_cities:
        city_filter = ""

    if date_filter:
        try:
            datetime.strptime(date_filter, "%Y-%m-%d")
        except ValueError:
            date_filter = ""

    return city_filter, date_filter


def serialize_history_rows(rows):
    serialized = []
    for row in rows:
        observation_time = row["observation_time"]
        if hasattr(observation_time, "strftime"):
            observation_time = observation_time.strftime("%Y-%m-%d %H:%M:%S")
        serialized.append({
            **row,
            "observation_time": str(observation_time),
        })
    return serialized


def get_history_payload(page, city_filter="", date_filter=""):
    offset = (page - 1) * HISTORY_PER_PAGE
    history = get_weather_history(
        HISTORY_PER_PAGE,
        offset,
        city=city_filter or None,
        date=date_filter or None,
    )
    total = count_weather(
        city=city_filter or None,
        date=date_filter or None,
    )
    total_pages = math.ceil(total / HISTORY_PER_PAGE) if total else 1

    return {
        "history": serialize_history_rows(history),
        "page": page,
        "total_pages": total_pages,
        "total": total,
        "selected_city": city_filter,
        "selected_date": date_filter,
    }


@app.route("/api/history")
def history_api():
    all_cities = get_all_cities()
    page = request.args.get("page", 1, type=int)
    city_filter, date_filter = parse_history_filters(all_cities)
    return jsonify(get_history_payload(page, city_filter, date_filter))


@app.route("/download-csv")
def download_csv():
    if not os.path.exists(RAW_DATA_PATH):
        abort(404)

    return send_file(
        RAW_DATA_PATH,
        as_attachment=True,
        download_name="weather.csv",
        mimetype="text/csv",
    )


@app.route("/")
def index():
    summary_rows = get_dashboard_summary()
    summary = summary_rows[0] if summary_rows else {
        "total_city": 0,
        "avg_temp": 0,
        "avg_humidity": 0,
        "avg_wind_speed": 0,
        "last_updated": None,
    }

    weather = get_latest_weather()
    temp_chart = get_temperature_by_city()
    cities = [item["city"] for item in temp_chart]
    temps = [item["temperature"] for item in temp_chart]

    page = request.args.get("page", 1, type=int)
    all_cities = get_all_cities()
    city_filter, date_filter = parse_history_filters(all_cities)
    history_payload = get_history_payload(page, city_filter, date_filter)

    return render_template(
        "index.html",
        summary=summary,
        weather=weather,
        cities=cities,
        temps=temps,
        history=history_payload["history"],
        page=history_payload["page"],
        total_pages=history_payload["total_pages"],
        all_cities=all_cities,
        selected_city=city_filter,
        selected_date=date_filter,
        status=etl_status,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
