import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(BASE_DIR, "Company_Telemetry_Sample_Data.csv")

np.random.seed(101) # Set seed for reproducible evaluation data
data_rows = []

# High efficiency, low pollution load, sustainable groundwater usage
for i in range(15):
    data_rows.append({
        "Company_Record_ID": f"COMP-2026-{i+101:03d}",
        "pH": np.round(np.random.uniform(6.8, 7.6), 2),
        "COD_mgL": np.round(np.random.uniform(11000, 18000), 1),
        "BOD_mgL": np.round(np.random.uniform(5000, 8500), 1),
        "TDS_mgL": np.round(np.random.uniform(600, 1100), 1),
        "Water_Consumption_Ratio": np.round(np.random.uniform(4.2, 6.8), 2),
        "Groundwater_Depth_m": np.round(np.random.uniform(3.5, 7.0), 2),
        "Rainfall_mm": np.round(np.random.uniform(30.0, 75.0), 1)
    })

# Moderate organic load and standard operational consumption
for i in range(20):
    data_rows.append({
        "Company_Record_ID": f"COMP-2026-{i+116:03d}",
        "pH": np.round(np.random.uniform(6.3, 8.1), 2),
        "COD_mgL": np.round(np.random.uniform(22000, 48000), 1),
        "BOD_mgL": np.round(np.random.uniform(11000, 24000), 1),
        "TDS_mgL": np.round(np.random.uniform(1400, 3100), 1),
        "Water_Consumption_Ratio": np.round(np.random.uniform(7.8, 12.5), 2),
        "Groundwater_Depth_m": np.round(np.random.uniform(9.0, 17.5), 2),
        "Rainfall_mm": np.round(np.random.uniform(12.0, 32.0), 1)
    })

# High COD/BOD, excessive water usage, depleted aquifer levels
for i in range(15):
    data_rows.append({
        "Company_Record_ID": f"COMP-2026-{i+136:03d}",
        "pH": np.round(np.random.choice([np.random.uniform(4.2, 5.3), np.random.uniform(8.9, 9.8)]), 2),
        "COD_mgL": np.round(np.random.uniform(65000, 115000), 1),
        "BOD_mgL": np.round(np.random.uniform(32000, 62000), 1),
        "TDS_mgL": np.round(np.random.uniform(3800, 5700), 1),
        "Water_Consumption_Ratio": np.round(np.random.uniform(13.5, 19.0), 2),
        "Groundwater_Depth_m": np.round(np.random.uniform(23.0, 34.0), 2),
        "Rainfall_mm": np.round(np.random.uniform(0.0, 10.0), 1)
    })

df_company = pd.DataFrame(data_rows)
df_company.to_csv(output_file, index=False)

print(f"✅ Created Company Test Dataset with {len(df_company)} rows at:")
print(f"   {output_file}\n")
print("📊 Summary of generated rows:")
print(" - Rows 0-14  (COMP-2026-101 to 115): High Compliance / EXCELLENT (>80)")
print(" - Rows 15-34 (COMP-2026-116 to 135): Moderate Risk / ACCEPTABLE (60-79)")
print(" - Rows 35-49 (COMP-2026-136 to 150): High Risk / CRITICAL RISK (<60)")