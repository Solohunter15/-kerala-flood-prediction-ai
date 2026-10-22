"""
Module: hadoop_mapreduce.py
Purpose: Simulates Hadoop MapReduce distributed batch processing over the 100,000 (1 Lakh)
         record unified flood dataset stored in HDFS.
         Extracts district feature aggregations, peak telemetry, risk scores, and rankings.
"""

import csv
import json
import time
import os
import sys

DATASET_PATH = os.path.join(os.path.dirname(__file__), "kerala_flood_1lakh_unified.csv")
SUMMARY_JSON_PATH = os.path.join(os.path.dirname(__file__), "kerala_district_hadoop_summary.json")
SUMMARY_CSV_PATH = os.path.join(os.path.dirname(__file__), "kerala_district_hadoop_summary.csv")

class HadoopMapReduceSimulator:
    """
    Simulates the 3-phase Hadoop MapReduce processing architecture:
    1. Mapper: Parses and projects district telemetry tuples
    2. Shuffle & Sort: Partition grouping by District key
    3. Reducer: Aggregation, trend analysis, ranking, and Hive summary export
    """

    def __init__(self, input_csv_path=DATASET_PATH):
        self.input_csv_path = input_csv_path
        self.stats = {
            "total_records_processed": 0,
            "mapper_execution_ms": 0,
            "shuffle_sort_execution_ms": 0,
            "reducer_execution_ms": 0,
            "total_execution_ms": 0,
            "nodes_simulated": 4
        }

    def run_job(self):
        print(f"[*] Submitting Hadoop MapReduce Job: 'DistrictFloodRiskAggregationJob'")
        print(f"[*] Input HDFS Location: /data/kerala_flood/master/{os.path.basename(self.input_csv_path)}")
        t0 = time.time()

        # -------------------------------------------------------------
        # Phase 1: MAPPER PHASE
        # -------------------------------------------------------------
        print("[1/3] MAPPER PHASE: Reading input splits across 4 DataNodes...")
        t_map_start = time.time()
        
        intermediate_pairs = []
        with open(self.input_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                district = row["District"]
                # Mapper emits (Key: District, Value: extracted numeric metrics)
                val = (
                    float(row["Rainfall_mm"]),
                    float(row["River_Level_m"]),
                    float(row["Risk_Score"]),
                    int(row["Flood_Occurred"]),
                    int(row["Houses_Affected"]),
                    float(row["Infrastructure_Damage"]),
                    int(row["Emergency_Reports"]),
                    int(row["Social_Post_Count"])
                )
                intermediate_pairs.append((district, val))
                
        self.stats["total_records_processed"] = len(intermediate_pairs)
        self.stats["mapper_execution_ms"] = round((time.time() - t_map_start) * 1000, 2)
        print(f"      Mapped {self.stats['total_records_processed']} records in {self.stats['mapper_execution_ms']} ms")

        # -------------------------------------------------------------
        # Phase 2: SHUFFLE & SORT PHASE
        # -------------------------------------------------------------
        print("[2/3] SHUFFLE & SORT PHASE: Partitioning and grouping by District key...")
        t_shuffle_start = time.time()
        
        partition_buckets = {}
        for district, val in intermediate_pairs:
            if district not in partition_buckets:
                partition_buckets[district] = []
            partition_buckets[district].append(val)
            
        self.stats["shuffle_sort_execution_ms"] = round((time.time() - t_shuffle_start) * 1000, 2)
        print(f"      Grouped into {len(partition_buckets)} district keys in {self.stats['shuffle_sort_execution_ms']} ms")

        # -------------------------------------------------------------
        # Phase 3: REDUCER PHASE
        # -------------------------------------------------------------
        print("[3/3] REDUCER PHASE: Aggregating district metrics and computing risk index...")
        t_reduce_start = time.time()
        
        district_summaries = []
        for district, vals in partition_buckets.items():
            n = len(vals)
            avg_rainfall = sum(v[0] for v in vals) / n
            max_rainfall = max(v[0] for v in vals)
            
            avg_river = sum(v[1] for v in vals) / n
            max_river = max(v[1] for v in vals)
            
            avg_risk = sum(v[2] for v in vals) / n
            flood_instances = sum(v[3] for v in vals)
            total_houses_affected = sum(v[4] for v in vals)
            avg_infra_damage = sum(v[5] for v in vals) / n
            total_emergency_sos = sum(v[6] for v in vals)
            total_social_posts = sum(v[7] for v in vals)
            
            # Risk Level
            if avg_risk >= 75.0:
                lvl = "Critical"
                priority = "Level 1"
            elif avg_risk >= 60.0:
                lvl = "High"
                priority = "Level 2"
            elif avg_risk >= 40.0:
                lvl = "Moderate"
                priority = "Level 3"
            else:
                lvl = "Low"
                priority = "Level 4"
                
            district_summaries.append({
                "district": district,
                "records_analyzed": n,
                "avg_rainfall_mm": round(avg_rainfall, 2),
                "peak_rainfall_mm": round(max_rainfall, 2),
                "avg_river_level_m": round(avg_river, 2),
                "peak_river_level_m": round(max_river, 2),
                "avg_risk_score": round(avg_risk, 2),
                "risk_level": lvl,
                "emergency_priority": priority,
                "flood_occurrences_recorded": flood_instances,
                "total_houses_affected": total_houses_affected,
                "avg_infrastructure_damage": round(avg_infra_damage, 2),
                "total_emergency_reports": total_emergency_sos,
                "total_social_posts": total_social_posts
            })
            
        # Rank districts from highest to lowest risk
        district_summaries.sort(key=lambda x: x["avg_risk_score"], reverse=True)
        for rank, dist in enumerate(district_summaries, 1):
            dist["risk_rank"] = rank

        self.stats["reducer_execution_ms"] = round((time.time() - t_reduce_start) * 1000, 2)
        self.stats["total_execution_ms"] = round((time.time() - t0) * 1000, 2)
        print(f"      Reduced and ranked {len(district_summaries)} districts in {self.stats['reducer_execution_ms']} ms")
        print(f"[SUCCESS] Total MapReduce Job Duration: {self.stats['total_execution_ms']} ms")

        # Save to JSON
        output_payload = {
            "job_metadata": {
                "job_id": "job_hadoop_kerala_flood_001",
                "dataset_file": os.path.basename(self.input_csv_path),
                "records_processed": self.stats["total_records_processed"],
                "total_time_ms": self.stats["total_execution_ms"],
                "data_nodes": self.stats["nodes_simulated"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "districts": district_summaries
        }
        
        with open(SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, indent=2)
            
        # Save to CSV
        with open(SUMMARY_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "risk_rank", "district", "avg_risk_score", "risk_level",
                "emergency_priority", "avg_rainfall_mm", "peak_rainfall_mm",
                "avg_river_level_m", "peak_river_level_m", "records_analyzed",
                "flood_occurrences_recorded", "total_houses_affected",
                "avg_infrastructure_damage", "total_emergency_reports", "total_social_posts"
            ])
            writer.writeheader()
            writer.writerows(district_summaries)
            
        print(f"[SUCCESS] Exported Hive summary table to:\n - {SUMMARY_JSON_PATH}\n - {SUMMARY_CSV_PATH}")
        return output_payload

if __name__ == "__main__":
    job = HadoopMapReduceSimulator()
    res = job.run_job()
    print("\n--- TOP 5 MOST VULNERABLE DISTRICTS ---")
    for d in res["districts"][:5]:
        print(f"#{d['risk_rank']} {d['district']}: Score {d['avg_risk_score']} ({d['risk_level']}) - Priority: {d['emergency_priority']}")
