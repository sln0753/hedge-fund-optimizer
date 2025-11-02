"""
Investment Distribution Report
Shows detailed allocation of capital across all instruments
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import pandas as pd

def generate_investment_distribution():
    """Generate detailed investment distribution report"""
    
    optimizer = DynamicPortfolioOptimizer()
    
    print("="*100)
    print("РАСПРЕДЕЛЕНИЕ ИНВЕСТИЦИЙ ПО ИНСТРУМЕНТАМ")
    print("INVESTMENT DISTRIBUTION BY INSTRUMENTS")
    print("="*100)
    
    # Get optimal portfolio
    print("\nРасчет оптимального портфеля с реальными прогнозами...")
    optimal_weights = optimizer.optimize_portfolio('constant', 'base', 'base')
    
    # Calculate total capital
    total_capital_rub = optimizer.initial_capital_rub
    total_capital_usd = optimizer.initial_usd_amount
    total_capital = total_capital_rub + total_capital_usd * optimizer.current_usd_rub
    
    print(f"\n{'='*100}")
    print("ИСХОДНЫЙ КАПИТАЛ:")
    print(f"{'='*100}")
    print(f"Рублевый капитал:     {total_capital_rub:>15,.0f} руб")
    print(f"Валютный капитал:     {total_capital_usd:>15,.0f} USD (× {optimizer.current_usd_rub} = {total_capital_usd * optimizer.current_usd_rub:,.0f} руб)")
    print(f"{'-'*100}")
    print(f"ОБЩИЙ КАПИТАЛ:        {total_capital:>15,.0f} руб")
    print(f"{'='*100}")
    
    # Prepare detailed allocation data
    allocation_data = []
    rub_total = 0
    usd_total = 0
    
    for instrument, weight in sorted(optimal_weights.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.001:  # Only significant allocations
            instrument_info = optimizer.instruments[instrument]
            
            # Capital allocated
            capital_allocated = total_capital * weight
            
            # Currency-specific formatting
            if instrument_info['currency'] == 'USD':
                capital_in_usd = capital_allocated / optimizer.current_usd_rub
                capital_display = f"${capital_in_usd:,.0f}"
                capital_rub_equiv = f"({capital_allocated:,.0f} руб)"
                usd_total += capital_allocated
            else:
                capital_display = f"{capital_allocated:,.0f} руб"
                capital_rub_equiv = ""
                rub_total += capital_allocated
            
            # Calculate after-tax yield
            base_yield = instrument_info['yield']
            adjusted_yield = optimizer.calculate_after_tax_yield(
                instrument, base_yield, 0, 'base'
            )
            
            allocation_data.append({
                'Инструмент': instrument,
                'Тип': instrument_info['type'],
                'Доля': f"{weight*100:.2f}%",
                'Сумма инвестиций': capital_display,
                'Эквивалент': capital_rub_equiv,
                'Валюта': instrument_info['currency'],
                'Доходность': f"{base_yield:.2f}%",
                'После налогов': f"{adjusted_yield:.2f}%",
                'Риск': instrument_info.get('risk', 'низкий'),
                'Ликвидность': instrument_info.get('liquidity', 'высокая'),
                'weight': weight,
                'capital_rub': capital_allocated
            })
    
    # Display full allocation table
    print(f"\n{'='*100}")
    print("ПОЛНОЕ РАСПРЕДЕЛЕНИЕ ИНВЕСТИЦИЙ:")
    print(f"{'='*100}\n")
    
    df = pd.DataFrame(allocation_data)
    display_cols = ['Инструмент', 'Доля', 'Сумма инвестиций', 'Эквивалент', 
                    'Тип', 'Доходность', 'После налогов', 'Риск']
    print(df[display_cols].to_string(index=False))
    
    # Summary by currency
    print(f"\n{'='*100}")
    print("РАСПРЕДЕЛЕНИЕ ПО ВАЛЮТАМ:")
    print(f"{'='*100}")
    print(f"Рублевые инструменты: {rub_total:>15,.0f} руб ({rub_total/total_capital*100:>5.1f}%)")
    print(f"Валютные инструменты: {usd_total:>15,.0f} руб ({usd_total/total_capital*100:>5.1f}%) = ${usd_total/optimizer.current_usd_rub:,.0f}")
    print(f"{'-'*100}")
    print(f"ИТОГО:                {total_capital:>15,.0f} руб (100.0%)")
    print(f"{'='*100}")
    
    # Summary by instrument type
    print(f"\n{'='*100}")
    print("РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ИНСТРУМЕНТОВ:")
    print(f"{'='*100}\n")
    
    type_summary = {}
    for item in allocation_data:
        inst_type = item['Тип']
        if inst_type not in type_summary:
            type_summary[inst_type] = {
                'capital': 0,
                'count': 0,
                'instruments': []
            }
        type_summary[inst_type]['capital'] += item['capital_rub']
        type_summary[inst_type]['count'] += 1
        type_summary[inst_type]['instruments'].append(item['Инструмент'])
    
    type_data = []
    for inst_type, data in sorted(type_summary.items(), key=lambda x: x[1]['capital'], reverse=True):
        type_data.append({
            'Тип': inst_type,
            'Количество': data['count'],
            'Сумма': f"{data['capital']:,.0f} руб",
            'Доля': f"{data['capital']/total_capital*100:.1f}%",
            'Инструменты': ', '.join(data['instruments'][:2]) + ('...' if len(data['instruments']) > 2 else '')
        })
    
    df_types = pd.DataFrame(type_data)
    print(df_types.to_string(index=False))
    
    # Summary by risk level
    print(f"\n{'='*100}")
    print("РАСПРЕДЕЛЕНИЕ ПО УРОВНЮ РИСКА:")
    print(f"{'='*100}\n")
    
    risk_summary = {}
    for item in allocation_data:
        risk = item['Риск']
        if risk not in risk_summary:
            risk_summary[risk] = 0
        risk_summary[risk] += item['capital_rub']
    
    risk_data = []
    for risk, capital in sorted(risk_summary.items(), key=lambda x: x[1], reverse=True):
        risk_data.append({
            'Уровень риска': risk.capitalize(),
            'Сумма': f"{capital:,.0f} руб",
            'Доля портфеля': f"{capital/total_capital*100:.1f}%"
        })
    
    df_risk = pd.DataFrame(risk_data)
    print(df_risk.to_string(index=False))
    
    # Top 5 allocations
    print(f"\n{'='*100}")
    print("ТОП-5 КРУПНЕЙШИХ ПОЗИЦИЙ:")
    print(f"{'='*100}\n")
    
    top5 = allocation_data[:5]
    for i, item in enumerate(top5, 1):
        print(f"{i}. {item['Инструмент']:35s} - {item['Доля']:>6s} - {item['Сумма инвестиций']:>15s} {item['Эквивалент']}")
    
    cumulative_top5 = sum([item['weight'] for item in top5])
    print(f"\nКонцентрация в топ-5: {cumulative_top5*100:.1f}% портфеля")
    
    # Tax efficiency analysis
    print(f"\n{'='*100}")
    print("АНАЛИЗ НАЛОГОВОЙ ЭФФЕКТИВНОСТИ:")
    print(f"{'='*100}\n")
    
    tax_free_capital = 0
    taxable_capital = 0
    
    for item in allocation_data:
        instrument = item['Инструмент']
        if optimizer.instruments[instrument]['tax_free']:
            tax_free_capital += item['capital_rub']
        else:
            taxable_capital += item['capital_rub']
    
    print(f"Инструменты без налогов (ОФЗ):  {tax_free_capital:>15,.0f} руб ({tax_free_capital/total_capital*100:>5.1f}%)")
    print(f"Налогооблагаемые инструменты:   {taxable_capital:>15,.0f} руб ({taxable_capital/total_capital*100:>5.1f}%)")
    print(f"\n💡 Налоговая экономия за счет ОФЗ: ~{tax_free_capital * 0.15 * 0.13:,.0f} руб/год")
    
    # Diversification metrics
    print(f"\n{'='*100}")
    print("МЕТРИКИ ДИВЕРСИФИКАЦИИ:")
    print(f"{'='*100}\n")
    
    # Herfindahl index (concentration)
    herfindahl = sum([item['weight']**2 for item in allocation_data])
    
    print(f"Количество инструментов:        {len(allocation_data)}")
    print(f"Индекс концентрации (Herfindahl): {herfindahl:.4f}")
    print(f"Эквивалент равного распределения: {1/herfindahl:.1f} инструментов")
    
    if herfindahl < 0.15:
        diversification = "Отлично диверсифицирован ✅"
    elif herfindahl < 0.25:
        diversification = "Хорошо диверсифицирован ✅"
    else:
        diversification = "Умеренная диверсификация ⚠️"
    
    print(f"Оценка: {diversification}")
    
    # Liquidity analysis
    print(f"\n{'='*100}")
    print("АНАЛИЗ ЛИКВИДНОСТИ:")
    print(f"{'='*100}\n")
    
    liquidity_summary = {}
    for item in allocation_data:
        instrument = item['Инструмент']
        liquidity = optimizer.instruments[instrument].get('liquidity', 'высокая')
        if liquidity not in liquidity_summary:
            liquidity_summary[liquidity] = 0
        liquidity_summary[liquidity] += item['capital_rub']
    
    liquidity_data = []
    for liquidity, capital in sorted(liquidity_summary.items(), 
                                     key=lambda x: {'высокая': 3, 'средняя': 2, 'низкая': 1}.get(x[0], 0), 
                                     reverse=True):
        liquidity_data.append({
            'Ликвидность': liquidity.capitalize(),
            'Сумма': f"{capital:,.0f} руб",
            'Доля': f"{capital/total_capital*100:.1f}%"
        })
    
    df_liquidity = pd.DataFrame(liquidity_data)
    print(df_liquidity.to_string(index=False))
    
    # Summary chart (ASCII)
    print(f"\n{'='*100}")
    print("ВИЗУАЛИЗАЦИЯ РАСПРЕДЕЛЕНИЯ (по типам):")
    print(f"{'='*100}\n")
    
    for type_item in type_data:
        bar_length = int(float(type_item['Доля'].rstrip('%')) / 2)
        bar = '█' * bar_length
        print(f"{type_item['Тип']:25s} {type_item['Доля']:>6s} {bar}")
    
    print(f"\n{'='*100}")
    print("✅ Отчет о распределении инвестиций сформирован")
    print(f"{'='*100}\n")

if __name__ == "__main__":
    generate_investment_distribution()

