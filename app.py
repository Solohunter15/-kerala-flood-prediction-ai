"""
Application: app.py
Purpose: Complete Kerala Flood AI Frontend & Backend System matching the exact
         5 reference images and 3-stage user flow:
         1. Page 1: Home Page
         2. Page 2: User Input Parameters (with interactive Kerala Vector Map)
         3. Page 3+: Continuous Scroll Results Page (Session 1: Overview, Session 2: Prediction, Session 3: Impact)
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse
from risk_engine import FloodRiskEngine
from hadoop_mapreduce import HadoopMapReduceSimulator, SUMMARY_JSON_PATH

PORT = 8080
HOST = "127.0.0.1"

# Read frontend HTML from template or serve directly
HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "index.html")

class FloodAIRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json", status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path in ["/", "/index.html", "/home", "/predict", "/results"]:
            self._set_headers("text/html; charset=utf-8")
            if os.path.exists(HTML_FILE_PATH):
                with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"<h1>Error: index.html not found</h1>")

        elif parsed.path.startswith("/assets/"):
            rel_path = parsed.path.lstrip("/").replace("/", os.sep)
            full_path = os.path.join(os.path.dirname(__file__), rel_path)
            if os.path.exists(full_path):
                ext = os.path.splitext(full_path)[1].lower()
                ct = (
                    "application/javascript" if ext == ".js"
                    else "image/png" if ext == ".png"
                    else "image/jpeg" if ext in [".jpg", ".jpeg"]
                    else "application/octet-stream"
                )
                with open(full_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Asset not found")
                
        elif parsed.path == "/api/districts":
            self._set_headers("application/json")
            districts = FloodRiskEngine.get_supported_districts()
            self.wfile.write(json.dumps({"districts": districts}).encode("utf-8"))
            
        elif parsed.path == "/api/hadoop/summary":
            if os.path.exists(SUMMARY_JSON_PATH):
                with open(SUMMARY_JSON_PATH, "r", encoding="utf-8") as f:
                    data = f.read()
                self._set_headers("application/json")
                self.wfile.write(data.encode("utf-8"))
            else:
                sim = HadoopMapReduceSimulator()
                payload = sim.run_job()
                self._set_headers("application/json")
                self.wfile.write(json.dumps(payload).encode("utf-8"))
                
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length)

        if parsed.path == "/api/predict":
            try:
                params = json.loads(post_body.decode("utf-8"))
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
                self._set_headers("application/json")
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self._set_headers("application/json", status=400)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif parsed.path == "/api/hadoop/run":
            sim = HadoopMapReduceSimulator()
            payload = sim.run_job()
            self._set_headers("application/json")
            self.wfile.write(json.dumps(payload).encode("utf-8"))

        else:
            self.send_error(404, "Endpoint not found")

def run_server():
    server_address = (HOST, PORT)
    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(server_address, FloodAIRequestHandler)
    print(f"[*] Kerala Flood AI Server online at http://{HOST}:{PORT}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        httpd.server_close()

# Top-level serverless entry point exports for Vercel and WSGI compat
handler = FloodAIRequestHandler
app = FloodAIRequestHandler
application = FloodAIRequestHandler

if __name__ == "__main__":
    run_server()
