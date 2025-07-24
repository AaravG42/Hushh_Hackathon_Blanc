from typing import Dict, List, Any, Optional
import json
import re
from dataclasses import dataclass

from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope
from hushh_mcp.types import UserID
from hushh_mcp.vault.encrypt import encrypt_data, decrypt_data
from hushh_mcp.config import VAULT_ENCRYPTION_KEY

@dataclass
class EthicalValues:
    environmental_importance: int  # 1-5
    labor_practices_importance: int  # 1-5
    local_sourcing_preference: int  # 1-5
    animal_welfare_importance: int  # 1-5
    transparency_importance: int  # 1-5

@dataclass
class EthicalScore:
    overall_score: float
    environmental_score: float  
    labor_score: float
    supply_chain_score: float
    transparency_score: float
    reasons: List[str]

class EthicalConsumptionAgent:
    """
    Privacy-first agent for ethical consumption analysis and product recommendations.
    """
    
    def __init__(self, agent_id: str = "ethical_consumption_agent"):
        self.agent_id = agent_id
        self.required_scopes = {
            "values_access": ConsentScope.CUSTOM_ETHICAL_VALUES,
            "email_access": ConsentScope.VAULT_READ_EMAIL,
            "finance_access": ConsentScope.VAULT_READ_FINANCE,
            "shopping_access": ConsentScope.AGENT_SHOPPING_PURCHASE,
            "supply_chain": ConsentScope.CUSTOM_SUPPLY_CHAIN
        }

    def assess_ethical_values(self, user_id: UserID, token_str: str) -> Dict[str, Any]:
        """
        Interactive quiz to assess user's ethical values and preferences.
        """
        valid, reason, token = validate_token(token_str, expected_scope=self.required_scopes["values_access"])
        
        if not valid:
            raise PermissionError(f"Consent validation failed: {reason}")
        
        if token.user_id != user_id:
            raise PermissionError("Token user ID does not match provided user")
            
        print("🌱 Welcome to the Ethical Values Assessment")
        print("This helps us understand your priorities for ethical consumption.\n")
        
        questions = [
            ("Environmental sustainability (climate impact, waste reduction)", "environmental_importance"),
            ("Fair labor practices (worker rights, fair wages)", "labor_practices_importance"), 
            ("Local sourcing vs global supply chains", "local_sourcing_preference"),
            ("Animal welfare considerations", "animal_welfare_importance"),
            ("Supply chain transparency", "transparency_importance")
        ]
        
        values = {}
        for question, key in questions:
            while True:
                try:
                    response = input(f"❓ Rate importance of {question} (1-5): ")
                    score = int(response)
                    if 1 <= score <= 5:
                        values[key] = score
                        break
                    else:
                        print("Please enter a number between 1 and 5")
                except ValueError:
                    print("Please enter a valid number")
        
        ethical_values = EthicalValues(**values)
        
        encrypted_values = encrypt_data(
            json.dumps(values), 
            VAULT_ENCRYPTION_KEY
        )
        
        print("✅ Values encrypted and stored locally with consent token validation")
        
        return {
            "status": "success",
            "message": "Ethical values assessment completed",
            "encrypted_data": encrypted_values,
            "summary": self._generate_values_summary(ethical_values)
        }

    def analyze_purchase_history(self, user_id: UserID, token_str: str, period: str = "last_6_months") -> Dict[str, Any]:
        """
        Analyze historical purchases and generate ethical/eco scores.
        """
        valid, reason, token = validate_token(token_str, expected_scope=self.required_scopes["email_access"])
        
        if not valid:
            raise PermissionError(f"Consent validation failed: {reason}")
            
        if token.user_id != user_id:
            raise PermissionError("Token user ID does not match provided user")
            
        print(f"🔍 Analyzing purchase history for {period}...")
        
        # Mock analysis - in real implementation would parse emails/transactions
        mock_analysis = {
            "total_purchases": 47,
            "ethical_score": 6.2,
            "eco_score": 7.1,
            "improvement_vs_last_period": {
                "ethical": 0.8,
                "eco": 1.2
            },
            "top_issues": [
                "23% of purchases from companies with poor labor practices",
                "67% of electronics from non-certified suppliers", 
                "Opportunity: 15 local alternatives available for frequent purchases"
            ],
            "recommendations": [
                "Consider B-Corp certified alternatives for your next electronics purchase",
                "Look for Fair Trade certified options in your regular grocery shopping",
                "Explore local farmers markets for produce and packaged goods"
            ]
        }
        
        encrypted_analysis = encrypt_data(
            json.dumps(mock_analysis),
            VAULT_ENCRYPTION_KEY
        )
        
        return {
            "status": "success", 
            "analysis": mock_analysis,
            "encrypted_data": encrypted_analysis,
            "period": period
        }

    def search_ethical_products(self, user_id: UserID, token_str: str, query: str, budget: Optional[int] = None) -> Dict[str, Any]:
        """
        Search for products and score them on ethical/environmental factors.
        """
        valid, reason, token = validate_token(token_str, expected_scope=self.required_scopes["shopping_access"])
        
        if not valid:
            raise PermissionError(f"Consent validation failed: {reason}")
            
        if token.user_id != user_id:
            raise PermissionError("Token user ID does not match provided user")
            
        print(f"🔍 Searching for '{query}' with ethical analysis...")
        
        if budget:
            print(f"💰 Budget constraint: ${budget}")
            
        # Mock product search and scoring
        mock_results = {
            "query": query,
            "total_options_analyzed": 47,
            "budget": budget,
            "recommendations": [
                {
                    "name": "Fairphone Headphones",
                    "price": 180,
                    "ethical_score": 9.2,
                    "eco_score": 8.8,
                    "certifications": ["Fair Trade", "Recyclable Materials"],
                    "strengths": ["Transparent supply chain", "Worker-owned factories", "Biodegradable packaging"],
                    "source": "fairphone.com"
                },
                {
                    "name": "Patagonia Audio Gear", 
                    "price": 195,
                    "ethical_score": 8.7,
                    "eco_score": 9.1,
                    "certifications": ["B-Corp", "1% for the Planet"],
                    "strengths": ["Carbon neutral shipping", "Repair program", "Recycled materials"],
                    "source": "patagonia.com"
                }
            ],
            "mainstream_comparison": {
                "name": "Sony XM4",
                "price": 199,
                "ethical_score": 4.1,
                "eco_score": 3.8,
                "issues": ["Supply chain concerns in 3rd party factories", "Limited transparency", "Non-renewable materials"]
            }
        }
        
        return {
            "status": "success",
            "results": mock_results,
            "timestamp": "2024-01-15T10:30:00Z"
        }

    def trace_supply_chain(self, user_id: UserID, token_str: str, product_url: str) -> Dict[str, Any]:
        """
        Trace supply chain for a specific product and analyze ethical factors.
        """
        valid, reason, token = validate_token(token_str, expected_scope=self.required_scopes["supply_chain"])
        
        if not valid:
            raise PermissionError(f"Consent validation failed: {reason}")
            
        if token.user_id != user_id:
            raise PermissionError("Token user ID does not match provided user")
            
        print(f"🔗 Tracing supply chain for: {product_url}")
        
        # Mock supply chain analysis
        mock_trace = {
            "product_url": product_url,
            "supply_chain": {
                "manufacturer": "TechCorp Manufacturing Ltd",
                "manufacturing_location": "Shenzhen, China",
                "raw_materials_origin": ["Democratic Republic of Congo (cobalt)", "Chile (lithium)", "Indonesia (nickel)"],
                "labor_certifications": ["SA8000", "WRAP"],
                "environmental_certifications": ["ISO14001"],
                "transparency_score": 6.5
            },
            "ethical_concerns": [
                "Cobalt sourcing from conflict regions",
                "Limited visibility into Tier 2/3 suppliers",
                "No living wage certification for factory workers"
            ],
            "positive_factors": [
                "Third-party labor audits conducted annually",
                "Waste reduction program in manufacturing",
                "Supplier code of conduct published"
            ],
            "overall_supply_chain_score": 5.8
        }
        
        encrypted_trace = encrypt_data(
            json.dumps(mock_trace),
            VAULT_ENCRYPTION_KEY
        )
        
        return {
            "status": "success",
            "supply_chain_analysis": mock_trace,
            "encrypted_data": encrypted_trace
        }

    def generate_report(self, user_id: UserID, token_str: str) -> Dict[str, Any]:
        """
        Generate comprehensive ethical consumption report.
        """
        # This would combine data from multiple scopes
        valid, reason, token = validate_token(token_str, expected_scope=self.required_scopes["email_access"])
        
        if not valid:
            raise PermissionError(f"Consent validation failed: {reason}")
            
        print("📊 Generating comprehensive ethical consumption report...")
        
        # Mock comprehensive report
        report = {
            "user_id": user_id,
            "report_date": "2024-01-15",
            "ethical_score_trend": [5.4, 5.8, 6.0, 6.2],
            "eco_score_trend": [5.9, 6.4, 6.8, 7.1], 
            "top_achievements": [
                "Increased purchases from B-Corp certified companies by 35%",
                "Reduced carbon footprint from shopping by 18%",
                "Supported 12 local businesses this quarter"
            ],
            "areas_for_improvement": [
                "Electronics sourcing - consider refurbished options",
                "Fast fashion purchases - explore sustainable brands",
                "Food packaging - look for zero-waste alternatives"
            ],
            "personalized_recommendations": [
                "Based on your environmental priority, consider Patagonia for outdoor gear",
                "For electronics, Fairphone aligns with your transparency values",
                "Local farmers market on Saturdays matches your local sourcing preference"
            ]
        }
        
        return {
            "status": "success",
            "report": report
        }

    def _generate_values_summary(self, values: EthicalValues) -> str:
        """Generate human-readable summary of user values."""
        priorities = []
        
        if values.environmental_importance >= 4:
            priorities.append("environmental sustainability")
        if values.labor_practices_importance >= 4:
            priorities.append("fair labor practices")
        if values.local_sourcing_preference >= 4:
            priorities.append("local sourcing")
        if values.animal_welfare_importance >= 4:
            priorities.append("animal welfare")
        if values.transparency_importance >= 4:
            priorities.append("supply chain transparency")
            
        if priorities:
            return f"Your top priorities: {', '.join(priorities)}"
        else:
            return "Balanced approach across all ethical factors" 