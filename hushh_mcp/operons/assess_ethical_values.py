from typing import Dict, Any
import json

def assess_ethical_values(interactive: bool = True) -> Dict[str, Any]:
    """
    Reusable operon for assessing user ethical values and preferences.
    
    Args:
        interactive (bool): Whether to use interactive CLI prompts
        
    Returns:
        dict: Structured ethical values data
    """
    
    if interactive:
        print("🌱 Ethical Values Assessment")
        print("Rate each factor's importance to you (1-5 scale)\n")
    
    questions = [
        ("Environmental sustainability (climate impact, waste reduction)", "environmental_importance"),
        ("Fair labor practices (worker rights, fair wages)", "labor_practices_importance"), 
        ("Local sourcing vs global supply chains", "local_sourcing_preference"),
        ("Animal welfare considerations", "animal_welfare_importance"),
        ("Supply chain transparency", "transparency_importance")
    ]
    
    values = {}
    
    if interactive:
        for question, key in questions:
            while True:
                try:
                    response = input(f"❓ {question} (1-5): ")
                    score = int(response)
                    if 1 <= score <= 5:
                        values[key] = score
                        break
                    else:
                        print("Please enter a number between 1 and 5")
                except ValueError:
                    print("Please enter a valid number")
    else:
        # Default balanced values for non-interactive mode
        for _, key in questions:
            values[key] = 3
    
    # Generate priority summary
    priorities = []
    for question, key in questions:
        if values[key] >= 4:
            priorities.append(question.split(' (')[0].lower())
    
    summary = f"Top priorities: {', '.join(priorities)}" if priorities else "Balanced approach"
    
    return {
        "values": values,
        "summary": summary,
        "total_score": sum(values.values()),
        "assessment_type": "interactive" if interactive else "default"
    } 