import typer
from typing import Optional
import json

from hushh_mcp.consent.token import issue_token
from hushh_mcp.constants import ConsentScope
from .index import EthicalConsumptionAgent

app = typer.Typer(help="🌱 Ethical Consumption Agent - Make ethical purchasing decisions with privacy")

@app.command()
def quiz(
    user_id: str = typer.Option(..., "--user", "-u", help="Your user ID"),
    interactive: bool = typer.Option(True, "--interactive/--batch", help="Interactive quiz mode")
):
    """
    🌱 Assess your ethical values and preferences
    """
    try:
        # Issue consent token for values assessment
        token = issue_token(user_id, "ethical_consumption_agent", ConsentScope.CUSTOM_ETHICAL_VALUES)
        
        agent = EthicalConsumptionAgent()
        result = agent.assess_ethical_values(user_id, token.token)
        
        if result["status"] == "success":
            typer.echo("✅ " + result["message"])
            typer.echo(f"📊 Summary: {result['summary']}")
        else:
            typer.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except PermissionError as e:
        typer.echo(f"🔒 Permission denied: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)

@app.command()
def analyze(
    user_id: str = typer.Option(..., "--user", "-u", help="Your user ID"),
    period: str = typer.Option("last_6_months", "--period", "-p", help="Analysis period"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json")
):
    """
    📊 Analyze your purchase history for ethical insights
    """
    try:
        # Issue consent token for email/finance access
        token = issue_token(user_id, "ethical_consumption_agent", ConsentScope.VAULT_READ_EMAIL)
        
        agent = EthicalConsumptionAgent()
        result = agent.analyze_purchase_history(user_id, token.token, period)
        
        if result["status"] == "success":
            analysis = result["analysis"]
            
            if format == "json":
                typer.echo(json.dumps(analysis, indent=2))
            else:
                # Pretty table format
                typer.echo(f"\n📊 Your Ethical Consumption Report ({period})")
                typer.echo("=" * 50)
                typer.echo(f"Ethical Score: {analysis['ethical_score']}/10 📈 (+{analysis['improvement_vs_last_period']['ethical']})")
                typer.echo(f"Eco Score: {analysis['eco_score']}/10 🌱 (+{analysis['improvement_vs_last_period']['eco']})")
                typer.echo(f"Total Purchases: {analysis['total_purchases']}")
                
                typer.echo("\n🔍 Top Issues Found:")
                for issue in analysis['top_issues']:
                    typer.echo(f"  • {issue}")
                
                typer.echo("\n💡 Recommendations:")
                for rec in analysis['recommendations']:
                    typer.echo(f"  • {rec}")
                    
        else:
            typer.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except PermissionError as e:
        typer.echo(f"🔒 Permission denied: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)

@app.command()
def search(
    query: str = typer.Argument(..., help="Product to search for"),
    user_id: str = typer.Option(..., "--user", "-u", help="Your user ID"),
    budget: Optional[int] = typer.Option(None, "--budget", "-b", help="Maximum budget"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json")
):
    """
    🔍 Search for products with ethical analysis
    """
    try:
        # Issue consent token for shopping access
        token = issue_token(user_id, "ethical_consumption_agent", ConsentScope.AGENT_SHOPPING_PURCHASE)
        
        agent = EthicalConsumptionAgent()
        result = agent.search_ethical_products(user_id, token.token, query, budget)
        
        if result["status"] == "success":
            results = result["results"]
            
            if format == "json":
                typer.echo(json.dumps(results, indent=2))
            else:
                # Pretty table format
                typer.echo(f"\n🔍 Ethical Product Search: '{query}'")
                if budget:
                    typer.echo(f"💰 Budget: ${budget}")
                typer.echo(f"📊 Analyzed {results['total_options_analyzed']} options")
                typer.echo("=" * 60)
                
                typer.echo("\n🏆 Best Ethical Choices:")
                for i, rec in enumerate(results['recommendations'], 1):
                    typer.echo(f"\n{i}. {rec['name']} - ${rec['price']}")
                    typer.echo(f"   ✅ Ethical Score: {rec['ethical_score']}/10")
                    typer.echo(f"   🌱 Eco Score: {rec['eco_score']}/10")
                    typer.echo(f"   🏷️  Certifications: {', '.join(rec['certifications'])}")
                    typer.echo(f"   💪 Strengths: {', '.join(rec['strengths'])}")
                    typer.echo(f"   🔗 Source: {rec['source']}")
                
                # Show mainstream comparison
                mainstream = results['mainstream_comparison']
                typer.echo(f"\n⚠️  Popular Choice (for comparison):")
                typer.echo(f"   {mainstream['name']} - ${mainstream['price']}")
                typer.echo(f"   ❌ Ethical Score: {mainstream['ethical_score']}/10")
                typer.echo(f"   ❌ Eco Score: {mainstream['eco_score']}/10")
                typer.echo(f"   ⚠️  Issues: {', '.join(mainstream['issues'])}")
                    
        else:
            typer.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except PermissionError as e:
        typer.echo(f"🔒 Permission denied: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)

@app.command()
def trace(
    product_url: str = typer.Argument(..., help="Product URL to trace"),
    user_id: str = typer.Option(..., "--user", "-u", help="Your user ID"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json")
):
    """
    🔗 Trace supply chain for a specific product
    """
    try:
        # Issue consent token for supply chain access
        token = issue_token(user_id, "ethical_consumption_agent", ConsentScope.CUSTOM_SUPPLY_CHAIN)
        
        agent = EthicalConsumptionAgent()
        result = agent.trace_supply_chain(user_id, token.token, product_url)
        
        if result["status"] == "success":
            trace = result["supply_chain_analysis"]
            
            if format == "json":
                typer.echo(json.dumps(trace, indent=2))
            else:
                # Pretty table format
                supply_chain = trace['supply_chain']
                typer.echo(f"\n🔗 Supply Chain Analysis")
                typer.echo("=" * 50)
                typer.echo(f"Manufacturer: {supply_chain['manufacturer']}")
                typer.echo(f"Location: {supply_chain['manufacturing_location']}")
                typer.echo(f"Overall Score: {trace['overall_supply_chain_score']}/10")
                
                typer.echo(f"\n🌍 Raw Materials Origin:")
                for origin in supply_chain['raw_materials_origin']:
                    typer.echo(f"  • {origin}")
                
                typer.echo(f"\n🏷️ Certifications:")
                for cert in supply_chain['labor_certifications'] + supply_chain['environmental_certifications']:
                    typer.echo(f"  • {cert}")
                
                typer.echo(f"\n⚠️ Ethical Concerns:")
                for concern in trace['ethical_concerns']:
                    typer.echo(f"  • {concern}")
                
                typer.echo(f"\n✅ Positive Factors:")
                for factor in trace['positive_factors']:
                    typer.echo(f"  • {factor}")
                    
        else:
            typer.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except PermissionError as e:
        typer.echo(f"🔒 Permission denied: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)

@app.command()
def report(
    user_id: str = typer.Option(..., "--user", "-u", help="Your user ID"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json")
):
    """
    📋 Generate comprehensive ethical consumption report
    """
    try:
        # Issue consent token for comprehensive access
        token = issue_token(user_id, "ethical_consumption_agent", ConsentScope.VAULT_READ_EMAIL)
        
        agent = EthicalConsumptionAgent()
        result = agent.generate_report(user_id, token.token)
        
        if result["status"] == "success":
            report_data = result["report"]
            
            if format == "json":
                typer.echo(json.dumps(report_data, indent=2))
            else:
                # Pretty table format
                typer.echo(f"\n📋 Comprehensive Ethical Consumption Report")
                typer.echo(f"📅 Report Date: {report_data['report_date']}")
                typer.echo("=" * 60)
                
                typer.echo(f"\n📈 Score Trends:")
                typer.echo(f"Ethical Scores: {' → '.join(map(str, report_data['ethical_score_trend']))}")
                typer.echo(f"Eco Scores: {' → '.join(map(str, report_data['eco_score_trend']))}")
                
                typer.echo(f"\n🏆 Top Achievements:")
                for achievement in report_data['top_achievements']:
                    typer.echo(f"  • {achievement}")
                
                typer.echo(f"\n🎯 Areas for Improvement:")
                for area in report_data['areas_for_improvement']:
                    typer.echo(f"  • {area}")
                
                typer.echo(f"\n💡 Personalized Recommendations:")
                for rec in report_data['personalized_recommendations']:
                    typer.echo(f"  • {rec}")
                    
        else:
            typer.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except PermissionError as e:
        typer.echo(f"🔒 Permission denied: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 