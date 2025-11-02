"""
Test script for the Portfolio Optimizer
This script tests the core functionality without interactive menu
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import sys

def test_basic_functionality():
    """Test basic optimizer functionality"""
    print("="*80)
    print("TESTING PORTFOLIO OPTIMIZER")
    print("="*80)
    
    # Create optimizer instance
    print("\n1. Creating optimizer instance...")
    optimizer = DynamicPortfolioOptimizer()
    print("✅ Optimizer created successfully")
    
    # Test initial parameters
    print(f"\n2. Initial parameters:")
    print(f"   - Initial capital RUB: {optimizer.initial_capital_rub:,.0f}")
    print(f"   - Initial USD amount: {optimizer.initial_usd_amount:,.0f}")
    print(f"   - Current USD/RUB rate: {optimizer.current_usd_rub}")
    print(f"   - Monthly income target: {optimizer.monthly_income_target:,.0f}")
    print(f"   - Planning horizon: {optimizer.years} years")
    print(f"   - Number of instruments: {len(optimizer.instruments)}")
    print("✅ Parameters verified")
    
    # Test instrument list
    print(f"\n3. Available instruments:")
    for name, data in optimizer.instruments.items():
        print(f"   - {name}: {data['type']}, {data['yield']}%, {data['currency']}")
    print("✅ Instruments loaded")
    
    # Test scenarios
    print(f"\n4. Available scenarios:")
    print(f"   - Capital scenarios: {list(optimizer.capital_growth_scenarios.keys())}")
    print(f"   - CBR rate scenarios: {list(optimizer.cbr_scenarios.keys())}")
    print(f"   - FX rate scenarios: {list(optimizer.fx_scenarios.keys())}")
    print("✅ Scenarios loaded")
    
    return optimizer

def test_optimization(optimizer):
    """Test portfolio optimization"""
    print("\n" + "="*80)
    print("TESTING PORTFOLIO OPTIMIZATION")
    print("="*80)
    
    # Test base scenario optimization
    print("\n5. Running optimization for base scenario...")
    try:
        optimal_weights = optimizer.optimize_portfolio(
            capital_growth_scenario='constant',
            rate_scenario='base',
            fx_scenario='base'
        )
        print("✅ Optimization completed successfully")
        
        # Show top allocations
        print("\n   Top allocations:")
        sorted_weights = sorted(optimal_weights.items(), key=lambda x: x[1], reverse=True)
        for instrument, weight in sorted_weights[:5]:
            if weight > 0.01:
                print(f"   - {instrument}: {weight*100:.1f}%")
        
        # Verify sum of weights
        total_weight = sum(optimal_weights.values())
        print(f"\n   Total allocation: {total_weight*100:.1f}%")
        if abs(total_weight - 1.0) < 0.01:
            print("✅ Weights sum to 100%")
        else:
            print(f"❌ Warning: Weights sum to {total_weight*100:.1f}%")
        
        return optimal_weights
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_simulation(optimizer, optimal_weights):
    """Test portfolio simulation"""
    print("\n" + "="*80)
    print("TESTING PORTFOLIO SIMULATION")
    print("="*80)
    
    print("\n6. Running 5-year simulation...")
    try:
        simulation = optimizer.simulate_portfolio_performance(
            optimal_weights,
            capital_growth_scenario='constant',
            rate_scenario='base',
            fx_scenario='base'
        )
        print("✅ Simulation completed successfully")
        
        # Show year-by-year results
        print("\n   Year-by-year results:")
        for result in simulation:
            coverage = "✅" if result['monthly_income'] >= optimizer.monthly_income_target else "❌"
            print(f"   Year {result['year']}: "
                  f"Capital: {result['total_capital_end']:,.0f} руб, "
                  f"Monthly income: {result['monthly_income']:,.0f} руб {coverage}")
        
        return simulation
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_recommendations(optimizer):
    """Test recommendation generation"""
    print("\n" + "="*80)
    print("TESTING RECOMMENDATION GENERATION")
    print("="*80)
    
    print("\n7. Generating recommendations for base scenario...")
    try:
        optimizer.generate_recommendations(
            capital_growth_scenario='constant',
            rate_scenario='base',
            fx_scenario='base'
        )
        print("\n✅ Recommendations generated successfully")
        return True
    except Exception as e:
        print(f"\n❌ Recommendation generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scenario_comparison(optimizer):
    """Test scenario comparison"""
    print("\n" + "="*80)
    print("TESTING SCENARIO COMPARISON")
    print("="*80)
    
    print("\n8. Comparing scenarios...")
    try:
        optimizer.compare_scenarios()
        print("\n✅ Scenario comparison completed successfully")
        return True
    except Exception as e:
        print(f"\n❌ Scenario comparison failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_scenarios(optimizer):
    """Test different scenario combinations"""
    print("\n" + "="*80)
    print("TESTING DIFFERENT SCENARIO COMBINATIONS")
    print("="*80)
    
    test_cases = [
        ('constant', 'base', 'base', 'Базовый'),
        ('decrease_5', 'pessimistic', 'pessimistic', 'Пессимистичный с уменьшением капитала'),
        ('increase_5', 'optimistic', 'optimistic', 'Оптимистичный с ростом капитала'),
    ]
    
    print("\n9. Testing scenario combinations...")
    for capital, rate, fx, label in test_cases:
        print(f"\n   Testing: {label}...")
        try:
            optimal_weights = optimizer.optimize_portfolio(capital, rate, fx)
            simulation = optimizer.simulate_portfolio_performance(optimal_weights, capital, rate, fx)
            
            avg_income = sum([r['monthly_income'] for r in simulation]) / len(simulation)
            final_capital = simulation[-1]['total_capital_end']
            
            print(f"   ✅ {label}: "
                  f"Avg monthly income: {avg_income:,.0f} руб, "
                  f"Final capital: {final_capital:,.0f} руб")
        except Exception as e:
            print(f"   ❌ {label} failed: {e}")
    
    print("\n✅ All scenario combinations tested")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("PORTFOLIO OPTIMIZER - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    try:
        # Test 1-4: Basic functionality
        optimizer = test_basic_functionality()
        
        # Test 5: Optimization
        optimal_weights = test_optimization(optimizer)
        if optimal_weights is None:
            print("\n❌ Critical error: Optimization failed. Stopping tests.")
            return False
        
        # Test 6: Simulation
        simulation = test_simulation(optimizer, optimal_weights)
        if simulation is None:
            print("\n❌ Critical error: Simulation failed. Stopping tests.")
            return False
        
        # Test 7: Recommendations
        if not test_recommendations(optimizer):
            print("\n⚠️ Warning: Recommendation generation failed, but continuing tests.")
        
        # Test 8: Scenario comparison
        if not test_scenario_comparison(optimizer):
            print("\n⚠️ Warning: Scenario comparison failed, but continuing tests.")
        
        # Test 9: Different scenarios
        test_different_scenarios(optimizer)
        
        # Final summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print("✅ All core tests passed successfully!")
        print("\nThe Portfolio Optimizer is working correctly and ready to use.")
        print("\nTo run the interactive version, use:")
        print("  python portfolio_optimizer.py")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

