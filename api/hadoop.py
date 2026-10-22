import os
import sys
import json
from http.server import BaseHTTPRequestHandler

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from hadoop_mapreduce import HadoopMapReduceSimulator, SUMMARY_JSON_PATH

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        self._set_headers(200)
        if os.path.exists(SUMMARY_JSON_PATH):
            with open(SUMMARY_JSON_PATH, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            sim = HadoopMapReduceSimulator()
            payload = sim.run_job()
            self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_POST(self):
        sim = HadoopMapReduceSimulator()
        payload = sim.run_job()
        self._set_headers(200)
        self.wfile.write(json.dumps(payload).encode("utf-8"))
