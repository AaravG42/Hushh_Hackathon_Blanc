# 🌱 Ethical Consumption Agent

A privacy-first AI agent for making ethical purchasing decisions while maintaining complete control over personal data.

## 🎯 Overview

The Ethical Consumption Agent empowers users to:
- **Assess personal ethical values** through interactive quizzes
- **Analyze purchase history** for ethical and environmental impact scoring  
- **Search for products** with comprehensive ethical analysis
- **Trace supply chains** to understand product origins and labor practices
- **Generate reports** with personalized recommendations for improvement

All while following **consent-first principles** and **end-to-end encryption**.

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Setup Environment

Create a `.env` file with required keys:
```bash
SECRET_KEY=your_64_character_secret_key_here
VAULT_ENCRYPTION_KEY=your_64_character_hex_vault_key_here
```

### Basic Usage

```bash
# Assess your ethical values
python -m hushh_mcp.agents.ethical_consumption_agent.cli quiz --user your_user_id

# Analyze purchase history  
python -m hushh_mcp.agents.ethical_consumption_agent.cli analyze --user your_user_id

# Search for ethical products
python -m hushh_mcp.agents.ethical_consumption_agent.cli search "wireless headphones" --user your_user_id --budget 200

# Trace supply chain
python -m hushh_mcp.agents.ethical_consumption_agent.cli trace "https://amazon.com/product/123" --user your_user_id

# Generate comprehensive report
python -m hushh_mcp.agents.ethical_consumption_agent.cli report --user your_user_id
```

## 🔐 Privacy & Consent

### Consent-First Design

Every operation requires explicit user consent via cryptographically signed tokens:

```python
from hushh_mcp.consent.token import issue_token
from hushh_mcp.constants import ConsentScope

# Issue consent for values assessment
token = issue_token(user_id, "ethical_consumption_agent", ConsentScope("custom.ethical.values"))

# Agent validates consent before any action
agent = EthicalConsumptionAgent()
result = agent.assess_ethical_values(user_id, token.token)
```

### Required Consent Scopes

| Scope | Purpose | Data Access |
|-------|---------|-------------|
| `custom.ethical.values` | Store ethical preferences | Quiz responses, value weights |
| `vault.read.email` | Purchase history analysis | Order confirmations, receipts |
| `vault.read.finance` | Spending pattern analysis | Transaction data, payment info |
| `agent.shopping.purchase` | Product search & scoring | Public product information |
| `custom.supply.chain` | Supply chain tracing | Manufacturer data, certifications |

### Data Encryption

All sensitive data is encrypted using AES-256-GCM:

```python
from hushh_mcp.vault.encrypt import encrypt_data, decrypt_data

# Encrypt user values before storage
encrypted_values = encrypt_data(json.dumps(user_values), VAULT_ENCRYPTION_KEY)

# Decrypt when needed (with valid consent)
decrypted_values = decrypt_data(encrypted_values, VAULT_ENCRYPTION_KEY)
```

## 🧬 Modular Design

### Operons (Reusable Functions)

The agent is built using modular "operons" that can be reused by other agents:

#### `assess_ethical_values()`
```python
from hushh_mcp.operons.assess_ethical_values import assess_ethical_values

# Interactive quiz
result = assess_ethical_values(interactive=True)

# Batch mode with defaults
result = assess_ethical_values(interactive=False)
```

#### `score_ethical_factors()`
```python
from hushh_mcp.operons.score_ethical_factors import score_ethical_factors

product_data = {
    "certifications": ["Fair Trade", "B-Corp"],
    "origin": "Local, USA",
    "labor_practices": {"living_wage": True}
}

user_values = {"environmental_importance": 5}

score = score_ethical_factors(product_data, user_values)
```

### Agent Architecture

```
EthicalConsumptionAgent
├── assess_ethical_values()     # Interactive values quiz
├── analyze_purchase_history()  # Historical ethical scoring  
├── search_ethical_products()   # Product search with scoring
├── trace_supply_chain()        # Supply chain transparency
└── generate_report()           # Comprehensive analysis
```

## 📊 Ethical Scoring System

### Multi-Factor Analysis

Products are scored on 5 key factors:

1. **Environmental Impact** (25% weight)
   - Carbon footprint, renewable energy use
   - Packaging sustainability, recyclability
   - Organic/eco-friendly certifications

2. **Labor Practices** (25% weight)  
   - Fair wages, worker rights
   - Safe working conditions
   - Fair Trade certifications

3. **Supply Chain Transparency** (20% weight)
   - Visibility into supplier tiers
   - Public reporting on practices
   - Third-party audits

4. **Corporate Transparency** (15% weight)
   - B-Corp certification
   - Public sustainability commitments
   - ESG reporting

5. **Ethical Certifications** (15% weight)
   - Third-party certifications
   - Industry standards compliance
   - Ethical sourcing verification

### User Preference Weighting

Scores are adjusted based on individual user values:

```python
# User prioritizes environment (5/5) and labor (4/5)
user_values = {
    "environmental_importance": 5,
    "labor_practices_importance": 4,
    "transparency_importance": 3
}

# Score calculation applies user preference multipliers
final_score = base_score * user_preference_multiplier
```

## 🌐 Supply Chain Tracing

### Data Sources

- **Manufacturer Information**: Company registration, location data
- **Certification Databases**: Fair Trade, B-Corp, organic certifications  
- **Labor Audits**: SA8000, WRAP, company audit reports
- **Environmental Data**: Carbon footprint, renewable energy usage
- **Transparency Reports**: Public sustainability reporting

### Tracing Process

1. **Extract Product Data**: Scrape manufacturer, model, origin
2. **Follow Links**: Trace manufacturer → suppliers → raw materials
3. **Cross-Reference**: Check against certification databases
4. **Score Components**: Rate each supply chain factor
5. **Generate Report**: Comprehensive analysis with concerns/strengths

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/test_ethical_agent.py -v

# Run specific test class
pytest tests/test_ethical_agent.py::TestEthicalConsumptionAgent -v

# Run with coverage
pytest tests/test_ethical_agent.py --cov=hushh_mcp.agents.ethical_consumption_agent
```

### Test Coverage

- ✅ Consent token validation and revocation
- ✅ Data encryption/decryption roundtrip
- ✅ Ethical scoring algorithms
- ✅ Supply chain analysis
- ✅ CLI interface functionality
- ✅ Error handling and edge cases

## 🔧 Development

### Adding New Ethical Factors

1. **Update Scoring Operon**:
```python
# In score_ethical_factors.py
def score_ethical_factors(product_data, user_values, weights=None):
    # Add new factor scoring logic
    scores["new_factor"] = calculate_new_factor_score(product_data)
```

2. **Update Assessment Quiz**:
```python
# In assess_ethical_values.py
questions.append(("New ethical factor importance", "new_factor_importance"))
```

3. **Update Agent Manifest**:
```python
# In manifest.py
manifest["scopes"].append("custom.new_factor")
```

### Extending to New Data Sources

```python
class EthicalDataSource:
    def fetch_certification_data(self, product_id):
        # Implement new data source integration
        pass
    
    def validate_labor_practices(self, manufacturer):
        # Add new verification methods
        pass
```

## 📈 Performance

### Benchmarks

- **Values Assessment**: < 30 seconds (interactive)
- **Purchase Analysis**: ~2-5 seconds (100 transactions)  
- **Product Search**: ~3-8 seconds (50 products analyzed)
- **Supply Chain Trace**: ~5-15 seconds (depends on links)
- **Report Generation**: ~1-3 seconds

### Optimizations

- **Caching**: Encrypted supply chain data cached locally
- **Async Operations**: Parallel API calls for product data
- **Incremental Analysis**: Only analyze new transactions
- **Batch Processing**: Group similar products for efficiency

## 🤝 Contributing

### Code Style

- Follow HushhMCP consent-first patterns
- Use type hints for all function parameters
- Add docstrings for public methods
- Include comprehensive tests for new features

### Submission Guidelines

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/new-ethical-factor`
3. **Implement** with tests and documentation
4. **Test** consent flows and encryption
5. **Submit** pull request with clear description

## 📜 License

This project is part of the HushhMCP framework and follows the same open-source license. All contributions become part of the MIT-licensed codebase.

---

Build AI agents that help users consume more ethically.  
**Build with consent. Build with purpose.** 