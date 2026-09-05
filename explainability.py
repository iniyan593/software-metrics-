def generate_shap_attributions(sub_scores: dict, weights: dict) -> list:
    attributions = []
    for param, score in sub_scores.items():
        w = weights[param]
        impact_loss = (1.0 - score) * w * 100.0
        attributions.append({
            "parameter": param,
            "sub_score": round(score, 3),
            "weight": round(w, 3),
            "points_lost": round(impact_loss, 2)
        })
    return sorted(attributions, key=lambda x: x["points_lost"], reverse=True)

def generate_insights(attributions: list) -> list:
    alerts = []
    for item in attributions:
        if item["points_lost"] > 5.0:
            alerts.append(
                f"⚠️ High Risk: **{item['parameter']}** sub-score ({item['sub_score']}) reduced overall score by **-{item['points_lost']} pts**."
            )
        elif item["points_lost"] > 2.0:
            alerts.append(
                f"⚡ Caution: **{item['parameter']}** degraded overall score by **-{item['points_lost']} pts**."
            )
    return alerts