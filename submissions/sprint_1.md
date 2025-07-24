# 🌱 Sprint 1 Submission - Ethical Consumption Agent

Welcome to **Sprint 1** of the Hushh PDA Hackathon submission for **Team Blanc**.

This submission outlines our **Ethical Consumption Agent** - a privacy-first AI agent that helps users make ethical purchasing decisions while maintaining complete control over their personal data.

---

## 📦 Project Information

### ✅ GitHub Repo Link
```
https://github.com/YOUR_TEAM/Hushh_Hackathon_Blanc
```

### ✅ Agent Name
`ethical_consumption_agent`

### ✅ One-Line Problem Statement
"Conscious consumers today struggle to make ethical purchasing decisions because critical information about sustainability, labor practices, and sourcing is fragmented, hidden, or misleading.  Ethical Consumption Agent solves this by acting as a personalized shopping assistant that instantly analyzes products against your values, empowering you to shop with clarity, confidence, and conscience."

### ✅ Consent Scopes Required

Our agent will use the following consent scopes:

* `vault.read.email` - Access order confirmation emails and purchase history
* `vault.read.finance` - Analyze spending patterns and transaction data  
* `agent.shopping.purchase` - Search and analyze products from e-commerce platforms
* `custom.ethical.values` - Store and access user's personal ethical preferences and quiz results
* `custom.supply.chain` - Cache and encrypt supply chain analysis data

---

## 🧠 Agent Architecture & Technical Approach

### Core Components

**1. Values Assessment Module**
- Interactive CLI quiz system using `typer` for elegant UX
- Stores encrypted ethical preferences (environmental, labor rights, animal welfare, local sourcing)
- Uses weighted scoring system based on user priorities

**2. Historical Analysis Engine**  
- Processes email receipts and transaction data with consent validation
- Calculates personal "Ethical Score" and "Eco Score" based on past purchases
- Generates trend analysis and recommendations for improvement

**3. Product Research & Supply Chain Tracer**
- Integrates with Amazon Product API and web scraping (BeautifulSoup, Selenium)
- Follows supply chain links: seller → manufacturer → origin country → labor practices
- Cross-references with ethical databases (Fair Trade, B-Corp, environmental certifications)

**4. Real-time Shopping Assistant**
- When user wants to buy something, agent searches across multiple platforms
- Scores each option on ethics/environment using cached data and real-time analysis
- Provides alternative recommendations with better ethical scores

### Privacy & Consent Architecture

**Consent Flow:**
```python
# Every action requires valid consent token
token = issue_token(user_id, "ethical_consumption_agent", required_scope)
valid, reason, parsed = validate_token(token, expected_scope)

# All personal data encrypted in vault
encrypted_values = encrypt_data(user_ethical_preferences, vault_key)
encrypted_history = encrypt_data(purchase_analysis, vault_key)
```

**Data Encryption:**
- User values/preferences: AES-256-GCM encrypted locally
- Purchase history analysis: Encrypted before storage
- Supply chain cache: Encrypted with per-user keys
- No plaintext PII ever stored or transmitted

---

## 🛠 Tech Stack

**Core Framework:**
- Python 3.10+ with HushhMCP protocol
- Typer/Click for rich CLI interactions
- Pydantic for data validation

**AI & Analysis:**
- OpenAI GPT-4 or Claude for natural language processing
- LangChain for agent workflows and tool integration
- Pandas for data analysis and scoring calculations

**Web Scraping & APIs:**
- Amazon Product Advertising API (primary)
- Requests + BeautifulSoup for supply chain link following
- Selenium for dynamic content when needed

**Storage & Encryption:**
- Local SQLite with AES-256-GCM encryption
- HushhMCP vault system for all user data
- No remote databases - privacy-first architecture

---

## 🎯 Key Features & User Experience

### 1. Ethical Values Assessment
```bash
$ hushh-ethical-agent quiz
🌱 Let's understand your values...

❓ How important is environmental sustainability? (1-5)
❓ Rate importance of fair labor practices: (1-5)  
❓ Local vs global sourcing preference?
❓ Animal welfare considerations?

✅ Values encrypted and stored locally with consent token validation
```

### 2. Historical Analysis Dashboard
```bash
$ hushh-ethical-agent analyze --period=last_6_months

📊 Your Ethical Consumption Report:
   
   Ethical Score: 6.2/10 📈 (+0.8 from last month)
   Eco Score: 7.1/10 🌱 (+1.2 from last month)
   
   Top Issues Found:
   • 23% of purchases from companies with poor labor practices
   • 67% of electronics from non-certified suppliers
   • Opportunity: 15 local alternatives available for frequent purchases
```

### 3. Smart Shopping Assistant
```bash
$ hushh-ethical-agent search "wireless headphones" --budget=200

🔍 Analyzed 47 options across 5 platforms...

🏆 Best Ethical Choice:
   Fairphone Headphones - $180
   ✅ Ethical Score: 9.2/10
   ✅ Eco Score: 8.8/10
   ✅ Fair Trade certified, recyclable materials
   
⚠️  Popular Choice (for comparison):
   Sony XM4 - $199  
   ❌ Ethical Score: 4.1/10
   ❌ Supply chain concerns in 3rd party factories
```

---

## 🧬 Modular Design - Genes & Operons

Following Hushh's biological philosophy:

**Operons (Reusable Workflows):**
- `assess_ethical_values()` - Quiz and preference storage
- `analyze_purchase_history()` - Historical scoring and trends
- `trace_supply_chain()` - Product origin and ethics research
- `score_ethical_factors()` - Weighted scoring algorithm

**Genes (Atomic Functions):**
- `validate_consent_token()` - Security gatekeeper
- `encrypt_user_data()` - Privacy protection
- `scrape_product_info()` - Data collection
- `calculate_scores()` - Ethics/eco scoring

---

## 🔐 Security & Privacy Guarantees

**Consent-First Design:**
- Every data access requires explicit user consent via signed tokens
- Granular permissions - user controls what data agent can access
- Automatic token expiration and revocation support

**Data Minimization:**
- Only collects necessary data for ethical analysis
- Aggregated insights, not raw transaction details stored
- User can delete all data at any time

**Encryption Everywhere:**
- All personal data encrypted at rest using HushhMCP vault
- No third-party analytics or tracking
- Supply chain cache encrypted per-user

---

## 🧪 Testing Strategy

**Consent Flow Tests:**
```python
def test_ethical_agent_consent_flow():
    token = issue_token("user_123", "ethical_consumption_agent", "vault.read.email")
    agent = EthicalConsumptionAgent()
    
    # Should succeed with valid token
    result = agent.analyze_purchase_history("user_123", token.token)
    assert "ethical_score" in result
    
    # Should fail without consent
    with pytest.raises(PermissionError):
        agent.analyze_purchase_history("user_123", "invalid_token")
```

**Integration Tests:**
- Mock purchase history analysis
- Mock supply chain API responses  
- End-to-end ethical scoring workflow
- Encryption/decryption roundtrip tests

---

Let's build AI agents that help users consume more ethically.
Build with consent. Build with purpose.

—
Team Blanc
