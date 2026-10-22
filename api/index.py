import os
import sys
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from risk_engine import FloodRiskEngine
from hadoop_mapreduce import HadoopMapReduceSimulator, SUMMARY_JSON_PATH

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.endswith("/districts") or parsed.path == "/api/districts":
            self._set_headers(200)
            districts = FloodRiskEngine.get_supported_districts()
            self.wfile.write(json.dumps({"districts": districts}).encode("utf-8"))
        elif parsed.path.endswith("/hadoop/summary") or parsed.path == "/api/hadoop/summary":
            self._set_headers(200)
            if os.path.exists(SUMMARY_JSON_PATH):
                with open(SUMMARY_JSON_PATH, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                sim = HadoopMapReduceSimulator()
                payload = sim.run_job()
                self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        if parsed.path.endswith("/predict") or parsed.path == "/api/predict":
            try:
                params = json.loads(post_body.decode("utf-8")) if post_body else {}
                result = FloodRiskEngine.evaluate_comprehensive(
                    district_name=params.get("district", "Wayanad"),
                    rainfall_mm=float(params.get("rainfall_amount", 250.0)),
                    rainfall_duration_hrs=float(params.get("rainfall_duration", 24.0)),
                    soil_moisture_pct=float(params.get("soil_moisture", 80.0)),
                    selected_taluks=params.get("selected_taluks", None),
                    historical_flood_freq=int(params.get("historical_freq", 5)),
                    current_water_level_m=float(params.get("current_water_level", 2.8)),
                    temperature_c=float(params.get("temperature", 28.0)),
                    wind_speed_kmh=float(params.get("wind_speed", 15.0)),
                    horizon=params.get("horizon", "1_hour")
                )
                self._set_headers(200)
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        elif parsed.path.endswith("/hadoop/run") or parsed.path == "/api/hadoop/run":
            sim = HadoopMapReduceSimulator()
            payload = sim.run_job()
            self._set_headers(200)
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))
