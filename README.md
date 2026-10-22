# 🌊 Kerala Flood Risk Prediction & Big Data Analytics

An enterprise big data analytics and multi-factor hydrodynamic risk forecasting system engineered for Kerala district flood risk prediction, topographic vulnerability scoring, and disaster impact assessment across 100,000+ records.

---

## ⚡ Live Deployment on Vercel

This repository is optimized for one-click deployment on **[Vercel](https://vercel.com)**:
- **Frontend**: High-fidelity responsive dashboard (`index.html`, vanilla CSS, Three.js 3D terrain simulation, interactive SVG Kerala vector maps).
- **Backend**: Native Serverless Python functions (`api/predict.py`, `api/index.py`) powered by `risk_engine.py`.
- **Zero Heavy Dependencies**: Pure standard library execution with near-instant cold starts (<150ms).

---

## 🚀 Quick Start (Local)

### 1. Run Web Dashboard Locally
```bash
python local_server.py
```
Open **[http://127.0.0.1:8080/](http://127.0.0.1:8080/)** in your browser.

### 2. Generate 1 Lakh Unified Big Data Dataset
```bash
python generate_1lakh_dataset.py
```
- Creates `kerala_flood_1lakh_unified.csv` (~21.5 MB, 100,000 records).
- Adheres to the 32-column standardized master schema across historical flood data, real-time IoT sensors, and citizen SOS telemetry.

### 3. Run MapReduce Distributed Aggregation
```bash
python hadoop_mapreduce.py
```
- Executes MapReduce Mapper, Shuffle & Sort, and Reducer stages.
- Generates district summary tables: `kerala_district_hadoop_summary.json` and `kerala_district_hadoop_summary.csv`.

---

## 📁 Repository Structure

| File / Folder | Purpose |
|---|---|
| [`index.html`](index.html) | Complete interactive user interface & visualization dashboard |
| [`api/predict.py`](api/predict.py) | Vercel serverless function for flood risk prediction |
| [`api/index.py`](api/index.py) | Vercel serverless router for auxiliary endpoints |
| [`risk_engine.py`](risk_engine.py) | SCS-CN runoff modeling & 77-taluk vulnerability engine |
| [`generate_1lakh_dataset.py`](generate_1lakh_dataset.py) | 100k Big Data generator adhering to 32-attribute schema |
| [`hadoop_mapreduce.py`](hadoop_mapreduce.py) | Multi-stage MapReduce distributed simulation pipeline |
| [`app.py`](app.py) | Standalone local HTTP server for offline testing |
| [`vercel.json`](vercel.json) | Vercel deployment routes and serverless configuration |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System & HDFS/MapReduce data pipeline architecture |
| [`PRD.md`](PRD.md) | Product Requirements Document & Master 32-column schema |
| [`RULES.md`](RULES.md) | Multi-criteria weighted algorithm specification |
| [`UI_UX.md`](UI_UX.md) | Interface design, wireframes, and aesthetic standards |
| [`MEMORY.md`](MEMORY.md) | Technical decisions & Viva Voce Q&A Cheat Sheet |
