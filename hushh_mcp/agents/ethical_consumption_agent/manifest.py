manifest = {
    "id": "ethical_consumption_agent",
    "name": "Ethical Consumption Agent", 
    "description": "Empowers users to make ethical purchasing decisions by analyzing consumption patterns, scoring products on ethical/environmental factors, and providing supply chain transparency while maintaining complete data privacy.",
    "scopes": [
        "vault.read.email",
        "vault.read.finance", 
        "agent.shopping.purchase",
        "custom.ethical.values",
        "custom.supply.chain"
    ],
    "version": "0.1.0",
    "author": "Team EthicalConsume",
    "consent_required": True,
    "data_encryption": True,
    "categories": ["shopping", "ethics", "environment", "supply_chain"],
    "supported_platforms": ["cli"],
    "dependencies": [
        "requests>=2.32.3",
        "beautifulsoup4>=4.12.0", 
        "pandas>=2.0.0",
        "typer>=0.9.0"
    ]
} 