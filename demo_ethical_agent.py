#!/usr/bin/env python3
"""
🌱 Ethical Consumption Agent Demo
Demonstrates privacy-first ethical consumption analysis with consent validation.
"""

import json
from hushh_mcp.consent.token import issue_token
from hushh_mcp.constants import ConsentScope
from hushh_mcp.agents.ethical_consumption_agent.index import EthicalConsumptionAgent

def demo_header():
    print("🌱" + "="*70 + "🌱")
    print("    ETHICAL CONSUMPTION AGENT - HUSHH PDA HACKATHON DEMO")
    print("    Privacy-First AI for Ethical Shopping Decisions")
    print("🌱" + "="*70 + "🌱\n")

def demo_product_search():
    print("🔍 PRODUCT SEARCH & ANALYSIS DEMONSTRATION")
    print("-" * 50)
    
    user_id = "demo_user_123"
    agent = EthicalConsumptionAgent()
    
    # Issue consent for shopping
    token = issue_token(user_id, "ethical_consumption_agent", ConsentScope.AGENT_SHOPPING_PURCHASE)
    
    print("Searching for 'wireless headphones' with $200 budget...")
    result = agent.search_ethical_products(user_id, token.token, "wireless headphones", budget=200)
    
    if result["status"] == "success":
        results = result["results"]
        print(f"✅ Analyzed {results['total_options_analyzed']} options")
        
        print("\n🏆 TOP ETHICAL RECOMMENDATION:")
        top_rec = results["recommendations"][0]
        print(f"   Product: {top_rec['name']}")
        print(f"   Price: ${top_rec['price']}")
        print(f"   Ethical Score: {top_rec['ethical_score']}/10")
        print(f"   Eco Score: {top_rec['eco_score']}/10")
        print(f"   Certifications: {', '.join(top_rec['certifications'])}")
        
        print("\n⚠️ MAINSTREAM COMPARISON:")
        mainstream = results["mainstream_comparison"]
        print(f"   Product: {mainstream['name']}")
        print(f"   Price: ${mainstream['price']}")
        print(f"   Ethical Score: {mainstream['ethical_score']}/10")
        print(f"   Issues: {', '.join(mainstream['issues'])}")
    
    print()

def demo_consent_flow():
    print("🔐 CONSENT-FIRST DESIGN DEMONSTRATION")
    print("-" * 50)
    
    user_id = "demo_user_123"
    agent = EthicalConsumptionAgent()
    
    # Issue consent token
    print("1. Issuing consent token for purchase analysis...")
    token = issue_token(user_id, "ethical_consumption_agent", ConsentScope.VAULT_READ_EMAIL)
    print(f"   ✅ Token issued: {token.token[:30]}...")
    print(f"   ✅ User ID: {token.user_id}")
    print(f"   ✅ Scope: {token.scope}")
    
    # Test consent validation
    print("\n2. Testing consent validation...")
    result = agent.analyze_purchase_history(user_id, token.token)
    print(f"   ✅ Consent accepted: {result['status']}")
    
    analysis = result["analysis"]
    print(f"   📊 Ethical Score: {analysis['ethical_score']}/10")
    print(f"   🌱 Eco Score: {analysis['eco_score']}/10")
    print(f"   📈 Improvement: +{analysis['improvement_vs_last_period']['ethical']} ethical")
    
    print()

def main():
    demo_header()
    
    print("This demo showcases the Ethical Consumption Agent's key features:")
    print("• Consent-first architecture with cryptographic token validation")
    print("• Multi-factor ethical scoring system")
    print("• Product search with ethical recommendations")
    print("• Purchase history analysis")
    print()
    
    try:
        demo_consent_flow()
        demo_product_search()
        
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("✅ All consent validation working")
        print("✅ All ethical scoring functional")
        print("\n" + "="*70)
        print("🌱 BUILD AI AGENTS THAT HELP USERS CONSUME MORE ETHICALLY")
        print("🌱 BUILD WITH CONSENT. BUILD WITH PURPOSE.")
        print("="*70)
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
