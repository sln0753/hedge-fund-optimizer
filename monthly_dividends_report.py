"""
Monthly Dividend/Income Report for First Year
Shows detailed month-by-month payouts from each instrument
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import pandas as pd

def generate_monthly_dividend_table():
    """Generate detailed monthly dividend payout table for Year 1"""
    
    optimizer = DynamicPortfolioOptimizer()
    
    print("="*100)
    print("МЕСЯЧНЫЕ ВЫПЛАТЫ ДИВИДЕНДОВ / КУПОНОВ - ГОД 1")
    print("MONTHLY DIVIDEND/COUPON PAYMENTS - YEAR 1")
    print("="*100)
    
    # Get optimal portfolio
    print("\nРасчет оптимального портфеля...")
    optimal_weights = optimizer.optimize_portfolio('constant', 'base', 'base')
    
    # Calculate total capital
    total_capital = optimizer.initial_capital_rub + optimizer.initial_usd_amount * optimizer.current_usd_rub
    
    print(f"\nОбщий капитал: {total_capital:,.0f} руб")
    print(f"Целевой месячный доход: {optimizer.monthly_income_target:,.0f} руб\n")
    
    # Prepare instrument details
    instruments_data = []
    
    for instrument, weight in optimal_weights.items():
        if weight > 0.01:  # Only significant allocations
            instrument_info = optimizer.instruments[instrument]
            
            # Calculate after-tax yield for year 0 (current year)
            base_yield = instrument_info['yield']
            adjusted_yield = optimizer.calculate_after_tax_yield(
                instrument, base_yield, 0, 'base'
            )
            
            # Capital allocated to this instrument
            capital_allocated = total_capital * weight
            
            # Annual income from this instrument
            annual_income = capital_allocated * adjusted_yield / 100
            
            # Monthly income (assuming monthly distributions)
            monthly_income = annual_income / 12
            
            # Convert to rubles if USD
            if instrument_info['currency'] == 'USD':
                capital_in_currency = capital_allocated / optimizer.current_usd_rub
                monthly_income_display = f"{monthly_income:,.0f} руб (${monthly_income/optimizer.current_usd_rub:,.0f})"
                capital_display = f"${capital_in_currency:,.0f}"
            else:
                monthly_income_display = f"{monthly_income:,.0f} руб"
                capital_display = f"{capital_allocated:,.0f} руб"
            
            instruments_data.append({
                'Инструмент': instrument,
                'Тип': instrument_info['type'],
                'Капитал': capital_display,
                'Доходность': f"{adjusted_yield:.2f}%",
                'Годовой доход': f"{annual_income:,.0f} руб",
                'Месячный доход': monthly_income_display,
                'Налог': 'Нет' if instrument_info['tax_free'] else 'НДФЛ 13%',
                'monthly_income_rub': monthly_income  # For totals calculation
            })
    
    # Display summary table
    df = pd.DataFrame(instruments_data)
    display_df = df.drop('monthly_income_rub', axis=1)
    
    print("="*100)
    print("РАСПРЕДЕЛЕНИЕ ИНСТРУМЕНТОВ И МЕСЯЧНЫЙ ДОХОД")
    print("="*100)
    print(display_df.to_string(index=False))
    
    # Calculate totals
    total_monthly = sum([item['monthly_income_rub'] for item in instruments_data])
    total_annual = total_monthly * 12
    
    print("\n" + "="*100)
    print("ИТОГИ:")
    print("="*100)
    print(f"Общий месячный доход:  {total_monthly:>15,.0f} руб")
    print(f"Общий годовой доход:   {total_annual:>15,.0f} руб")
    print(f"Целевой месячный доход:{optimizer.monthly_income_target:>15,.0f} руб")
    print(f"Покрытие цели:         {total_monthly/optimizer.monthly_income_target*100:>15.1f}%")
    print("="*100)
    
    # Generate month-by-month table
    print("\n" + "="*100)
    print("ПОМЕСЯЧНАЯ ТАБЛИЦА ВЫПЛАТ - ГОД 1 (2025-2026)")
    print("="*100)
    
    months = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]
    
    monthly_data = []
    cumulative = 0
    
    for i, month in enumerate(months, 1):
        monthly_income = total_monthly
        cumulative += monthly_income
        
        coverage_status = "✅" if monthly_income >= optimizer.monthly_income_target else "⚠️"
        
        monthly_data.append({
            'Месяц': f"{i:2d}. {month}",
            'Доход за месяц': f"{monthly_income:,.0f} руб",
            'Накопительно': f"{cumulative:,.0f} руб",
            'Покрытие цели': f"{monthly_income/optimizer.monthly_income_target*100:.1f}%",
            'Статус': coverage_status
        })
    
    df_monthly = pd.DataFrame(monthly_data)
    print(df_monthly.to_string(index=False))
    
    print("\n" + "="*100)
    print("ДЕТАЛИЗАЦИЯ ПО ТИПАМ ИНСТРУМЕНТОВ:")
    print("="*100)
    
    # Group by instrument type
    type_summary = {}
    for item in instruments_data:
        inst_type = item['Тип']
        if inst_type not in type_summary:
            type_summary[inst_type] = {
                'count': 0,
                'monthly_income': 0,
                'annual_income': 0
            }
        type_summary[inst_type]['count'] += 1
        type_summary[inst_type]['monthly_income'] += item['monthly_income_rub']
        type_summary[inst_type]['annual_income'] += item['monthly_income_rub'] * 12
    
    type_data = []
    for inst_type, data in type_summary.items():
        type_data.append({
            'Тип инструмента': inst_type,
            'Количество': data['count'],
            'Месячный доход': f"{data['monthly_income']:,.0f} руб",
            'Годовой доход': f"{data['annual_income']:,.0f} руб",
            'Доля от дохода': f"{data['monthly_income']/total_monthly*100:.1f}%"
        })
    
    df_types = pd.DataFrame(type_data)
    print(df_types.to_string(index=False))
    
    # Payment schedule insights
    print("\n" + "="*100)
    print("ГРАФИК ВЫПЛАТ ПО ИНСТРУМЕНТАМ:")
    print("="*100)
    
    for item in instruments_data:
        instrument = item['Инструмент']
        inst_type = item['Тип']
        monthly = item['Месячный доход']
        
        if 'ОФЗ' in inst_type:
            frequency = "2 раза в год (купоны раз в полгода)"
        elif 'Депозит' in inst_type:
            frequency = "Ежемесячно (или капитализация)"
        elif 'БПИФ' in inst_type:
            frequency = "Реинвестирование (выплаты при продаже)"
        elif 'Структурная' in inst_type:
            frequency = "Ежемесячно (структурный купон)"
        elif 'Еврооблигация' in inst_type:
            frequency = "Полугодовые купоны"
        else:
            frequency = "По условиям инструмента"
        
        print(f"• {instrument:35s} - {monthly:30s} - {frequency}")
    
    print("\n" + "="*100)
    print("💡 ВАЖНЫЕ ЗАМЕЧАНИЯ:")
    print("="*100)
    print("""
1. ОФЗ (облигации федерального займа):
   - Купоны обычно выплачиваются 2 раза в год
   - В таблице показан средний месячный эквивалент
   - Фактические выплаты будут в даты купонов (обычно раз в полгода)

2. Депозиты:
   - Могут быть с ежемесячными выплатами процентов
   - Или с капитализацией (проценты добавляются к телу вклада)

3. БПИФ (биржевые ПИФы):
   - Доход формируется за счет роста стоимости паев
   - Выплаты при продаже паев, не ежемесячно

4. Структурные облигации:
   - Обычно имеют ежемесячные купоны
   - Размер купона может меняться в зависимости от условий

5. Еврооблигации:
   - Купоны обычно полугодовые
   - Выплаты в валюте (USD), затем конвертация

РЕАЛЬНЫЙ ДЕНЕЖНЫЙ ПОТОК:
- Фактический месячный доход будет неравномерным
- Некоторые месяцы - больше (когда купоны по облигациям)
- Некоторые месяцы - меньше (только проценты по вкладам)
- Средний месячный доход: """ + f"{total_monthly:,.0f} руб" + """
- Рекомендуется создать резервный фонд для сглаживания
""")
    
    print("="*100)
    print("\n✅ Отчет по месячным выплатам сформирован")
    print("="*100)

if __name__ == "__main__":
    generate_monthly_dividend_table()

