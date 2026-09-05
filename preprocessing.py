import numpy as np

THRESHOLDS = {
    "pH": {"min": 6.5, "max": 8.5, "direction": "optimal_range"},
    "COD_mgL": {"min": 250, "max": 120000, "direction": "lower_is_better"},
    "BOD_mgL": {"min": 30, "max": 65000, "direction": "lower_is_better"},
    "TDS_mgL": {"min": 500, "max": 6000, "direction": "lower_is_better"},
    "Water_Consumption_Ratio": {"min": 6.0, "max": 18.0, "direction": "lower_is_better"},
    "Groundwater_Depth_m": {"min": 5.0, "max": 30.0, "direction": "lower_is_better"},
    "Rainfall_mm": {"min": 0.0, "max": 50.0, "direction": "higher_is_better"}
}

def normalize_parameter(val: float, param_name: str) -> float:
    config = THRESHOLDS[param_name]
    low, high = config["min"], config["max"]
    val_clipped = np.clip(val, low, high)
    scaled = (val_clipped - low) / (high - low + 1e-6)
    
    if config["direction"] == "lower_is_better":
        return float(1.0 - scaled)
    elif config["direction"] == "higher_is_better":
        return float(scaled)
    elif config["direction"] == "optimal_range":
        mid = (low + high) / 2.0
        dist = abs(val_clipped - mid) / (high - low)
        return float(max(0.0, 1.0 - (dist * 2)))
    
    return float(scaled)

def compute_all_subscores(raw_inputs: dict) -> dict:
    return {param: normalize_parameter(val, param) for param, val in raw_inputs.items()}