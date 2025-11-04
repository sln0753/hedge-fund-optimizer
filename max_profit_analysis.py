"""
Maximum Profit Analysis
Simple analytical approach to find profit-maximizing allocation
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import pandas as pd

def analyze_max_profit():
    """Анализ максимизации прибыли для разных горизонтов"""
    
    optimizer = DynamicPortfolioOptimizer()
    
    print("="*100)
    print("АНАЛИЗ МАКСИМИЗАЦИИ ПРИБЫЛИ")
    print("MAXIMUM PROFIT ANALYSIS")
    print("="*100)
    
    total_capital = optimizer.initial_capital_rub + optimizer.initial_usd_amount * optimizer.current_usd_rub
    
    print(f"\nИсходный капитал: {total_capital:,.0f} руб")
    print(f"Сценарий: Базовый (CBR: 16.5%→12.0%, USD/RUB: 81.17→92.00)")
    
    # Рассчитываем доходность каждого инструмента по годам
    print(f"\n{'='*100}")
    print("ДОХОДНОСТЬ ИНСТРУМЕНТОВ ПО ГОДАМ (после налогов):")
    print(f"{'='*100}\n")
    
    instruments_performance = {}
    
    for instrument, data in optimizer.instruments.items():
        yearly_yields = []
        for year in range(3):
            base_yield = data['yield']
            adjusted_yield = optimizer.calculate_after_tax_yield(
                instrument, base_yield, year, 'base'
            )
            yearly_yields.append(adjusted_yield)
        
        instruments_performance[instrument] = yearly_yields
        
        print(f"{instrument}:")
        print(f"  Год 1: {yearly_yields[0]:.2f}%")
        print(f"  Год 2: {yearly_yields[1]:.2f}%")
        print(f"  Год 3: {yearly_yields[2]:.2f}%")
        print(f"  Средняя: {sum(yearly_yields)/3:.2f}%")
        print(f"  Налог: {'0%' if data.get('tax_free') else '13%'}")
        print()
    
    # Анализ для разных горизонтов
    print(f"{'='*100}")
    print("ОПТИМАЛЬНЫЕ СТРАТЕГИИ ДЛЯ МАКСИМИЗАЦИИ ПРИБЫЛИ:")
    print(f"{'='*100}\n")
    
    scenarios_results = []
    
    # Сценарий 1: Максимизация прибыли за 1 год
    print("1️⃣  ГОРИЗОНТ: 1 ГОД (максимизация прибыли за год 1)")
    print("-" * 100)
    
    year1_yields = {inst: perf[0] for inst, perf in instruments_performance.items()}
    best_year1 = max(year1_yields.items(), key=lambda x: x[1])
    
    print(f"Лучший инструмент: {best_year1[0]} ({best_year1[1]:.2f}%)")
    
    # Простая стратегия: максимум в лучший инструмент (с учетом limits)
    allocation_1y = {}
    for inst in optimizer.instruments.keys():
        if inst == best_year1[0]:
            # Максимально возможная доля
            if optimizer.instruments[inst]['risk'] == 'средний':
                allocation_1y[inst] = 0.20  # Структурная: max 20%
            elif optimizer.instruments[inst]['currency'] == 'USD':
                allocation_1y[inst] = 0.40  # USD: max 40%
            else:
                allocation_1y[inst] = 0.50  # Остальные: max 50%
        else:
            allocation_1y[inst] = 0.0
    
    # Распределяем остаток на второй лучший
    remaining = 1.0 - sum(allocation_1y.values())
    if remaining > 0:
        year1_yields_remaining = {k: v for k, v in year1_yields.items() if allocation_1y[k] < 0.5}
        second_best = max(year1_yields_remaining.items(), key=lambda x: x[1])
        allocation_1y[second_best[0]] = remaining
    
    print("\nРаспределение:")
    for inst, weight in sorted(allocation_1y.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"  {inst:40s}: {weight*100:>5.1f}%")
    
    # Расчет прибыли
    sim_1y = optimizer.simulate_portfolio_performance(allocation_1y, 'constant', 'base', 'base', years=1)
    profit_1y = sim_1y[0]['annual_income']
    monthly_1y = sim_1y[0]['monthly_income']
    
    print(f"\nПрибыль за 1 год: {profit_1y:,.0f} руб ({profit_1y/total_capital*100:.2f}%)")
    print(f"Месячный доход: {monthly_1y:,.0f} руб ({monthly_1y/50000*100:.1f}% от цели)")
    
    scenarios_results.append({
        'Горизонт': '1 ГОД',
        'Прибыль': profit_1y,
        '% от капитала': profit_1y/total_capital*100,
        'Мес. доход': monthly_1y,
        'Топ инструмент': best_year1[0],
        'Топ доля': max(allocation_1y.values())*100
    })
    
    # Сценарий 2: Максимизация за 2 года
    print(f"\n{'='*100}")
    print("2️⃣  ГОРИЗОНТ: 2 ГОДА (максимизация суммарной прибыли за 2 года)")
    print("-" * 100)
    
    avg_2y_yields = {inst: (perf[0] + perf[1])/2 for inst, perf in instruments_performance.items()}
    best_2y = max(avg_2y_yields.items(), key=lambda x: x[1])
    
    print(f"Лучший инструмент (средняя за 2 года): {best_2y[0]} ({best_2y[1]:.2f}%)")
    
    allocation_2y = {}
    for inst in optimizer.instruments.keys():
        if inst == best_2y[0]:
            if optimizer.instruments[inst]['risk'] == 'средний':
                allocation_2y[inst] = 0.20
            elif optimizer.instruments[inst]['currency'] == 'USD':
                allocation_2y[inst] = 0.40
            else:
                allocation_2y[inst] = 0.50
        else:
            allocation_2y[inst] = 0.0
    
    remaining = 1.0 - sum(allocation_2y.values())
    if remaining > 0:
        avg_2y_remaining = {k: v for k, v in avg_2y_yields.items() if allocation_2y[k] < 0.5}
        second_best = max(avg_2y_remaining.items(), key=lambda x: x[1])
        allocation_2y[second_best[0]] = remaining
    
    print("\nРаспределение:")
    for inst, weight in sorted(allocation_2y.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"  {inst:40s}: {weight*100:>5.1f}%")
    
    sim_2y = optimizer.simulate_portfolio_performance(allocation_2y, 'constant', 'base', 'base', years=2)
    profit_2y = sum([yr['annual_income'] for yr in sim_2y])
    monthly_2y = profit_2y / 24  # Average over 24 months
    
    print(f"\nПрибыль за 2 года: {profit_2y:,.0f} руб ({profit_2y/total_capital*100:.2f}%)")
    print(f"Средний месячный доход: {monthly_2y:,.0f} руб ({monthly_2y/50000*100:.1f}% от цели)")
    
    scenarios_results.append({
        'Горизонт': '2 ГОДА',
        'Прибыль': profit_2y,
        '% от капитала': profit_2y/total_capital*100,
        'Мес. доход': monthly_2y,
        'Топ инструмент': best_2y[0],
        'Топ доля': max(allocation_2y.values())*100
    })
    
    # Сценарий 3: Максимизация за 3 года
    print(f"\n{'='*100}")
    print("3️⃣  ГОРИЗОНТ: 3 ГОДА (максимизация суммарной прибыли за 3 года)")
    print("-" * 100)
    
    avg_3y_yields = {inst: sum(perf)/3 for inst, perf in instruments_performance.items()}
    best_3y = max(avg_3y_yields.items(), key=lambda x: x[1])
    
    print(f"Лучший инструмент (средняя за 3 года): {best_3y[0]} ({best_3y[1]:.2f}%)")
    
    allocation_3y = {}
    for inst in optimizer.instruments.keys():
        if inst == best_3y[0]:
            if optimizer.instruments[inst]['risk'] == 'средний':
                allocation_3y[inst] = 0.20
            elif optimizer.instruments[inst]['currency'] == 'USD':
                allocation_3y[inst] = 0.40
            else:
                allocation_3y[inst] = 0.50
        else:
            allocation_3y[inst] = 0.0
    
    remaining = 1.0 - sum(allocation_3y.values())
    if remaining > 0:
        avg_3y_remaining = {k: v for k, v in avg_3y_yields.items() if allocation_3y[k] < 0.5}
        second_best = max(avg_3y_remaining.items(), key=lambda x: x[1])
        allocation_3y[second_best[0]] = remaining
    
    print("\nРаспределение:")
    for inst, weight in sorted(allocation_3y.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"  {inst:40s}: {weight*100:>5.1f}%")
    
    sim_3y = optimizer.simulate_portfolio_performance(allocation_3y, 'constant', 'base', 'base', years=3)
    profit_3y = sum([yr['annual_income'] for yr in sim_3y])
    monthly_3y = profit_3y / 36  # Average over 36 months
    
    print(f"\nПрибыль за 3 года: {profit_3y:,.0f} руб ({profit_3y/total_capital*100:.2f}%)")
    print(f"Средний месячный доход: {monthly_3y:,.0f} руб ({monthly_3y/50000*100:.1f}% от цели)")
    
    scenarios_results.append({
        'Горизонт': '3 ГОДА',
        'Прибыль': profit_3y,
        '% от капитала': profit_3y/total_capital*100,
        'Мес. доход': monthly_3y,
        'Топ инструмент': best_3y[0],
        'Топ доля': max(allocation_3y.values())*100
    })
    
    # Финальное сравнение
    print(f"\n{'='*100}")
    print("📊 ФИНАЛЬНОЕ СРАВНЕНИЕ:")
    print(f"{'='*100}\n")
    
    comparison_df = pd.DataFrame(scenarios_results)
    print(comparison_df.to_string(index=False))
    
    print(f"\n{'='*100}")


if __name__ == "__main__":
    try:
        analyze_max_profit()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

