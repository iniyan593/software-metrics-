import os
import pandas as pd
import numpy as np

# Ensure data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

output_file = os.path.join(DATA_DIR, "EWSS_2.0_synthetic_dataset_10000.csv")

# 1. First row: Explicitly engineered for >80 Composite Score (EXCELLENT Status)
high_score_row = {
    "pH": 7.20,
    "COD_mgL": 12000.0,
    "BOD_mgL": 6000.0,
    "TDS_mgL": 750.0,
    "Water_Consumption_Ratio": 6.50,
    "Groundwater_Depth_m": 6.00,
    "Rainfall_mm": 45.0
}

# 2. Generate remaining synthetic rows for baseline variation (100 rows for quick loading)
np.random.seed(42)
n_samples = 99

synthetic_data = {
    "pH": np.round(np.random.uniform(5.5, 9.0, n_samples), 2),
    "COD_mgL": np.round(np.random.uniform(15000, 100000, n_samples), 1),
    "BOD_mgL": np.round(np.random.uniform(8000, 55000, n_samples), 1),
    "TDS_mgL": np.round(np.random.uniform(1000, 5500, n_samples), 1),
    "Water_Consumption_Ratio": np.round(np.random.uniform(7.0, 17.0, n_samples), 2),
    "Groundwater_Depth_m": np.round(np.random.uniform(5.0, 30.0, n_samples), 2),
    "Rainfall_mm": np.round(np.random.uniform(0.0, 50.0, n_samples), 1)
}

df_synthetic = pd.DataFrame(synthetic_data)

# Combine high score row at Index 0 with the rest
df_final = pd.concat([pd.DataFrame([high_score_row]), df_synthetic], ignore_index=True)

# Save file to data folder
df_final.to_csv(output_file, index=False)
print(f"✅ Generated synthetic dataset successfully at: {output_file}")
print("📌 Row index 0 contains the >80 EXCELLENT score dataset.")