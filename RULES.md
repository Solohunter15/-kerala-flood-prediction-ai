# System Rules & Algorithmic Specifications

## 1. Risk Factor Weight Allocations
The composite risk score is evaluated using an explainable multi-criteria weighting model:

$$\text{Composite Risk Score} = \sum (W_i \times S_i)$$

| Parameter ($i$) | Weight ($W_i$) | Source Input Features | Normalization Target (0–100) |
|---|---|---|---|
| **Rainfall Intensity** | **30% (0.30)** | 24h rainfall (mm) vs local threshold | $0\text{ mm} \to 0$, $\ge 400\text{ mm} \to 100$ |
| **River Water Level** | **25% (0.25)** | River water gauge vs Danger Mark (m) | Below Warning $\to 0-30$, Danger Mark $\to 80-100$ |
| **Historical Frequency** | **20% (0.20)** | Flood instances in past 10 years | 0 floods $\to 10$, $\ge 4$ floods $\to 100$ |
| **Geographic Vulnerability**| **10% (0.10)** | Low elevation + river proximity + poor drainage | Inverted elevation & drainage, proximity scale |
| **Population Exposure** | **10% (0.10)** | Population density per km² | Scaled relative to state peak density |
| **Emergency & Citizen Reports**| **5% (0.05)** | SOS reports + social media panic signals | Volume and keyword intensity mapped 0–100 |

$$\sum W_i = 0.30 + 0.25 + 0.20 + 0.10 + 0.10 + 0.05 = 1.00\ (100\%)$$

---

## 2. Risk Level Classification Rules
| Computed Score ($\text{Score}$) | Risk Category | Alert Color | Operational Status |
|---|---|---|---|
| $0.0 \le \text{Score} < 40.0$ | **Low** | 🟢 Green | Routine observation; normal drainage operations |
| $40.0 \le \text{Score} < 60.0$ | **Moderate** | 🟡 Yellow | Advisory warning; monitor river gauges & sluice gates |
| $60.0 \le \text{Score} < 75.0$ | **High** | 🟠 Orange | Evacuation preparedness; relief centers pre-staged |
| $75.0 \le \text{Score} \le 100.0$ | **Critical** | 🔴 Red | Immediate disaster response; NDRF deployment |

---

## 3. Impact Assessment Rules & Priority Matrix
Impact prediction combines the **Risk Category** with **Population Exposure Index**:

| Risk Category | Population Density | Expected Affected Pop. | Infrastructure Damage | Emergency Priority Tier |
|---|---|---|---|---|
| **Critical** | High | Very High (> 100k) | Severe / High | **Level 1 (Immediate - 0 to 2 hrs)** |
| **Critical** | Moderate / Low | High (25k–100k) | Moderate–High | **Level 1 (Immediate - 0 to 2 hrs)** |
| **High** | High | High (25k–100k) | High | **Level 2 (Urgent - 2 to 6 hrs)** |
| **High** | Moderate / Low | Moderate (10k–25k) | Moderate | **Level 2 (Urgent - 2 to 6 hrs)** |
| **Moderate** | Any | Low (< 10k) | Minor | **Level 3 (Guarded - 6 to 12 hrs)** |
| **Low** | Any | Minimal | Minimal | **Level 4 (Routine Monitoring)** |

---

## 4. Historical Trend Adjustment Rules
When analyzing multi-year trends in Hadoop:
- If a district has registered recurrent severe flood events in $\ge 3$ of the last 5 monsoon seasons (e.g., 2018, 2019, 2021, 2023):
  $$\text{Adjusted Future Risk} = \min(100, \text{Current Base Risk} + \Delta_{\text{trend}})$$
  where $\Delta_{\text{trend}} = +15$ points.
- If no severe flooding occurred in the last 7 years: $\Delta_{\text{trend}} = -5$ points.

---

## 5. Big Data & Data Cleaning Rules
1. **Deduplication:** Records with duplicate `(Timestamp, Latitude, Longitude, Data_Source)` must be filtered in the MapReduce Mapper.
2. **Missing Attribute Imputation:**
   - Social media records lack rainfall/river levels: enriched via nearest spatial-temporal IMD/CWC weather station.
   - Missing elevation: derived from geographic coordinates lookup.
3. **Outlier Filtering:**
   - Negative rainfall or water levels below physical bed level are rejected as sensor errors.
4. **Data Integrity:** Strict schema conformity before loading transformed datasets into HDFS master storage directory `/data/kerala_flood/master/`.
