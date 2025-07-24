from typing import Dict, List, Any, Optional
import json

def score_ethical_factors(
    product_data: Dict[str, Any], 
    user_values: Dict[str, int],
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Reusable operon for calculating ethical scores based on product characteristics.
    
    Args:
        product_data (dict): Product information including certifications, origin, etc.
        user_values (dict): User's ethical preference scores (1-5)
        weights (dict, optional): Custom scoring weights
        
    Returns:
        dict: Comprehensive ethical scoring breakdown
    """
    
    # Default scoring weights
    if weights is None:
        weights = {
            "environmental": 0.25,
            "labor": 0.25, 
            "supply_chain": 0.20,
            "transparency": 0.15,
            "certifications": 0.15
        }
    
    # Extract product characteristics
    certifications = product_data.get("certifications", [])
    origin = product_data.get("origin", "unknown")
    labor_practices = product_data.get("labor_practices", {})
    environmental_impact = product_data.get("environmental_impact", {})
    supply_chain_info = product_data.get("supply_chain", {})
    
    # Calculate component scores (0-10 scale)
    scores = {}
    
    # Environmental score
    env_score = 5.0  # baseline
    if "organic" in [c.lower() for c in certifications]:
        env_score += 1.5
    if "carbon neutral" in str(environmental_impact).lower():
        env_score += 1.0
    if "renewable energy" in str(environmental_impact).lower():
        env_score += 1.0
    if "recyclable" in str(product_data).lower():
        env_score += 0.5
    
    scores["environmental"] = min(env_score, 10.0)
    
    # Labor practices score
    labor_score = 5.0  # baseline
    if "fair trade" in [c.lower() for c in certifications]:
        labor_score += 2.0
    if "living wage" in str(labor_practices).lower():
        labor_score += 1.5
    if "worker rights" in str(labor_practices).lower():
        labor_score += 1.0
    if "sa8000" in [c.lower() for c in certifications]:
        labor_score += 1.0
    
    scores["labor"] = min(labor_score, 10.0)
    
    # Supply chain score
    supply_score = 5.0  # baseline
    transparency_level = supply_chain_info.get("transparency_score", 5)
    supply_score = transparency_level
    
    if "local" in origin.lower() or "domestic" in origin.lower():
        supply_score += 1.5
    if len(supply_chain_info.get("tier_visibility", [])) > 2:
        supply_score += 1.0
    
    scores["supply_chain"] = min(supply_score, 10.0)
    
    # Transparency score
    trans_score = 5.0  # baseline
    if supply_chain_info.get("public_reporting", False):
        trans_score += 1.5
    if "b-corp" in [c.lower() for c in certifications]:
        trans_score += 2.0
    if len(certifications) > 2:
        trans_score += 1.0
    
    scores["transparency"] = min(trans_score, 10.0)
    
    # Certification bonus
    cert_score = min(len(certifications) * 1.5, 10.0)
    scores["certifications"] = cert_score
    
    # Calculate weighted overall score
    overall_score = sum(scores[factor] * weights[factor] for factor in weights.keys())
    
    # Apply user preference weighting
    user_weight_multiplier = 1.0
    if user_values.get("environmental_importance", 3) >= 4:
        user_weight_multiplier += 0.1 * (scores["environmental"] / 10)
    if user_values.get("labor_practices_importance", 3) >= 4:
        user_weight_multiplier += 0.1 * (scores["labor"] / 10)
    if user_values.get("transparency_importance", 3) >= 4:
        user_weight_multiplier += 0.1 * (scores["transparency"] / 10)
    
    final_score = min(overall_score * user_weight_multiplier, 10.0)
    
    # Generate explanation
    strengths = []
    concerns = []
    
    for factor, score in scores.items():
        if score >= 7.5:
            strengths.append(f"Strong {factor.replace('_', ' ')} practices")
        elif score <= 4.0:
            concerns.append(f"Limited {factor.replace('_', ' ')} information")
    
    return {
        "overall_score": round(final_score, 1),
        "component_scores": {k: round(v, 1) for k, v in scores.items()},
        "strengths": strengths,
        "concerns": concerns,
        "certifications_found": certifications,
        "user_alignment": "high" if user_weight_multiplier > 1.05 else "moderate",
        "scoring_methodology": "weighted_multi_factor"
    } 