"""
Dynamic Monthly Rebalancing Optimizer
Allows moving investments between instruments each month
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import pandas as pd
import numpy as np
from scipy.optimize import minimize

class DynamicRebalancer(DynamicPortfolioOptimizer):
    """Optimizer with monthly rebalancing capability"""
    
    def __init__(self, use_yaml_config=True, transaction_cost_pct=0.1):
        super().__init__(use_yaml_config)
        self.transaction_cost_pct = transaction_cost_pct  # Комиссия за перемещение (%)
        
    def optimize_with_monthly_rebalancing(self, rate_scenario='base', fx_scenario='base',
                                         capital_scenario='constant', years=3,
                                         rebalance_frequency='monthly'):
        """
        Оптимизация с возможностью ежемесячной ребалансировки
        
        Parameters:
        - rebalance_frequency: 'monthly', 'quarterly', 'annual', or 'none'
        - Каждый период пересчитываем оптимальные веса
        - Учитываем комиссии за перемещение средств
        """
        
        months_total = years * 12
        
        # Determine rebalancing periods
        if rebalance_frequency == 'monthly':
            rebalance_months = list(range(months_total))
        elif rebalance_frequency == 'quarterly':
            rebalance_months = list(range(0, months_total, 3))
        elif rebalance_frequency == 'annual':
            rebalance_months = list(range(0, months_total, 12))
        else:  # 'none'
            rebalance_months = [0]  # Only initial allocation
        
        # Initialize
        total_capital = self.initial_capital_rub + self.initial_usd_amount * self.current_usd_rub
        current_capital = total_capital
        current_weights = {inst: 0 for inst in self.instruments.keys()}
        
        # Initial allocation (month 0)
        current_weights = self._optimize_for_month(0, rate_scenario, fx_scenario)
        
        monthly_results = []
        
        for month in range(months_total):
            year_idx = month // 12
            month_in_year = month % 12
            
            # Check if we should rebalance this month
            if month in rebalance_months and month > 0:
                # Calculate optimal weights for current conditions
                new_weights = self._optimize_for_month(month, rate_scenario, fx_scenario)
                
                # Calculate transaction costs
                transaction_cost = self._calculate_rebalancing_cost(
                    current_weights, new_weights, current_capital
                )
                
                # Apply new weights
                current_weights = new_weights
                current_capital -= transaction_cost
            
            # Calculate returns for this month
            monthly_return = self._calculate_monthly_return(
                current_weights, year_idx, month_in_year, rate_scenario, fx_scenario
            )
            
            monthly_income = current_capital * monthly_return
            current_capital += monthly_income
            
            monthly_results.append({
                'month': month + 1,
                'year': year_idx + 1,
                'month_in_year': month_in_year + 1,
                'capital': current_capital,
                'monthly_income': monthly_income,
                'return_pct': monthly_return * 100,
                'rebalanced': month in rebalance_months,
                'weights': current_weights.copy()
            })
        
        return monthly_results
    
    def _optimize_for_month(self, month, rate_scenario, fx_scenario):
        """Оптимизация для конкретного месяца с учетом прогноза"""
        year_idx = month // 12
        
        instruments_list = list(self.instruments.keys())
        n_instruments = len(instruments_list)
        
        def objective(weights_array):
            weights_dict = {instrument: weights_array[i] 
                          for i, instrument in enumerate(instruments_list)}
            
            # Рассчитываем ожидаемую доходность на ближайший год
            expected_return = 0
            for instrument, weight in weights_dict.items():
                base_yield = self.instruments[instrument]['yield']
                adjusted_yield = self.calculate_after_tax_yield(
                    instrument, base_yield, year_idx, rate_scenario
                )
                expected_return += weight * adjusted_yield
            
            # Минимизируем отрицательную доходность (= максимизируем доходность)
            # Плюс штраф за концентрацию
            concentration_penalty = sum([w**2 for w in weights_array]) * 5
            
            return -expected_return + concentration_penalty
        
        # Ограничения и границы
        constraints = [{'type': 'eq', 'fun': lambda x: sum(x) - 1}]
        
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
        
        x0 = np.array([1/n_instruments] * n_instruments)
        
        result = minimize(objective, x0, method='SLSQP', 
                         constraints=constraints, bounds=bounds,
                         options={'maxiter': 200})
        
        optimal_weights = result.x if result.success else x0
        return {instrument: optimal_weights[i] for i, instrument in enumerate(instruments_list)}
    
    def _calculate_monthly_return(self, weights, year_idx, month_in_year, rate_scenario, fx_scenario):
        """Расчет месячной доходности портфеля"""
        monthly_return = 0
        
        for instrument, weight in weights.items():
            if weight > 0.001:
                base_yield = self.instruments[instrument]['yield']
                annual_yield = self.calculate_after_tax_yield(
                    instrument, base_yield, year_idx, rate_scenario
                )
                # Простое приближение: годовая доходность / 12
                monthly_yield = annual_yield / 12 / 100
                monthly_return += weight * monthly_yield
        
        return monthly_return
    
    def _calculate_rebalancing_cost(self, old_weights, new_weights, capital):
        """Расчет стоимости ребалансировки (комиссии на перемещение средств)"""
        total_moved = 0
        
        for instrument in old_weights.keys():
            weight_change = abs(new_weights.get(instrument, 0) - old_weights.get(instrument, 0))
            amount_moved = capital * weight_change
            total_moved += amount_moved
        
        # Комиссия только на фактически перемещенную сумму
        transaction_cost = total_moved * self.transaction_cost_pct / 100
        
        return transaction_cost


def demonstrate_rebalancing():
    """Демонстрация динамической ребалансировки"""
    
    print("="*100)
    print("ДИНАМИЧЕСКАЯ РЕБАЛАНСИРОВКА ПОРТФЕЛЯ")
    print("DYNAMIC PORTFOLIO REBALANCING")
    print("="*100)
    
    rebalancer = DynamicRebalancer(use_yaml_config=False, transaction_cost_pct=0.1)
    
    total_capital = rebalancer.initial_capital_rub + rebalancer.initial_usd_amount * rebalancer.current_usd_rub
    
    print(f"\nИсходный капитал: {total_capital:,.0f} руб")
    print(f"Комиссия за перемещение: {rebalancer.transaction_cost_pct}%")
    print(f"Период: 3 года (36 месяцев)")
    print(f"Сценарий: Базовый\n")
    
    # Сравнение разных стратегий ребалансировки
    strategies = [
        ('none', 'БЕЗ ребалансировки (buy-and-hold)'),
        ('annual', 'ГОДОВАЯ ребалансировка (раз в год)'),
        ('quarterly', 'КВАРТАЛЬНАЯ ребалансировка (раз в 3 месяца)'),
        ('monthly', 'МЕСЯЧНАЯ ребалансировка (каждый месяц)')
    ]
    
    comparison_results = []
    
    for strategy, label in strategies:
        print(f"{'='*100}")
        print(f"Стратегия: {label}")
        print(f"{'='*100}")
        
        results = rebalancer.optimize_with_monthly_rebalancing(
            rate_scenario='base',
            fx_scenario='base',
            years=3,
            rebalance_frequency=strategy
        )
        
        # Итоговые показатели
        final_capital = results[-1]['capital']
        total_profit = final_capital - total_capital
        avg_monthly_income = sum([r['monthly_income'] for r in results]) / len(results)
        rebalance_count = sum([1 for r in results if r['rebalanced']])
        
        print(f"\nРезультаты:")
        print(f"  Итоговый капитал: {final_capital:,.0f} руб")
        print(f"  Прибыль: {total_profit:,.0f} руб ({total_profit/total_capital*100:.2f}%)")
        print(f"  Средний месячный доход: {avg_monthly_income:,.0f} руб")
        print(f"  Количество ребалансировок: {rebalance_count}")
        
        # Показываем изменения весов (первые 12 месяцев)
        print(f"\n  Распределение по месяцам (первый год):")
        for i in range(min(12, len(results))):
            if results[i]['rebalanced']:
                month_num = results[i]['month']
                weights = results[i]['weights']
                print(f"\n  Месяц {month_num}: {'[РЕБАЛАНСИРОВКА]' if i > 0 else '[НАЧАЛО]'}")
                for inst, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
                    if weight > 0.01:
                        print(f"    {inst:40s}: {weight*100:5.1f}%")
        
        comparison_results.append({
            'Стратегия': label,
            'Итоговый капитал': final_capital,
            'Прибыль': total_profit,
            'Прибыль %': total_profit/total_capital*100,
            'Ср. мес. доход': avg_monthly_income,
            'Ребалансировок': rebalance_count
        })
    
    # Сравнительная таблица
    print(f"\n{'='*100}")
    print("СРАВНЕНИЕ СТРАТЕГИЙ РЕБАЛАНСИРОВКИ:")
    print(f"{'='*100}\n")
    
    df_comparison = pd.DataFrame(comparison_results)
    print(df_comparison.to_string(index=False))
    
    # Анализ
    print(f"\n{'='*100}")
    print("ВЫВОДЫ:")
    print(f"{'='*100}")
    
    best_strategy = max(comparison_results, key=lambda x: x['Прибыль'])
    
    print(f"\n✅ Лучшая стратегия: {best_strategy['Стратегия']}")
    print(f"   Прибыль: {best_strategy['Прибыль']:,.0f} руб ({best_strategy['Прибыль %']:.2f}%)")
    print(f"   Количество ребалансировок: {best_strategy['Ребалансировок']}")
    
    print(f"\n💡 РЕКОМЕНДАЦИЯ:")
    print(f"   Оптимальная частота ребалансировки зависит от:")
    print(f"   • Стоимости транзакций (комиссии)")
    print(f"   • Волатильности рынка")
    print(f"   • Ваших временных возможностей")
    print(f"\n   Для большинства инвесторов: КВАРТАЛЬНАЯ ребалансировка ⭐")
    print(f"   Баланс между выгодой и удобством")
    
    print(f"\n{'='*100}\n")


if __name__ == "__main__":
    demonstrate_rebalancing()

