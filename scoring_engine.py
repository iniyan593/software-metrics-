import numpy as np

DEFAULT_WEIGHTS = {
    "pH": 0.08,
    "COD_mgL": 0.25,
    "BOD_mgL": 0.22,
    "TDS_mgL": 0.12,
    "Water_Consumption_Ratio": 0.15,
    "Groundwater_Depth_m": 0.10,
    "Rainfall_mm": 0.08
}

def calculate_ewss(sub_scores: dict, weights: dict = DEFAULT_WEIGHTS, input_std: float = 0.02, model_std: float = 0.03) -> dict:
    total_w = sum(weights.values())
    norm_weights = {k: v / total_w for k, v in weights.items()}
    
    ewss = 100.0 * sum(norm_weights[p] * sub_scores[p] for p in sub_scores)
    
    combined_std = np.sqrt((input_std ** 2) + (model_std ** 2))
    margin_of_error = 1.96 * combined_std * 100.0
    
    return {
        "EWSS": round(ewss, 2),
        "CI_Lower": round(max(0.0, ewss - margin_of_error), 2),
        "CI_Upper": round(min(100.0, ewss + margin_of_error), 2),
        "Margin_of_Error": round(margin_of_error, 2),
        "Normalized_Weights": norm_weights
    }