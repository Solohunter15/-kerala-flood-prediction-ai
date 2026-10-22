# Project Memory & Knowledge Base

## 1. Project Overview & Context
- **Project Name:** Kerala Flood Risk Prediction and Impact Analysis Using Hadoop Big Data Analytics
- **Primary Domain:** Big Data Engineering & Disaster Vulnerability Intelligence
- **Scale:** Over 1,100,000 records processed across 14 Kerala districts.
- **Key Frameworks:** Apache Hadoop (HDFS, MapReduce, Hive), Python / PySpark, Streamlit / Web UI.

---

## 2. Core Architectural & Design Decisions

### Decision 1: Why a Custom Weighted Algorithm Instead of Machine Learning?
- **Explainability & Disaster Governance:** In critical public safety decisions, government officials cannot rely on "black-box" neural networks or opaque tree ensembles. When ordering district-wide evacuations, officials must explicitly see *why* an alert was issued (e.g., 30% rainfall spike + 25% river cresting).
- **Zero Hallucination / Deterministic Trust:** Weighted multi-criteria evaluation complies with National Disaster Management Authority (NDMA) transparency guidelines.

### Decision 2: Why Hadoop Big Data Infrastructure?
- **Dataset Magnitude:** Historical records spanning 50+ years combined with continuous sensor readings and hundreds of thousands of social media streams exceed standard relational database memory limits.
- **Batch Aggregation via MapReduce:** Calculating rolling peak river heights, 10-year district flood frequencies, and territorial risk factors over 1.1M+ records runs concurrently across Hadoop worker nodes.
- **HDFS Fault Tolerance:** 3x block replication prevents data loss during infrastructure outages.

### Decision 3: Why a Single Unified Master Dataset (32 Columns)?
- Storing disparate siloed tables creates high join latencies in distributed systems.
- Normalizing Historical (500k), Current (250k), and Social (350k) into a single unified schema allows one single MapReduce pass to extract complete feature vectors.

---

## 3. Professor Viva Voce Cheat Sheet (Q&A)

### Q1: What exactly does your system predict?
> **Answer:** We predict the **flood vulnerability/risk score** (Low, Moderate, High, Critical) and the **quantifiable impact severity** (population affected, property damage index, emergency priority level) for each district, **not** the exact minute or day a flood will occur.

### Q2: Where exactly is Hadoop used in this project?
> **Answer:** 
> 1. **Storage (HDFS):** Stores multi-year historical logs, live telemetry, and social feeds across distributed DataNodes (`/data/kerala_flood/master/`).
> 2. **Processing (MapReduce):** A MapReduce job processes the 1.1M+ row unified dataset, grouping records by district to compute historical flood recurrence rates, average rainfall trends, and aggregated exposure features.
> 3. **Querying (Hive):** Allows running SQL-like ad-hoc queries for reporting district summaries.

### Q3: How do you justify 1.1 Million records for Kerala?
> **Answer:** 
> - **Historical Data (500,000 records):** Hourly and daily station records across 14 districts over decades from IMD, CWC, and KSDMA.
> - **Current Telemetry (250,000 records):** High-frequency sensor and weather API pings across multiple taluks, reservoirs, and automated weather stations (AWS).
> - **Social Media Reports (350,000 records):** Crowdsourced citizen SOS posts, tweets, and helpline inquiries during monsoon months.

### Q4: How is the Impact calculated?
> **Answer:** Impact is calculated by multiplying the computed **Risk Category** with **Social Exposure Factors** (population density per km², housing count, proximity to river banks, and critical infrastructure locations).

### Q5: What is the final deliverable?
> **Answer:** A centralized disaster management intelligence dashboard that ranks districts by risk, simulates "what-if" rainfall scenarios, and outputs emergency resource allocation priority rankings (Level 1 to Level 4).
