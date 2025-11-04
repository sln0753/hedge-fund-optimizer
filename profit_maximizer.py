"""
Pure Profit Maximization Optimizer
Maximizes total returns over different time horizons
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import numpy as np
from scipy.optimize import minimize
import pandas as pd

class ProfitMaximizer(DynamicPortfolioOptimizer):
    """Optimizer focused on maximizing total profit"""
    
    def optimize_for_max_profit(self, years_horizon, rate_scenario='base', 
                                fx_scenario='base', capital_scenario='constant'):
        """
        Оптимизация для максимизации прибыли за заданный период
        
        Parameters:
        - years_horizon: 1, 2, или 3 года
        - rate_scenario: сценарий ставок ЦБ
        - fx_scenario: сценарий курса валют
        """
        instruments_list = list(self.instruments.keys())
        n_instruments = len(instruments_list)
        
        def objective(weights_array):
            """Максимизация прибыли = минимизация отрицательной прибыли"""
            weights_dict = {instrument: weights_array[i] 
                          for i, instrument in enumerate(instruments_list)}
            
            # Симулируем портфель
            simulation = self.simulate_portfolio_performance(
                weights_dict, capital_scenario, rate_scenario, fx_scenario, years=years_horizon
            )
            
            # Считаем общую прибыль за период
            total_profit = 0
            for year_result in simulation:
                total_profit += year_result['annual_income']
            
            # Минимизируем ОТРИЦАТЕЛЬНУЮ прибыль = максимизируем прибыль!
            return -total_profit
        
        # Ограничения
        constraints = [
            {'type': 'eq', 'fun': lambda x: sum(x) - 1}  # сумма = 1
        ]
        
        # Границы (те же что и раньше)
        bounds = []
        for instrument in instruments_list:
            instrument_data = self.instruments[instrument]
            
            if instrument == 'Структурная облигация Сбер':
                bounds.append((0, 0.2))
            elif instrument_data['currency'] == 'USD':
                bounds.append((0, 0.4))
            elif instrument_data['risk'] == 'низкий':
                bounds.append((0, 0.5))
            else:
                bounds.append((0, 0.4))
        
        # Начальное приближение
        x0 = np.array([1/n_instruments] * n_instruments)
        
        # Оптимизация
        result = minimize(objective, x0, method='SLSQP', 
                         constraints=constraints, bounds=bounds,
                         options={'maxiter': 500, 'ftol': 1e-6})
        
        optimal_weights = result.x if result.success else x0
        optimal_profit = -result.fun if result.success else 0
        
        return {
            'weights': {instrument: optimal_weights[i] for i, instrument in enumerate(instruments_list)},
            'total_profit': optimal_profit,
            'success': result.success
        }


def compare_profit_scenarios():
    """Сравнение оптимизации для 1, 2 и 3 лет"""
    
    print("="*100)
    print("МАКСИМИЗАЦИЯ ПРИБЫЛИ - СРАВНЕНИЕ ГОРИЗОНТОВ")
    print("PROFIT MAXIMIZATION - HORIZON COMPARISON")
    print("="*100)
    
    optimizer = ProfitMaximizer()
    
    # Исходные данные
    total_capital = optimizer.initial_capital_rub + optimizer.initial_usd_amount * optimizer.current_usd_rub
    
    print(f"\nИсходный капитал: {total_capital:,.0f} руб")
    print(f"Целевой месячный доход: {optimizer.monthly_income_target:,.0f} руб")
    print(f"Сценарий ставок: base (CBR: 16.5% → 12.0%)")
    print(f"Сценарий курса: base (USD/RUB: 81.17 → 92.00)")
    
    scenarios = [
        (1, "1 ГОД"),
        (2, "2 ГОДА"),
        (3, "3 ГОДА")
    ]
    
    results_summary = []
    
    for years, label in scenarios:
        print(f"\n{'='*100}")
        print(f"ОПТИМИЗАЦИЯ ДЛЯ МАКСИМИЗАЦИИ ПРИБЫЛИ ЗА {label}")
        print(f"{'='*100}")
        
        # Оптимизируем
        result = optimizer.optimize_for_max_profit(
            years_horizon=years,
            rate_scenario='base',
            fx_scenario='base'
        )
        
        weights = result['weights']
        total_profit = result['total_profit']
        
        # Детальная симуляция
        simulation = optimizer.simulate_portfolio_performance(
            weights, 'constant', 'base', 'base', years=years
        )
        
        # Показываем распределение
        print(f"\n📊 ОПТИМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ (максимизация прибыли за {years} лет):")
        allocation_data = []
        for instrument, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            if weight > 0.01:
                inst_data = optimizer.instruments[instrument]
                amount = total_capital * weight
                allocation_data.append({
                    'Инструмент': instrument,
                    'Доля': f"{weight*100:.1f}%",
                    'Сумма': f"{amount:,.0f} руб" if inst_data['currency'] == 'RUB' else f"${amount/optimizer.current_usd_rub:,.0f}",
                    'Тип': inst_data['type'],
                    'Налог': '0%' if inst_data.get('tax_free') else '13%'
                })
        
        df_allocation = pd.DataFrame(allocation_data)
        print(df_allocation.to_string(index=False))
        
        # Показываем прибыль по годам
        print(f"\n📈 ПРИБЫЛЬ ПО ГОДАМ:")
        yearly_data = []
        cumulative_profit = 0
        for year_result in simulation:
            annual_profit = year_result['annual_income']
            cumulative_profit += annual_profit
            monthly_income = year_result['monthly_income']
            
            yearly_data.append({
                'Год': year_result['year'],
                'Годовая прибыль': f"{annual_profit:,.0f} руб",
                'Месячный доход': f"{monthly_income:,.0f} руб",
                'Накопленная прибыль': f"{cumulative_profit:,.0f} руб",
                'Капитал': f"{year_result['total_capital_end']:,.0f} руб"
            })
        
        df_yearly = pd.DataFrame(yearly_data)
        print(df_yearly.to_string(index=False))
        
        # Итоги
        final_capital = simulation[-1]['total_capital_end']
        profit_pct = (total_profit / total_capital) * 100
        avg_monthly = total_profit / (years * 12)
        
        print(f"\n💰 ИТОГИ ЗА {label}:")
        print(f"{'='*100}")
        print(f"Общая прибыль:           {total_profit:>15,.0f} руб  ({profit_pct:.2f}% от капитала)")
        print(f"Итоговый капитал:        {final_capital:>15,.0f} руб")
        print(f"Прирост капитала:        {final_capital - total_capital:>15,.0f} руб  ({(final_capital/total_capital - 1)*100:+.2f}%)")
        print(f"Средний месячный доход:  {avg_monthly:>15,.0f} руб")
        print(f"Покрытие цели (50К):     {avg_monthly/optimizer.monthly_income_target*100:>15.1f}%")
        print(f"{'='*100}")
        
        # Сохраняем для сравнения
        results_summary.append({
            'Горизонт': label,
            'Прибыль': total_profit,
            'Прибыль %': profit_pct,
            'Итоговый капитал': final_capital,
            'Ср. мес. доход': avg_monthly,
            'Покрытие цели': f"{avg_monthly/optimizer.monthly_income_target*100:.1f}%",
            'Топ инструмент': max(weights.items(), key=lambda x: x[1])[0],
            'Топ доля': max(weights.values()) * 100
        })
    
    # Сравнительная таблица
    print(f"\n{'='*100}")
    print("📋 СВОДНОЕ СРАВНЕНИЕ ГОРИЗОНТОВ:")
    print(f"{'='*100}\n")
    
    df_summary = pd.DataFrame(results_summary)
    print(df_summary.to_string(index=False))
    
    # Анализ
    print(f"\n{'='*100}")
    print("🔍 АНАЛИЗ:")
    print(f"{'='*100}")
    
    max_profit_horizon = max(results_summary, key=lambda x: x['Прибыль %'])
    
    print(f"\n✅ Максимальная прибыль (%) достигается при горизонте: {max_profit_horizon['Горизонт']}")
    print(f"   Прибыль: {max_profit_horizon['Прибыль']:,.0f} руб ({max_profit_horizon['Прибыль %']:.2f}%)")
    print(f"   Лучший инструмент: {max_profit_horizon['Топ инструмент']} ({max_profit_horizon['Топ доля']:.1f}%)")
    
    # Рекомендация
    print(f"\n💡 РЕКОМЕНДАЦИЯ:")
    for res in results_summary:
        coverage_pct = float(res['Покрытие цели'].rstrip('%'))
        if coverage_pct >= 100:
            status = "✅"
        else:
            status = "⚠️"
        print(f"   {status} {res['Горизонт']:7s}: Прибыль {res['Прибыль']:>10,.0f} руб, "
              f"Мес. доход {res['Ср. мес. доход']:>8,.0f} руб ({res['Покрытие цели']})")
    
    print(f"\n{'='*100}")
    print("✅ Анализ максимизации прибыли завершен")
    print(f"{'='*100}\n")


if __name__ == "__main__":
    compare_profit_scenarios()

