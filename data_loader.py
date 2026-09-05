import pandas as pd
import numpy as np
import glob
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def find_date_column(df: pd.DataFrame) -> str:
    """Finds the datetime or date column dynamically."""
    possible_names = ['date', 'datetime', 'timestamp', 'reading_time', 'time', 'Date', 'DateTime', 'Timestamp']
    for col in df.columns:
        if col.strip() in possible_names or 'date' in col.lower() or 'time' in col.lower():
            return col
    # Fallback to the first column if none match
    return df.columns[0]

def find_value_column(df: pd.DataFrame, exclude_col: str) -> str:
    """Finds the numeric reading column dynamically."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if exclude_col in numeric_cols:
        numeric_cols.remove(exclude_col)
    if numeric_cols:
        return numeric_cols[0]
    non_date_cols = [c for c in df.columns if c != exclude_col]
    return non_date_cols[0] if non_date_cols else df.columns[0]

def load_cwc_rainfall(state_code: str = "ts") -> pd.DataFrame:
    pattern = os.path.join(DATA_DIR, f"rainfall_tel_hr_cwc_{state_code.lower()}*.csv")
    files = glob.glob(pattern)
    
    if not files:
        files = glob.glob(os.path.join(DATA_DIR, "rainfall_tel_hr_cwc_*.csv"))
        if not files:
            print(f"⚠️ No rainfall CSVs found in {DATA_DIR}")
            return pd.DataFrame()

    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    date_col = find_date_column(df)
    df['date'] = pd.to_datetime(df[date_col], errors='coerce').dt.date

    val_col = find_value_column(df, exclude_col=date_col)
    df['rainfall_mm'] = pd.to_numeric(df[val_col], errors='coerce').fillna(0.0)

    daily_rain = df.groupby('date')['rainfall_mm'].sum().reset_index()
    daily_rain['rainfall_mm'] = daily_rain['rainfall_mm'].clip(lower=0.0)
    return daily_rain

def load_cgwb_groundwater(state_code: str = "ts") -> pd.DataFrame:
    pattern = os.path.join(DATA_DIR, f"gwl_tel_6_hourly_cgwb_{state_code.lower()}*.csv")
    files = glob.glob(pattern)
    
    if not files:
        files = glob.glob(os.path.join(DATA_DIR, "gwl_tel_6_hourly_cgwb_*.csv"))
        if not files:
            print(f"⚠️ No groundwater CSVs found in {DATA_DIR}")
            return pd.DataFrame()

    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    date_col = find_date_column(df)
    df['date'] = pd.to_datetime(df[date_col], errors='coerce').dt.date

    val_col = find_value_column(df, exclude_col=date_col)
    df['gw_depth_m'] = pd.to_numeric(df[val_col], errors='coerce')

    daily_gw = df.groupby('date')['gw_depth_m'].mean().reset_index()
    daily_gw['gw_depth_m'] = daily_gw['gw_depth_m'].interpolate(method='linear').bfill().ffill()
    return daily_gw

def build_master_dataset(synthetic_filename: str = "EWSS_2.0_synthetic_dataset_10000.csv", state_code: str = "ts") -> pd.DataFrame:
    synthetic_path = os.path.join(DATA_DIR, synthetic_filename)
    if not os.path.exists(synthetic_path):
        raise FileNotFoundError(f"Missing base dataset: {synthetic_path}")

    df_main = pd.read_csv(synthetic_path)
    df_rain = load_cwc_rainfall(state_code)
    df_gw = load_cgwb_groundwater(state_code)

    if not df_rain.empty and len(df_rain) > 0:
        n = min(len(df_main), len(df_rain))
        df_main.loc[:n-1, 'Rainfall_mm'] = df_rain['rainfall_mm'].values[:n]

    if not df_gw.empty and len(df_gw) > 0:
        n = min(len(df_main), len(df_gw))
        df_main.loc[:n-1, 'Groundwater_Depth_m'] = df_gw['gw_depth_m'].values[:n]

    return df_main

if __name__ == "__main__":
    fused_df = build_master_dataset(state_code="ts")
    out_path = os.path.join(DATA_DIR, "EWSS_master_fused_dataset.csv")
    fused_df.to_csv(out_path, index=False)
    print(f"✅ Data Fusion Successful! Saved merged dataset to {out_path}")