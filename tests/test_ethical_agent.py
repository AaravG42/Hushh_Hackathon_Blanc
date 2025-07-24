import pytest
import json
from unittest.mock import patch, MagicMock

from hushh_mcp.consent.token import issue_token, revoke_token
from hushh_mcp.constants import ConsentScope
from hushh_mcp.agents.ethical_consumption_agent.index import EthicalConsumptionAgent, EthicalValues
from hushh_mcp.operons.assess_ethical_values import assess_ethical_values
from hushh_mcp.operons.score_ethical_factors import score_ethical_factors


class TestEthicalConsumptionAgent:
    """Test suite for Ethical Consumption Agent with consent validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.user_id = "user_test_123"
        self.agent = EthicalConsumptionAgent()
        
    def test_agent_initialization(self):
        """Test agent initializes with correct scopes."""
        assert self.agent.agent_id == "ethical_consumption_agent"
        assert "values_access" in self.agent.required_scopes
        assert "email_access" in self.agent.required_scopes
        assert "shopping_access" in self.agent.required_scopes
        
    def test_ethical_values_assessment_with_consent(self):
        """Test values assessment with valid consent token."""
        # Issue valid consent token
        token = issue_token(
            self.user_id, 
            "ethical_consumption_agent", 
            ConsentScope("custom.ethical.values")
        )
        
        # Mock input for non-interactive testing
        with patch('builtins.input', side_effect=['4', '5', '3', '4', '5']):
            result = self.agent.assess_ethical_values(self.user_id, token.token)
            
        assert result["status"] == "success"
        assert "encrypted_data" in result
        assert "summary" in result
        assert "environmental sustainability" in result["summary"].lower()
        
    def test_ethical_values_assessment_without_consent(self):
        """Test values assessment fails without proper consent."""
        with pytest.raises(PermissionError, match="Consent validation failed"):
            self.agent.assess_ethical_values(self.user_id, "invalid_token")
            
    def test_ethical_values_assessment_wrong_user(self):
        """Test values assessment fails with token for different user."""
        token = issue_token(
            "different_user", 
            "ethical_consumption_agent", 
            ConsentScope("custom.ethical.values")
        )
        
        with pytest.raises(PermissionError, match="Token user ID does not match"):
            self.agent.assess_ethical_values(self.user_id, token.token)
            
    def test_purchase_history_analysis_with_consent(self):
        """Test purchase history analysis with valid consent."""
        token = issue_token(
            self.user_id,
            "ethical_consumption_agent", 
            ConsentScope.VAULT_READ_EMAIL
        )
        
        result = self.agent.analyze_purchase_history(self.user_id, token.token)
        
        assert result["status"] == "success"
        assert "analysis" in result
        assert "encrypted_data" in result
        assert result["analysis"]["ethical_score"] > 0
        assert result["analysis"]["eco_score"] > 0
        assert len(result["analysis"]["top_issues"]) > 0
        
    def test_purchase_history_analysis_without_consent(self):
        """Test purchase history analysis fails without consent."""
        with pytest.raises(PermissionError):
            self.agent.analyze_purchase_history(self.user_id, "invalid_token")
            
    def test_product_search_with_consent(self):
        """Test product search with valid consent token."""
        token = issue_token(
            self.user_id,
            "ethical_consumption_agent",
            ConsentScope.AGENT_SHOPPING_PURCHASE
        )
        
        result = self.agent.search_ethical_products(
            self.user_id, 
            token.token, 
            "wireless headphones", 
            budget=200
        )
        
        assert result["status"] == "success"
        assert "results" in result
        assert result["results"]["query"] == "wireless headphones"
        assert result["results"]["budget"] == 200
        assert len(result["results"]["recommendations"]) > 0
        
        # Check ethical scoring
        first_rec = result["results"]["recommendations"][0]
        assert "ethical_score" in first_rec
        assert "eco_score" in first_rec
        assert first_rec["ethical_score"] > 0
        assert first_rec["eco_score"] > 0
        
    def test_supply_chain_trace_with_consent(self):
        """Test supply chain tracing with valid consent."""
        token = issue_token(
            self.user_id,
            "ethical_consumption_agent",
            ConsentScope("custom.supply.chain")
        )
        
        result = self.agent.trace_supply_chain(
            self.user_id,
            token.token,
            "https://example.com/product/123"
        )
        
        assert result["status"] == "success"
        assert "supply_chain_analysis" in result
        assert "encrypted_data" in result
        
        analysis = result["supply_chain_analysis"]
        assert "supply_chain" in analysis
        assert "ethical_concerns" in analysis
        assert "positive_factors" in analysis
        assert "overall_supply_chain_score" in analysis
        
    def test_consent_token_revocation(self):
        """Test that revoked tokens are rejected."""
        token = issue_token(
            self.user_id,
            "ethical_consumption_agent",
            ConsentScope("custom.ethical.values")
        )
        
        # Revoke the token
        revoke_token(token.token)
        
        # Should fail with revoked token
        with pytest.raises(PermissionError, match="Token has been revoked"):
            self.agent.assess_ethical_values(self.user_id, token.token)
            
    def test_comprehensive_report_generation(self):
        """Test comprehensive report generation."""
        token = issue_token(
            self.user_id,
            "ethical_consumption_agent",
            ConsentScope.VAULT_READ_EMAIL
        )
        
        result = self.agent.generate_report(self.user_id, token.token)
        
        assert result["status"] == "success"
        assert "report" in result
        
        report = result["report"]
        assert "ethical_score_trend" in report
        assert "eco_score_trend" in report
        assert "top_achievements" in report
        assert "areas_for_improvement" in report
        assert "personalized_recommendations" in report
        
    def test_values_summary_generation(self):
        """Test ethical values summary generation."""
        values = EthicalValues(
            environmental_importance=5,
            labor_practices_importance=4,
            local_sourcing_preference=2,
            animal_welfare_importance=1,
            transparency_importance=5
        )
        
        summary = self.agent._generate_values_summary(values)
        
        assert "environmental sustainability" in summary
        assert "fair labor practices" in summary
        assert "supply chain transparency" in summary
        assert "local sourcing" not in summary  # Score was only 2
        assert "animal welfare" not in summary  # Score was only 1


class TestEthicalValueOperon:
    """Test the reusable ethical values assessment operon."""
    
    def test_assess_ethical_values_interactive_mode(self):
        """Test interactive mode with mocked input."""
        with patch('builtins.input', side_effect=['4', '5', '3', '2', '4']):
            result = assess_ethical_values(interactive=True)
            
        assert "values" in result
        assert "summary" in result
        assert result["values"]["environmental_importance"] == 4
        assert result["values"]["labor_practices_importance"] == 5
        assert result["assessment_type"] == "interactive"
        
    def test_assess_ethical_values_batch_mode(self):
        """Test batch mode with default values."""
        result = assess_ethical_values(interactive=False)
        
        assert "values" in result
        assert all(score == 3 for score in result["values"].values())
        assert result["assessment_type"] == "default"
        assert result["summary"] == "Balanced approach"


class TestEthicalScoringOperon:
    """Test the reusable ethical scoring operon."""
    
    def test_score_ethical_factors_with_certifications(self):
        """Test scoring with various certifications."""
        product_data = {
            "certifications": ["Fair Trade", "B-Corp", "Organic"],
            "origin": "Local, USA",
            "labor_practices": {"living_wage": True, "worker_rights": True},
            "environmental_impact": {"carbon_neutral": True, "renewable_energy": True},
            "supply_chain": {
                "transparency_score": 8,
                "public_reporting": True,
                "tier_visibility": ["tier1", "tier2", "tier3"]
            }
        }
        
        user_values = {
            "environmental_importance": 5,
            "labor_practices_importance": 4,
            "transparency_importance": 5
        }
        
        result = score_ethical_factors(product_data, user_values)
        
        assert result["overall_score"] >= 7.0  # Should score highly
        assert result["user_alignment"] == "high"
        assert len(result["strengths"]) > 0
        assert len(result["certifications_found"]) == 3
        
    def test_score_ethical_factors_poor_practices(self):
        """Test scoring with poor ethical practices."""
        product_data = {
            "certifications": [],
            "origin": "Unknown",
            "labor_practices": {},
            "environmental_impact": {},
            "supply_chain": {"transparency_score": 2}
        }
        
        user_values = {
            "environmental_importance": 5,
            "labor_practices_importance": 5,
            "transparency_importance": 5
        }
        
        result = score_ethical_factors(product_data, user_values)
        
        assert result["overall_score"] <= 6.0  # Should score poorly
        assert len(result["concerns"]) > 0
        assert result["certifications_found"] == []
        
    def test_score_ethical_factors_custom_weights(self):
        """Test scoring with custom weights."""
        product_data = {
            "certifications": ["Fair Trade"],
            "origin": "Local",
            "labor_practices": {"fair_wages": True},
            "environmental_impact": {"organic": True},
            "supply_chain": {"transparency_score": 7}
        }
        
        user_values = {"environmental_importance": 3}
        
        # Heavy environmental weighting
        custom_weights = {
            "environmental": 0.50,
            "labor": 0.20,
            "supply_chain": 0.15,
            "transparency": 0.10,
            "certifications": 0.05
        }
        
        result = score_ethical_factors(product_data, user_values, custom_weights)
        
        assert "overall_score" in result
        assert result["scoring_methodology"] == "weighted_multi_factor"
        
        # Environmental should be highly weighted
        assert result["component_scores"]["environmental"] > 0
        

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 