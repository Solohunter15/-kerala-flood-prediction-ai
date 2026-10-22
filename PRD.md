# Product Requirements Document (PRD)

## Project Title
**Kerala Flood Risk Prediction and Impact Analysis Using Hadoop Big Data Analytics**

---

## 1. Executive Summary & Vision
Kerala's unique topography—flanked by the Western Ghats and coastal Arabian Sea with 44 rivers—makes it recurrently vulnerable to devastating floods during monsoon seasons. The objective of this project is to build an enterprise-scale, Big Data-driven flood risk prediction and impact analysis platform. Rather than attempting to forecast meteorological dates, the system evaluates **vulnerability scores** and **quantifiable human/infrastructural impact** across all 14 districts of Kerala by processing over **1.1 million data records** using Apache Hadoop, HDFS, and MapReduce.

---

## 2. Target Personas
1. **Disaster Management Authorities (KSDMA, District Collectors, NDMA):**
   - Require explainable risk scores to deploy NDRF/SDRF teams and prioritize relief camps.
2. **General Public / Regional Citizens:**
   - Require district-level vulnerability outlooks, safety alerts, and emergency recommendations.
3. **Data Engineers / System Administrators:**
   - Ingest multi-source streams (historical, live weather APIs, social media crisis reports) and execute Hadoop MapReduce distributed jobs.

---

## 3. Scope & System Capabilities

### 3.1 Functional Requirements (FR)
- **FR-1: Multi-Source Data Ingestion:**
  - Historical flood & damage records (~500,000 rows from IMD, CWC, KSDMA).
  - Current real-time weather & river telemetry (~250,000 rows from weather APIs and sensors).
  - Social media and citizen crisis feeds (~350,000 rows from X/Twitter, emergency helplines).
- **FR-2: Unified Master Dataset Construction:**
  - Automated ETL transformation consolidating disparate data formats into a standardized 32-column schema.
- **FR-3: Hadoop Distributed Processing:**
  - Large-scale aggregation, cleaning, and metric compilation across HDFS using MapReduce and Hive queries.
- **FR-4: Transparent Risk Scoring Engine:**
  - Deterministic multi-factor weighted scoring algorithm producing a normalized score (0–100) and categorizing into Low, Moderate, High, or Critical.
- **FR-5: Impact Assessment Engine:**
  - Estimates affected population, infrastructure damage levels, and emergency relief tiers (Levels 1–4).
- **FR-6: Interactive Analytical Dashboard:**
  - Geospatial district rankings, historical flood event comparison, parameter simulation, and recommendation viewer.

### 3.2 Non-Functional Requirements (NFR)
- **Scalability:** Capable of horizontally scaling to multi-gigabyte/terabyte datasets in HDFS without performance degradation.
- **Explainability:** 100% auditable algorithmic calculations (avoiding black-box ML pitfalls during critical disaster response decision-making).
- **Fault Tolerance:** Distributed replication in HDFS (replication factor 3) ensuring continuous availability.
- **Performance:** Batch MapReduce queries finish within SLA benchmarks, with interactive dashboard queries served under 2 seconds.

---

## 4. Master Dataset Schema (32 Columns)
| Column Name | Data Type | Description |
|---|---|---|
| `Record_ID` | String (UUID) | Unique identifier for the observation |
| `Timestamp` | DateTime | Timestamp of observation or report |
| `District` | String | Kerala district name (e.g., Alappuzha, Idukki) |
| `Taluk` | String | Sub-district / Taluk level identifier |
| `Village` | String | Local administrative village |
| `Latitude` | Float | Geographic latitude coordinate |
| `Longitude` | Float | Geographic longitude coordinate |
| `Data_Source` | Enum | `Historical` \| `Current` \| `Social_Media` |
| `Rainfall_mm` | Float | Cumulative rainfall in millimeters (24h) |
| `River_Level_m` | Float | Water level relative to danger threshold (meters) |
| `Reservoir_Level` | Float | Reservoir storage capacity percentage (%) |
| `Temperature` | Float | Ambient temperature (°C) |
| `Humidity` | Float | Relative humidity (%) |
| `Wind_Speed` | Float | Wind speed (km/h) |
| `Flood_Occurred` | Boolean | Ground-truth flood occurrence indicator (0/1) |
| `Flood_Severity` | Enum | `None` \| `Low` \| `Moderate` \| `High` \| `Critical` |
| `Population` | Integer | Total resident population in the exposed zone |
| `Houses_Affected` | Integer | Historical / estimated inundated households |
| `Infrastructure_Damage`| Float | Damage severity index (0–100) |
| `Casualties` | Integer | Reported casualties or injuries |
| `Crop_Damage` | Float | Agricultural loss estimate in INR Lakhs |
| `Emergency_Reports` | Integer | Number of SOS distress calls received |
| `Social_Post_Count` | Integer | Number of distress social media posts |
| `Sentiment_Score` | Float | Crisis panic sentiment index (-1.0 to +1.0) |
| `Keyword_Score` | Float | Frequency of crisis keywords ("submerged", "stranded") |
| `Historical_Frequency`| Integer | Count of flood occurrences in last 10 years |
| `Elevation` | Float | Meters above mean sea level |
| `Distance_From_River`| Float | Distance to nearest river or waterbody (km) |
| `Drainage_Score` | Float | Terrain permeability & drainage capacity (0–100) |
| `Risk_Score` | Float | Computed composite risk score (0–100) |
| `Risk_Level` | Enum | `Low` \| `Moderate` \| `High` \| `Critical` |
| `Emergency_Priority` | Enum | `Level 1` (Immediate) to `Level 4` (Routine) |
