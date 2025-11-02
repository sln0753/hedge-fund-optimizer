"""
Quick Demo of Portfolio Optimizer
This script demonstrates key features without requiring interactive input
"""

from portfolio_optimizer import DynamicPortfolioOptimizer

def run_demo():
    print("\n" + "="*80)
    print("HEDGE FUND PORTFOLIO OPTIMIZER - QUICK DEMO")
    print("="*80)
    
    # Create optimizer
    optimizer = DynamicPortfolioOptimizer()
    
    print("\n🎯 Portfolio Parameters:")
    print(f"   Initial capital (RUB): {optimizer.initial_capital_rub:,.0f} руб")
    print(f"   Initial capital (USD): ${optimizer.initial_usd_amount:,.0f}")
    print(f"   Current USD/RUB rate: {optimizer.current_usd_rub}")
    print(f"   Total capital: {optimizer.initial_capital_rub + optimizer.initial_usd_amount * optimizer.current_usd_rub:,.0f} руб")
    print(f"   Target monthly income: {optimizer.monthly_income_target:,.0f} руб")
    print(f"   Planning horizon: {optimizer.years} years")
    
    print("\n📊 Available Investment Instruments:")
    print("\n   Ruble Instruments:")
    for name, data in optimizer.instruments.items():
        if data['currency'] == 'RUB':
            tax_status = "Tax-free" if data.get('tax_free') else "Taxable"
            print(f"   • {name}: {data['yield']}% yield, {data['type']}, {tax_status}")
    
    print("\n   USD Instruments:")
    for name, data in optimizer.instruments.items():
        if data['currency'] == 'USD':
            tax_status = "Tax-free" if data.get('tax_free') else "Taxable"
            print(f"   • {name}: {data['yield']}% yield, {data['type']}, {tax_status}")
    
    # Demo 1: Base scenario
    print("\n" + "="*80)
    print("DEMO 1: BASE SCENARIO OPTIMIZATION")
    print("="*80)
    optimizer.generate_recommendations(
        capital_growth_scenario='constant',
        rate_scenario='base',
        fx_scenario='base'
    )
    
    # Demo 2: Pessimistic scenario
    print("\n" + "="*80)
    print("DEMO 2: PESSIMISTIC SCENARIO (High rates, weak ruble)")
    print("="*80)
    optimizer.generate_recommendations(
        capital_growth_scenario='constant',
        rate_scenario='pessimistic',
        fx_scenario='pessimistic'
    )
    
    # Demo 3: Scenario comparison
    print("\n" + "="*80)
    print("DEMO 3: COMPREHENSIVE SCENARIO COMPARISON")
    print("="*80)
    optimizer.compare_scenarios()
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("\n✅ The portfolio optimizer is fully functional!")
    print("\n📖 For interactive usage, run:")
    print("   python portfolio_optimizer.py")
    print("\n📚 For documentation, see README.md")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_demo()

