from flask import Flask, render_template, jsonify, request
import os
import trafic  # ton module IDS

app = Flask(__name__)

# --- Page principale ---
@app.route("/")
def index():
    logs = []
    if os.path.exists("alerts.log"):
        with open("alerts.log", "r") as f:
            logs = f.readlines()[-30:]  # dernières 30 alertes
    else:
        logs = ["Aucune alerte détectée pour le moment"]

    status = trafic.sniffer_status()
    return render_template("index.html", logs=logs, running=status["running"], iface=status["iface"])

# --- Start sniffer ---
@app.route("/start", methods=["POST"])
def start():
    iface = request.json.get("iface") if request.is_json else "lo"
    ok, msg = trafic.start_sniffer(interface=iface)
    return jsonify({"status": "ok" if ok else "error", "message": msg})

# --- Stop sniffer ---
@app.route("/stop", methods=["POST"])
def stop():
    ok, msg = trafic.stop_sniffer()
    return jsonify({"status": "ok" if ok else "error", "message": msg})

# --- Get logs (AJAX) ---
@app.route("/logs")
def get_logs():
    logs = []
    if os.path.exists("alerts.log"):
        with open("alerts.log", "r") as f:
            logs = f.readlines()[-50:]
    return jsonify({"logs": logs})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
