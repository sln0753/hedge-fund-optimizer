"""
Structured Bond Monthly Coupon Forecast
Based on SBERBCMI Index forecast Nov 2025 - Oct 2026
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import pandas as pd

def show_structured_bond_forecast():
    """Display monthly coupon forecast for structured bond"""
    
    optimizer = DynamicPortfolioOptimizer()
    
    print("="*100)
    print("СТРУКТУРНАЯ ОБЛИГАЦИЯ СБЕР - ПРОГНОЗ МЕСЯЧНЫХ КУПОНОВ")
    print("SBERBANK STRUCTURED BOND - MONTHLY COUPON FORECAST")
    print("="*100)
    
    # Get structured bond data
    struct_bond = optimizer.instruments['Структурная облигация Сбер']
    coupon_forecast = struct_bond['coupon_forecast']
    
    print("\n📊 Источник: Индекс SBERBCMI (Sberbank-CIB)")
    print("Период: Ноябрь 2025 - Октябрь 2026 (12 месяцев)")
    print("\n" + "="*100)
    
    # Monthly coupon table
    months = [
        ('Ноябрь 2025', 'November 2025'),
        ('Декабрь 2025', 'December 2025'),
        ('Январь 2026', 'January 2026'),
        ('Февраль 2026', 'February 2026'),
        ('Март 2026', 'March 2026'),
        ('Апрель 2026', 'April 2026'),
        ('Май 2026', 'May 2026'),
        ('Июнь 2026', 'June 2026'),
        ('Июль 2026', 'July 2026'),
        ('Август 2026', 'August 2026'),
        ('Сентябрь 2026', 'September 2026'),
        ('Октябрь 2026', 'October 2026')
    ]
    
    monthly_data = []
    cumulative = 0
    
    for i, ((month_ru, month_en), coupon_pct) in enumerate(zip(months, coupon_forecast), 1):
        cumulative += coupon_pct
        monthly_data.append({
            '№': i,
            'Месяц': month_ru,
            'Купон (% в месяц)': f"{coupon_pct:.2f}%",
            'Накопительно': f"{cumulative:.2f}%"
        })
    
    df_monthly = pd.DataFrame(monthly_data)
    print("\nПОМЕСЯЧНЫЙ ГРАФИК ВЫПЛАТ:")
    print(df_monthly.to_string(index=False))
    
    # Statistics
    avg_monthly = sum(coupon_forecast) / len(coupon_forecast)
    min_monthly = min(coupon_forecast)
    max_monthly = max(coupon_forecast)
    total_annual = sum(coupon_forecast)
    
    print(f"\n{'='*100}")
    print("СТАТИСТИКА:")
    print(f"{'='*100}")
    print(f"Средний месячный купон:  {avg_monthly:.2f}%")
    print(f"Минимальный купон:       {min_monthly:.2f}% (Май 2026)")
    print(f"Максимальный купон:      {max_monthly:.2f}% (Январь 2026)")
    print(f"Общий годовой доход:     {total_annual:.2f}%")
    print(f"{'='*100}")
    
    # Example calculation on 800K investment
    print(f"\n{'='*100}")
    print("ПРИМЕР РАСЧЕТА НА ИНВЕСТИЦИЮ 800,000 руб:")
    print(f"{'='*100}\n")
    
    investment = 800000
    print(f"Сумма инвестиций: {investment:,.0f} руб\n")
    
    payment_data = []
    total_gross = 0
    total_tax = 0
    total_net = 0
    
    for i, ((month_ru, _), coupon_pct) in enumerate(zip(months, coupon_forecast), 1):
        gross_payment = investment * coupon_pct / 100
        tax_payment = gross_payment * 0.13  # 13% НДФЛ
        net_payment = gross_payment - tax_payment
        
        total_gross += gross_payment
        total_tax += tax_payment
        total_net += net_payment
        
        payment_data.append({
            'Месяц': month_ru,
            'Купон %': f"{coupon_pct:.2f}%",
            'Выплата брутто': f"{gross_payment:,.0f} руб",
            'Налог (13%)': f"{tax_payment:,.0f} руб",
            'Выплата нетто': f"{net_payment:,.0f} руб"
        })
    
    df_payments = pd.DataFrame(payment_data)
    print(df_payments.to_string(index=False))
    
    print(f"\n{'='*100}")
    print("ИТОГИ ЗА ГОД:")
    print(f"{'='*100}")
    print(f"Общая выплата (брутто):  {total_gross:>15,.0f} руб  ({total_gross/investment*100:.2f}%)")
    print(f"Налог (13% НДФЛ):        {total_tax:>15,.0f} руб")
    print(f"Чистая выплата (нетто):  {total_net:>15,.0f} руб  ({total_net/investment*100:.2f}%)")
    print(f"Средняя выплата в месяц: {total_net/12:>15,.0f} руб")
    print(f"{'='*100}")
    
    # Visual representation
    print(f"\n{'='*100}")
    print("ВИЗУАЛИЗАЦИЯ МЕСЯЧНЫХ КУПОНОВ:")
    print(f"{'='*100}\n")
    
    max_bar_length = 50
    for month_ru, coupon_pct in zip([m[0] for m in months], coupon_forecast):
        bar_length = int((coupon_pct / max_monthly) * max_bar_length)
        bar = '█' * bar_length
        print(f"{month_ru:20s} {coupon_pct:>5.2f}% {bar}")
    
    print(f"\n{'='*100}")
    print("КЛЮЧЕВЫЕ ОСОБЕННОСТИ:")
    print(f"{'='*100}")
    print("""
✅ ПЕРЕМЕННЫЕ КУПОНЫ - каждый месяц разный размер
✅ ПРИВЯЗКА К ИНДЕКСУ - SBERBCMI (Sberbank-CIB)
✅ ЕЖЕМЕСЯЧНЫЕ ВЫПЛАТЫ - денежный поток каждый месяц
✅ ПРОГНОЗИРУЕМО - есть официальный прогноз
⚠️ НЕ ГАРАНТИРОВАНО - фактические купоны могут отличаться

Источники данных:
• Индекс выбора облигаций: https://indices.sberbank-cib.com/?indexid=SBERBCPI
• Индекс денежной компоненты: https://indices.sberbank-cib.com/?indexid=SBERBCMI
""")
    print(f"{'='*100}")
    
    print("\n✅ Прогноз по структурной облигации сформирован")
    print(f"{'='*100}\n")

if __name__ == "__main__":
    show_structured_bond_forecast()

