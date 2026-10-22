import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Add root directory to sys.path for local and Vercel module resolution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from risk_engine import FloodRiskEngine

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
        self._set_headers(200, "application/json")
        self.wfile.write(json.dumps({
            "status": "online",
            "service": "Kerala Flood Risk Prediction API",
            "method": "POST to /api/predict",
            "supported_districts": FloodRiskEngine.get_supported_districts()
        }).encode("utf-8"))

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            params = json.loads(post_body.decode("utf-8")) if post_body else {}
            
            result = FloodRiskEngine.evaluate_comprehensive(
                district_name=params.get("district", "Wayanad"),
                rainfall_mm=params.get("rainfall_amount", 250.0),
                rainfall_duration_hrs=params.get("rainfall_duration", 24.0),
                soil_moisture_pct=params.get("soil_moisture", 80.0),
                selected_taluks=params.get("selected_taluks", None),
                historical_flood_freq=params.get("historical_freq", 5),
                current_water_level_m=params.get("current_water_level", 2.8),
                temperature_c=params.get("temperature", 28.0),
                wind_speed_kmh=params.get("wind_speed", 15.0),
                horizon=params.get("horizon", "1_hour")
            )
            
            response_json = json.dumps(result).encode("utf-8")
            self._set_headers(200, "application/json")
            self.wfile.write(response_json)
        except Exception as e:
            self._set_headers(400, "application/json")
            err_json = json.dumps({"status": "error", "message": str(e)}).encode("utf-8")
            self.wfile.write(err_json)
