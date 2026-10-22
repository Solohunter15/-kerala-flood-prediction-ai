"""
Script: generate_1lakh_dataset.py
Purpose: Generates a realistic, unified 100,000 (1 Lakh) record Big Data dataset
         for Kerala Flood Risk Prediction and Impact Analysis adhering to the 32-column schema.
"""

import csv
import random
import uuid
from datetime import datetime, timedelta
import os
import sys

# Output path
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "kerala_flood_1lakh_unified.csv")

# 14 Districts of Kerala with geographic and demographic baseline profiles
DISTRICT_PROFILES = {
    "Alappuzha": {
        "taluks": ["Ambalappuzha", "Cherthala", "Kuttanad", "Karthikappally", "Chengannur", "Mavelikkara"],
        "lat_range": (9.3, 9.7), "lon_range": (76.3, 76.5),
        "elevation_range": (-2.0, 8.0), # Low-lying Kuttanad below sea level
        "distance_river_range": (0.1, 4.0),
        "drainage_base": 25.0, # Poor natural drainage
        "population_base": 2127789,
        "hist_freq_base": 8,
        "flood_prone_factor": 1.45
    },
    "Idukki": {
        "taluks": ["Devikulam", "Peerumade", "Thodupuzha", "Udumbanchola", "Idukki"],
        "lat_range": (9.6, 10.2), "lon_range": (76.8, 77.3),
        "elevation_range": (500.0, 1800.0), # Highland Western Ghats
        "distance_river_range": (0.2, 8.0),
        "drainage_base": 70.0,
        "population_base": 1108974,
        "hist_freq_base": 7,
        "flood_prone_factor": 1.35
    },
    "Ernakulam": {
        "taluks": ["Kanayannur", "Kochi", "Aluva", "Paravur", "Kunnathunad", "Muvattupuzha", "Kothamangalam"],
        "lat_range": (9.8, 10.3), "lon_range": (76.2, 76.7),
        "elevation_range": (1.0, 45.0),
        "distance_river_range": (0.2, 5.0),
        "drainage_base": 40.0,
        "population_base": 3427500,
        "hist_freq_base": 6,
        "flood_prone_factor": 1.30
    },
    "Pathanamthitta": {
        "taluks": ["Adoor", "Konni", "Kozhencherry", "Mallappally", "Ranni", "Thiruvalla"],
        "lat_range": (9.1, 9.5), "lon_range": (76.6, 77.1),
        "elevation_range": (10.0, 350.0),
        "distance_river_range": (0.1, 3.5),
        "drainage_base": 45.0,
        "population_base": 1197412,
        "hist_freq_base": 7,
        "flood_prone_factor": 1.38
    },
    "Kottayam": {
        "taluks": ["Changanassery", "Kanjirappally", "Kottayam", "Meenachil", "Vaikom"],
        "lat_range": (9.4, 9.8), "lon_range": (76.4, 76.8),
        "elevation_range": (2.0, 60.0),
        "distance_river_range": (0.2, 4.0),
        "drainage_base": 35.0,
        "population_base": 1974551,
        "hist_freq_base": 6,
        "flood_prone_factor": 1.28
    },
    "Thrissur": {
        "taluks": ["Chalakudy", "Chavakkad", "Kodungallur", "Mukundapuram", "Thalapilly", "Thrissur"],
        "lat_range": (10.2, 10.7), "lon_range": (76.0, 76.5),
        "elevation_range": (2.0, 90.0),
        "distance_river_range": (0.3, 6.0),
        "drainage_base": 50.0,
        "population_base": 3121200,
        "hist_freq_base": 5,
        "flood_prone_factor": 1.22
    },
    "Wayanad": {
        "taluks": ["Mananthavady", "Sultan Bathery", "Vythiri"],
        "lat_range": (11.5, 11.9), "lon_range": (75.9, 76.3),
        "elevation_range": (700.0, 1400.0),
        "distance_river_range": (0.2, 5.0),
        "drainage_base": 65.0,
        "population_base": 817420,
        "hist_freq_base": 7,
        "flood_prone_factor": 1.32
    },
    "Kozhikode": {
        "taluks": ["Kozhikode", "Koyilandy", "Thamarassery", "Vadakara"],
        "lat_range": (11.1, 11.6), "lon_range": (75.7, 76.1),
        "elevation_range": (1.0, 110.0),
        "distance_river_range": (0.3, 5.0),
        "drainage_base": 55.0,
        "population_base": 3086293,
        "hist_freq_base": 5,
        "flood_prone_factor": 1.15
    },
    "Malappuram": {
        "taluks": ["Ernad", "Nilambur", "Perinthalmanna", "Ponnani", "Tirur", "Tirurangadi", "Kondotty"],
        "lat_range": (10.8, 11.3), "lon_range": (75.8, 76.4),
        "elevation_range": (5.0, 200.0),
        "distance_river_range": (0.3, 6.0),
        "drainage_base": 55.0,
        "population_base": 4112920,
        "hist_freq_base": 5,
        "flood_prone_factor": 1.18
    },
    "Palakkad": {
        "taluks": ["Alathur", "Chittur", "Mannarkkad", "Ottappalam", "Palakkad", "Pattambi"],
        "lat_range": (10.6, 11.1), "lon_range": (76.3, 76.9),
        "elevation_range": (50.0, 250.0),
        "distance_river_range": (0.5, 8.0),
        "drainage_base": 60.0,
        "population_base": 2809934,
        "hist_freq_base": 4,
        "flood_prone_factor": 1.05
    },
    "Kollam": {
        "taluks": ["Kollam", "Karunagappally", "Kunnathur", "Kottarakkara", "Punalur", "Pathanapuram"],
        "lat_range": (8.8, 9.2), "lon_range": (76.5, 77.1),
        "elevation_range": (2.0, 150.0),
        "distance_river_range": (0.3, 7.0),
        "drainage_base": 55.0,
        "population_base": 2635375,
        "hist_freq_base": 4,
        "flood_prone_factor": 1.08
    },
    "Kannur": {
        "taluks": ["Kannur", "Taliparamba", "Thalassery", "Iritty", "Payyanur"],
        "lat_range": (11.7, 12.2), "lon_range": (75.3, 75.8),
        "elevation_range": (2.0, 120.0),
        "distance_river_range": (0.4, 7.0),
        "drainage_base": 60.0,
        "population_base": 2523003,
        "hist_freq_base": 4,
        "flood_prone_factor": 1.05
    },
    "Kasaragod": {
        "taluks": ["Hosdurg", "Kasaragod", "Manjeshwaram", "Vellarikundu"],
        "lat_range": (12.2, 12.8), "lon_range": (74.9, 75.4),
        "elevation_range": (3.0, 150.0),
        "distance_river_range": (0.5, 8.0),
        "drainage_base": 62.0,
        "population_base": 1307375,
        "hist_freq_base": 3,
        "flood_prone_factor": 0.95
    },
    "Thiruvananthapuram": {
        "taluks": ["Neyyattinkara", "Kattakkada", "Nedumangad", "Thiruvananthapuram", "Chirayinkeezhu", "Varkala"],
        "lat_range": (8.3, 8.8), "lon_range": (76.8, 77.2),
        "elevation_range": (3.0, 180.0),
        "distance_river_range": (0.4, 8.0),
        "drainage_base": 65.0,
        "population_base": 3301427,
        "hist_freq_base": 3,
        "flood_prone_factor": 0.92
    }
}

SOCIAL_KEYWORDS = ["submerged", "stranded", "water logging", "overflowing", "rescue needed", "dam opened", "roads blocked", "red alert"]

def calculate_exact_risk_score(rainfall_norm, river_norm, hist_norm, geo_norm, pop_norm, emergency_norm):
    """
    Computes exact risk score using the specified weighted formula:
    Rainfall: 30%, River Level: 25%, Historical: 20%, Geography: 10%, Population: 10%, Emergency: 5%
    """
    score = (
        (rainfall_norm * 0.30) +
        (river_norm * 0.25) +
        (hist_norm * 0.20) +
        (geo_norm * 0.10) +
        (pop_norm * 0.10) +
        (emergency_norm * 0.05)
    )
    return round(score, 2)

def classify_risk_level(score):
    if score >= 75.0:
        return "Critical"
    elif score >= 60.0:
        return "High"
    elif score >= 40.0:
        return "Moderate"
    else:
        return "Low"

def determine_emergency_priority(risk_level, population_exposure):
    if risk_level == "Critical":
        return "Level 1" # Immediate (0-2h)
    elif risk_level == "High":
        return "Level 2" # Urgent (2-6h)
    elif risk_level == "Moderate":
        return "Level 3" # Guarded (6-12h)
    else:
        return "Level 4" # Routine Monitoring

def generate_records(total_target=100000):
    print(f"[*] Starting dataset generation: {total_target} records...")
    
    # Target distribution across 3 sources
    # Historical: ~45,000, Current: ~25,000, Social Media: ~30,000
    n_historical = int(total_target * 0.45)
    n_current = int(total_target * 0.25)
    n_social = total_target - (n_historical + n_current)
    
    districts = list(DISTRICT_PROFILES.keys())
    
    # 32 columns schema
    fieldnames = [
        "Record_ID", "Timestamp", "District", "Taluk", "Village",
        "Latitude", "Longitude", "Data_Source", "Rainfall_mm", "River_Level_m",
        "Reservoir_Level", "Temperature", "Humidity", "Wind_Speed", "Flood_Occurred",
        "Flood_Severity", "Population", "Houses_Affected", "Infrastructure_Damage", "Casualties",
        "Crop_Damage", "Emergency_Reports", "Social_Post_Count", "Sentiment_Score", "Keyword_Score",
        "Historical_Frequency", "Elevation", "Distance_From_River", "Drainage_Score", "Risk_Score",
        "Risk_Level", "Emergency_Priority"
    ]
    
    start_date_hist = datetime(2018, 5, 1)
    end_date_hist = datetime(2025, 12, 31)
    
    current_date = datetime(2026, 10, 1)
    
    rows = []
    
    # Generator loop helper
    def create_single_record(src_type, i):
        dist_name = random.choice(districts)
        p = DISTRICT_PROFILES[dist_name]
        taluk = random.choice(p["taluks"])
        village = f"{taluk}_Ward_{random.randint(1, 20)}"
        
        lat = round(random.uniform(*p["lat_range"]), 4)
        lon = round(random.uniform(*p["lon_range"]), 4)
        elevation = round(random.uniform(*p["elevation_range"]), 1)
        dist_river = round(random.uniform(*p["distance_river_range"]), 2)
        drainage = round(max(5.0, min(95.0, p["drainage_base"] + random.gauss(0, 10))), 1)
        
        # Rainfall and environmental intensity
        # Prone districts receive higher likelihood of extreme rainfall simulation
        prone_bias = p["flood_prone_factor"]
        
        is_monsoon_surge = random.random() < (0.28 * prone_bias)
        if is_monsoon_surge:
            rainfall = round(random.uniform(180.0, 480.0), 1)
            river_level = round(random.uniform(4.0, 12.5), 2)
            reservoir_level = round(random.uniform(82.0, 99.8), 1)
            humidity = round(random.uniform(88.0, 99.0), 1)
            temp = round(random.uniform(21.0, 27.0), 1)
            wind_speed = round(random.uniform(35.0, 85.0), 1)
            emergency_reports = random.randint(30, 250)
            social_posts = random.randint(150, 2500)
            sentiment = round(random.uniform(-0.95, -0.40), 2)
            keyword_score = round(random.uniform(65.0, 98.0), 1)
        else:
            rainfall = round(max(0.0, random.uniform(5.0, 120.0)), 1)
            river_level = round(random.uniform(0.5, 3.8), 2)
            reservoir_level = round(random.uniform(40.0, 80.0), 1)
            humidity = round(random.uniform(60.0, 85.0), 1)
            temp = round(random.uniform(26.0, 34.0), 1)
            wind_speed = round(random.uniform(8.0, 28.0), 1)
            emergency_reports = random.randint(0, 15)
            social_posts = random.randint(2, 60)
            sentiment = round(random.uniform(-0.25, 0.50), 2)
            keyword_score = round(random.uniform(5.0, 35.0), 1)
            
        # Timestamp based on source
        if src_type == "Historical":
            days_range = (end_date_hist - start_date_hist).days
            rec_time = start_date_hist + timedelta(days=random.randint(0, days_range), hours=random.randint(0, 23))
        elif src_type == "Current":
            rec_time = current_date + timedelta(days=random.randint(0, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        else: # Social_Media
            rec_time = current_date + timedelta(days=random.randint(0, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            
        # Compute 0-100 normalized scores for the 6 factors
        # 1. Rainfall score (400mm = 100)
        s_rainfall = min(100.0, (rainfall / 400.0) * 100.0)
        # 2. River level score (above 6m = danger)
        s_river = min(100.0, (river_level / 8.0) * 100.0)
        # 3. History score (based on base frequency 0-10)
        hist_count = p["hist_freq_base"] + (1 if is_monsoon_surge else 0)
        s_history = min(100.0, (hist_count / 10.0) * 100.0)
        # 4. Geography vulnerability score (low elevation + close to river + poor drainage)
        geo_elev_factor = max(0.0, (100.0 - min(100.0, elevation * 1.5)))
        geo_river_factor = max(0.0, (10.0 - dist_river) * 10.0)
        geo_drain_factor = 100.0 - drainage
        s_geography = min(100.0, max(5.0, (geo_elev_factor * 0.4 + geo_river_factor * 0.3 + geo_drain_factor * 0.3)))
        # 5. Population exposure score
        s_population = min(100.0, (p["population_base"] / 4200000.0) * 100.0)
        # 6. Emergency & social score
        s_emergency = min(100.0, (emergency_reports * 0.3) + (keyword_score * 0.5))
        
        # Exact composite risk score (0-100)
        risk_score = calculate_exact_risk_score(s_rainfall, s_river, s_history, s_geography, s_population, s_emergency)
        
        # Historical recurrence trend adjustment (+15 if severe history and current risk > 65)
        if hist_count >= 7 and risk_score >= 65.0:
            risk_score = min(100.0, round(risk_score + 10.0, 2))
            
        risk_lvl = classify_risk_level(risk_score)
        emergency_priority = determine_emergency_priority(risk_lvl, s_population)
        
        # Ground-truth indicators & impact estimates
        flood_occurred = 1 if (risk_score >= 60.0 or is_monsoon_surge) else 0
        if flood_occurred:
            houses_affected = int((p["population_base"] / 40.0) * (risk_score / 100.0) * random.uniform(0.05, 0.25))
            infra_damage = round(min(100.0, (risk_score * 0.85) + random.uniform(2.0, 12.0)), 1)
            casualties = int(random.uniform(0, 8) * (1 if risk_score > 75 else 0))
            crop_damage = round((risk_score * 2.8) * random.uniform(0.8, 1.5), 1)
        else:
            houses_affected = 0
            infra_damage = round(random.uniform(0.0, 15.0), 1)
            casualties = 0
            crop_damage = round(random.uniform(0.0, 5.0), 1)
            
        return [
            f"KLD-{src_type[:3].upper()}-{i+1:06d}",
            rec_time.strftime("%Y-%m-%d %H:%M:%S"),
            dist_name,
            taluk,
            village,
            lat,
            lon,
            src_type,
            rainfall,
            river_level,
            reservoir_level,
            temp,
            humidity,
            wind_speed,
            flood_occurred,
            risk_lvl if flood_occurred else "None",
            p["population_base"],
            houses_affected,
            infra_damage,
            casualties,
            crop_damage,
            emergency_reports,
            social_posts,
            sentiment,
            keyword_score,
            hist_count,
            elevation,
            dist_river,
            drainage,
            risk_score,
            risk_lvl,
            emergency_priority
        ]

    # Batch writing to file for fast memory execution
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        
        count = 0
        batch = []
        batch_size = 5000
        
        # 1. Historical
        for i in range(n_historical):
            batch.append(create_single_record("Historical", count))
            count += 1
            if len(batch) >= batch_size:
                writer.writerows(batch)
                batch = []
                
        # 2. Current
        for i in range(n_current):
            batch.append(create_single_record("Current", count))
            count += 1
            if len(batch) >= batch_size:
                writer.writerows(batch)
                batch = []
                
        # 3. Social Media
        for i in range(n_social):
            batch.append(create_single_record("Social_Media", count))
            count += 1
            if len(batch) >= batch_size:
                writer.writerows(batch)
                batch = []
                
        if batch:
            writer.writerows(batch)
            
    print(f"[SUCCESS] Generated {count} records successfully at {OUTPUT_FILE}")
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"[INFO] File Size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    generate_records(100000)
