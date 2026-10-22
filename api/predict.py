import os
import sys
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

# Add root directory to sys.path for local and Vercel module resolution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from risk_engine import FloodRiskEngine
try:
    from hadoop_mapreduce import HadoopMapReduceSimulator, SUMMARY_JSON_PATH
except Exception:
    HadoopMapReduceSimulator = None
    SUMMARY_JSON_PATH = os.path.join(ROOT_DIR, "kerala_district_hadoop_summary.json")

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".wasm": "application/wasm",
    ".csv": "text/csv; charset=utf-8"
}

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json", cache_control="no-cache"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        if cache_control:
            self.send_header("Cache-Control", cache_control)
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if not path:
            path = "/"

        # 1. API: Supported Districts
        if path in ["/api/districts", "/api/districts.py"]:
            self._set_headers(200, "application/json")
            districts = FloodRiskEngine.get_supported_districts()
            self.wfile.write(json.dumps({"districts": districts}).encode("utf-8"))
            return

        # 2. API: Hadoop MapReduce Summary
        if path.startswith("/api/hadoop"):
            self._set_headers(200, "application/json")
            if os.path.exists(SUMMARY_JSON_PATH):
                with open(SUMMARY_JSON_PATH, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            elif HadoopMapReduceSimulator:
                sim = HadoopMapReduceSimulator()
                payload = sim.run_job()
                self.wfile.write(json.dumps(payload).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"status": "summary_unavailable"}).encode("utf-8"))
            return

        # 3. API: Status/Health Info (only if explicitly hitting /api, /api/status, or GET /api/predict)
        if path in ["/api", "/api/status", "/api/predict", "/api/predict.py"]:
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "status": "online",
                "service": "Kerala Flood Risk Prediction AI API",
                "method": "POST to /api/predict",
                "supported_districts": FloodRiskEngine.get_supported_districts()
            }).encode("utf-8"))
            return

        # 4. Static Assets: /assets/*
        if path.startswith("/assets/"):
            rel_path = path.lstrip("/").replace("/", os.sep)
            file_path = os.path.join(ROOT_DIR, rel_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                ct = MIME_TYPES.get(ext, "application/octet-stream")
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "public, max-age=31536000, immutable")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "Asset not found")
                return

        # 5. Direct static files at root (e.g. kerala_district_hadoop_summary.json, favicon.ico) - excluding sensitive py code
        direct_candidate = os.path.join(ROOT_DIR, path.lstrip("/").replace("/", os.sep))
        ext = os.path.splitext(direct_candidate)[1].lower()
        if path != "/" and ext not in [".py", ".pyc", ".env"] and os.path.exists(direct_candidate) and os.path.isfile(direct_candidate):
            ct = MIME_TYPES.get(ext, "application/octet-stream")
            with open(direct_candidate, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
            return

        # 6. UI Routes: /, /index.html, /home, /predict, /results, or SPA fallback -> Serve index.html
        html_file = os.path.join(ROOT_DIR, "index.html")
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as f:
                html_content = f.read().encode("utf-8")
            self._set_headers(200, "text/html; charset=utf-8", cache_control="public, max-age=0, must-revalidate")
            self.wfile.write(html_content)
            return

        self.send_error(404, "Page not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        
        # Handle Hadoop Run
        if path == "/api/hadoop/run":
            if HadoopMapReduceSimulator:
                sim = HadoopMapReduceSimulator()
                payload = sim.run_job()
                self._set_headers(200, "application/json")
                self.wfile.write(json.dumps(payload).encode("utf-8"))
            else:
                self._set_headers(500, "application/json")
                self.wfile.write(json.dumps({"error": "Hadoop simulator module unavailable"}).encode("utf-8"))
            return

        # Handle Flood Prediction (Default for all POST requests including /api/predict)
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
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

            response_json = json.dumps(result).encode("utf-8")
            self._set_headers(200, "application/json")
            self.wfile.write(response_json)
        except Exception as e:
            self._set_headers(400, "application/json")
            err_json = json.dumps({"status": "error", "message": str(e)}).encode("utf-8")
            self.wfile.write(err_json)

# WSGI / Serverless aliases
app = handler
application = handler
