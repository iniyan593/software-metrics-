import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def generate_balanced_dataset():
    np.random.seed(42) # For reproducible results
    rows = []
    
    # ------------------------------------------------------------------
    # Category 1: EXCELLENT scenarios (Rows 0 - 19) -> EWSS > 80
    # Clean effluent, efficient water ratio, good groundwater depth & rainfall
    # ------------------------------------------------------------------
    for _ in range(20):
        rows.append({
            "pH": np.round(np.random.uniform(6.8, 7.5), 2),
            "COD_mgL": np.round(np.random.uniform(10000, 18000), 1),
            "BOD_mgL": np.round(np.random.uniform(5000, 9000), 1),
            "TDS_mgL": np.round(np.random.uniform(500, 1000), 1),
            "Water_Consumption_Ratio": np.round(np.random.uniform(4.5, 7.0), 2),
            "Groundwater_Depth_m": np.round(np.random.uniform(3.0, 7.5), 2),
            "Rainfall_mm": np.round(np.random.uniform(35.0, 80.0), 1)
        })

    # ------------------------------------------------------------------
    # Category 2: ACCEPTABLE scenarios (Rows 20 - 59) -> EWSS 60 - 79
    # Moderate load, acceptable parameters
    # ------------------------------------------------------------------
    for _ in range(40):
        rows.append({
            "pH": np.round(np.random.uniform(6.2, 8.2), 2),
            "COD_mgL": np.round(np.random.uniform(25000, 45000), 1),
            "BOD_mgL": np.round(np.random.uniform(12000, 25000), 1),
            "TDS_mgL": np.round(np.random.uniform(1500, 3000), 1),
            "Water_Consumption_Ratio": np.round(np.random.uniform(8.0, 12.0), 2),
            "Groundwater_Depth_m": np.round(np.random.uniform(10.0, 18.0), 2),
            "Rainfall_mm": np.round(np.random.uniform(10.0, 35.0), 1)
        })

    # ------------------------------------------------------------------
    # Category 3: CRITICAL RISK scenarios (Rows 60 - 99) -> EWSS < 60
    # High organic pollution, severe water draw, depleted water tables
    # ------------------------------------------------------------------
    for _ in range(40):
        rows.append({
            "pH": np.round(np.random.choice([np.random.uniform(4.0, 5.5), np.random.uniform(8.8, 10.0)]), 2),
            "COD_mgL": np.round(np.random.uniform(60000, 110000), 1),
            "BOD_mgL": np.round(np.random.uniform(30000, 60000), 1),
            "TDS_mgL": np.round(np.random.uniform(3500, 5800), 1),
            "Water_Consumption_Ratio": np.round(np.random.uniform(13.0, 19.5), 2),
            "Groundwater_Depth_m": np.round(np.random.uniform(22.0, 34.0), 2),
            "Rainfall_mm": np.round(np.random.uniform(0.0, 15.0), 1)
        })

    df = pd.DataFrame(rows)
    main_file = os.path.join(DATA_DIR, "EWSS_2.0_synthetic_dataset_10000.csv")
    df.to_csv(main_file, index=False)
    
    print(f"✅ Generated balanced dataset with 100 rows at: {main_file}")
    print("📌 Rows 0-19: EXCELLENT (>80)")
    print("📌 Rows 20-59: ACCEPTABLE (60-79)")
    print("📌 Rows 60-99: CRITICAL RISK (<60)")

if __name__ == "__main__":
    generate_balanced_dataset()