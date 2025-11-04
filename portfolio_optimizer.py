import pandas as pd
import numpy as np
from scipy.optimize import minimize
import warnings
import os
warnings.filterwarnings('ignore')

# Try to import YAML loader
try:
    from config_loader import ConfigLoader
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

class DynamicPortfolioOptimizer:
    def __init__(self, use_yaml_config=True):
        # Начальные параметры (можно редактировать)
        self.initial_capital_rub = 4000000
        self.initial_usd_amount = 10000
        self.current_usd_rub = 81.17  # Обновлено: текущий курс по прогнозу
        self.monthly_income_target = 50000
        self.years = 3  # Горизонт планирования: 3 года (для налоговой льготы SBMM фонда)
        self.usd_spread_pct = 0.5  # Спред на покупку/продажу USD (% от курса) - типично 0.1-0.5% через брокера
        
        # Сценарии изменения тела инвестиций (% в год)
        self.capital_growth_scenarios = {
            'constant': 0.0,      # не меняется
            'decrease_5': -0.05,  # уменьшается 5% в год
            'decrease_10': -0.1,  # уменьшается 10% в год  
            'increase_5': 0.05,   # увеличивается 5% в год
            'increase_10': 0.1    # увеличивается 10% в год
        }
        
        # Load configuration from YAML files if available
        self.use_yaml = use_yaml_config and YAML_AVAILABLE
        
        if self.use_yaml:
            try:
                self.config_loader = ConfigLoader()
                # Load forecasts from YAML
                self.cbr_scenarios = self.config_loader.get_cbr_scenarios()
                self.fx_scenarios = self.config_loader.get_fx_scenarios()
                # Load instruments from YAML
                self.instruments = self.config_loader.load_instruments()
                # Update instruments with forecast data
                for name, data in self.instruments.items():
                    if data.get('variable_coupon', False):
                        coupons = self.config_loader.get_structured_bond_coupons(name)
                        if coupons:
                            self.instruments[name]['coupon_forecast'] = coupons
                print("✅ Loaded configuration from YAML files")
            except Exception as e:
                print(f"⚠️ Warning: Could not load YAML configs: {e}")
                print("   Falling back to hardcoded values")
                self.use_yaml = False
                self._load_hardcoded_config()
        else:
            self._load_hardcoded_config()
    
    def _load_hardcoded_config(self):
        """Load hardcoded configuration (fallback)"""
        # Прогнозные сценарии ЦБ РФ (обновлено по реальному прогнозу)
        # Источник: Базовый прогноз от профессиональных аналитиков
        self.cbr_scenarios = {
            'base': [16.5, 16.0, 12.0, 10.0, 10.0, 10.0],  # Реальный прогноз: 2025-2028
            'pessimistic': [16.5, 17.0, 15.0, 14.0, 13.0, 12.0],  # Медленное снижение
            'optimistic': [16.5, 14.0, 11.0, 9.0, 8.0, 7.5]  # Быстрое снижение
        }
        
        # Прогнозные сценарии USD/RUB (обновлено по реальному прогнозу)
        # Источник: Базовый прогноз валютных курсов
        self.fx_scenarios = {
            'base': [81.17, 83.0, 92.0, 95.0, 98.0, 100.0],  # Реальный прогноз: умеренное ослабление рубля
            'pessimistic': [81.17, 88.0, 100.0, 110.0, 118.0, 125.0],  # Сильное ослабление
            'optimistic': [81.17, 80.0, 78.0, 76.0, 75.0, 74.0]  # Укрепление рубля
        }
        
        # База инструментов (можно редактировать)
        self.instruments = self._initialize_instruments()
    
    def _initialize_instruments(self):
        """Инициализация базы инструментов"""
        return {
            # Рублевые инструменты
            # ОФЗ bonds removed - use real current bonds from Moscow Exchange
            
            'Вклад Сбер ЦБ-0.5%': {'type': 'Депозит', 'yield': 16.0, 'duration': 1.0, 
                                  'risk': 'низкий', 'tax_free': False, 'currency': 'RUB',
                                  'liquidity': 'низкая', 'cbr_linked': True},  # Обновлено: КС 16.5% - 0.5%
            
            'Сберегательный фонд УК Первая': {
                'type': 'БПИФ',
                'ticker': 'SBMM',
                'yield': 15.5,  # Follows RUONIA (≈ CBR - 1%)
                'duration': 0,
                'risk': 'низкий',
                'tax_free': True,  # TAX-FREE after 3 years! Major advantage!
                'currency': 'RUB',
                'liquidity': 'высокая',
                'management_fee': 0.2,  # Very low: 0.2%
                'total_expenses': 0.299,  # Total: 0.299% per year
                'ruonia_linked': True,  # Follows RUONIA overnight rate
                'tax_free_period': 3,  # Years to hold for tax exemption
                'tax_free_limit': 3000000  # Max profit exempt (rubles/year)
            },
            
            'Структурная облигация Сбер': {
                'type': 'Структурная облигация', 
                'yield': 15.0,  # Average annual (from forecast: ~1.25% × 12)
                'duration': 3.27, 
                'risk': 'средний', 
                'tax_free': False, 
                'currency': 'RUB', 
                'liquidity': 'средняя',
                'monthly_coupon': True,
                'variable_coupon': True,  # NEW: Coupons vary monthly
                # Monthly coupon forecast (SBERBCMI Index) Nov 2025 - Oct 2026
                'coupon_forecast': [1.01, 1.45, 1.55, 1.27, 1.43, 1.11, 0.96, 1.25, 1.49, 1.23, 1.24, 1.00]  # %/month
            },
            
            # Валютные инструменты
            # Eurobonds and USD deposits removed - low yields, not attractive now
            'USD CASH': {'type': 'Валюта', 'yield': 0.1, 'duration': 0, 
                        'risk': 'низкий', 'tax_free': True, 'currency': 'USD'}  # Keep as currency hedge (0.1% nominal to avoid numerical issues)
        }
    
    def calculate_after_tax_yield(self, instrument, base_yield, year, scenario):
        """Расчет доходности после налогов с учетом сценария"""
        instrument_data = self.instruments[instrument]
        
        # Корректировка доходности для инструментов, привязанных к ставке ЦБ
        if instrument_data.get('cbr_linked', False):
            cbr_rate = self.cbr_scenarios[scenario][min(year, len(self.cbr_scenarios[scenario])-1)]
            base_yield = cbr_rate - 0.5  # Ставка ЦБ - 0.5%
        
        # Корректировка для инструментов, привязанных к RUONIA (overnight rate)
        if instrument_data.get('ruonia_linked', False):
            cbr_rate = self.cbr_scenarios[scenario][min(year, len(self.cbr_scenarios[scenario])-1)]
            base_yield = cbr_rate - 1.0  # RUONIA ≈ Ставка ЦБ - 1.0%
        
        # Налоговая корректировка
        if instrument_data['tax_free']:
            after_tax = base_yield
        else:
            after_tax = base_yield * 0.87  # НДФЛ 13%
        
        # Для валютных инструментов учитываем курс
        # ИСПРАВЛЕНО: Расчет FX gain для конкретного года (не кумулятивно!)
        if instrument_data['currency'] == 'USD':
            # Курс на НАЧАЛО года (предыдущий год)
            fx_year_start = self.fx_scenarios[scenario][min(year, len(self.fx_scenarios[scenario])-1)]
            # Курс на КОНЕЦ года (текущий год)
            fx_year_end = self.fx_scenarios[scenario][min(year + 1, len(self.fx_scenarios[scenario])-1)]
            
            # Учитываем bid-ask spread (стоимость конвертации)
            # При покупке USD: платим fx × (1 + spread/2)
            # При продаже USD: получаем fx × (1 - spread/2)
            # Эффективный курс с учетом спреда:
            fx_buy_rate = fx_year_start * (1 + self.usd_spread_pct / 200)  # Покупка в начале года
            fx_sell_rate = fx_year_end * (1 - self.usd_spread_pct / 200)   # Продажа в конце года
            
            # Прирост ТОЛЬКО за этот год с учетом спреда (в рублях!)
            fx_gain = (fx_sell_rate - fx_buy_rate) / fx_buy_rate * 100
            after_tax += fx_gain
        
        return max(after_tax, 0)  # Доходность не может быть отрицательной
    
    def simulate_portfolio_performance(self, weights, capital_growth_scenario, 
                                     rate_scenario, fx_scenario='base', years=None):
        """Симуляция работы портфеля на несколько лет"""
        if years is None:
            years = self.years
            
        results = []
        current_capital_rub = self.initial_capital_rub
        current_usd = self.initial_usd_amount
        total_capital = current_capital_rub + current_usd * self.current_usd_rub
        
        for year in range(years):
            year_results = {
                'year': year + 1,
                'capital_start_rub': current_capital_rub,
                'capital_start_usd': current_usd,
                'total_capital_start': total_capital
            }
            
            # Расчет доходности портфеля за год
            portfolio_yield = 0
            monthly_income = 0
            
            for instrument, weight in weights.items():
                if weight > 0.001:  # учитываем только значимые доли
                    instrument_data = self.instruments[instrument]
                    base_yield = instrument_data['yield']
                    
                    # Корректируем доходность
                    adjusted_yield = self.calculate_after_tax_yield(
                        instrument, base_yield, year, rate_scenario
                    )
                    
                    instrument_contribution = weight * adjusted_yield / 100
                    portfolio_yield += instrument_contribution
                    
                    # Ежемесячный доход от инструмента
                    monthly_income += (total_capital * weight * adjusted_yield / 100) / 12
            
            # Годовой доход и изменение капитала
            annual_income = total_capital * portfolio_yield
            year_results['portfolio_yield'] = portfolio_yield * 100
            year_results['annual_income'] = annual_income
            year_results['monthly_income'] = monthly_income
            
            # Изменение капитала согласно сценарию
            growth_rate = self.capital_growth_scenarios[capital_growth_scenario]
            capital_change = total_capital * growth_rate
            
            # Итоговый капитал
            total_capital = total_capital + annual_income + capital_change
            total_capital = max(total_capital, 0)  # Капитал не может быть отрицательным
            
            # Распределение между рублями и USD (сохраняем пропорции)
            usd_share = current_usd * self.current_usd_rub / year_results['total_capital_start']
            current_capital_rub = total_capital * (1 - usd_share)
            current_usd = total_capital * usd_share / self.current_usd_rub
            
            year_results['capital_change'] = capital_change
            year_results['total_capital_end'] = total_capital
            year_results['usd_share'] = usd_share * 100
            
            results.append(year_results)
        
        return results
    
    def optimize_portfolio(self, capital_growth_scenario='constant', 
                         rate_scenario='base', fx_scenario='base', 
                         target_income_coverage=1.0):
        """Оптимизация портфеля для заданных сценариев"""
        instruments_list = list(self.instruments.keys())
        n_instruments = len(instruments_list)
        
        def objective(weights_array):
            # Преобразуем массив в словарь
            weights_dict = {instrument: weights_array[i] for i, instrument in enumerate(instruments_list)}
            
            # Симулируем работу портфеля
            simulation = self.simulate_portfolio_performance(
                weights_dict, capital_growth_scenario, rate_scenario, fx_scenario
            )
            
            # Целевая функция: максимизация покрытия расходов и минимизация риска
            total_penalty = 0
            income_shortfalls = 0
            capital_decline = 0
            
            for year_result in simulation:
                # Штраф за недополучение дохода
                income_ratio = year_result['monthly_income'] / self.monthly_income_target
                if income_ratio < target_income_coverage:
                    income_shortfalls += (target_income_coverage - income_ratio) ** 2
                
                # Штраф за уменьшение капитала (если это не запланировано)
                if capital_growth_scenario not in ['decrease_5', 'decrease_10']:
                    capital_ratio = year_result['total_capital_end'] / year_result['total_capital_start']
                    if capital_ratio < 1.0:
                        capital_decline += (1.0 - capital_ratio) ** 2
            
            # Штраф за концентрацию рисков
            concentration_penalty = sum([w**2 for w in weights_array]) * 10
            
            total_penalty = income_shortfalls * 100 + capital_decline * 50 + concentration_penalty
            
            return total_penalty
        
        # Ограничения
        constraints = [
            {'type': 'eq', 'fun': lambda x: sum(x) - 1}  # сумма долей = 1
        ]
        
        # Границы для каждого инструмента
        bounds = []
        for instrument in instruments_list:
            instrument_data = self.instruments[instrument]
            
            if instrument == 'Структурная облигация Сбер':
                bounds.append((0, 0.2))  # максимум 20%
            elif instrument_data['currency'] == 'USD':
                bounds.append((0, 0.4))  # максимум 40% в валюте
            elif instrument_data['risk'] == 'низкий':
                bounds.append((0, 0.5))  # гибкие границы для надежных инструментов
            else:
                bounds.append((0, 0.4))
        
        # Начальное приближение (равномерное распределение)
        x0 = np.array([1/n_instruments] * n_instruments)
        
        # Оптимизация
        result = minimize(objective, x0, method='SLSQP', 
                         constraints=constraints, bounds=bounds, 
                         options={'maxiter': 500, 'ftol': 1e-6})
        
        optimal_weights = result.x if result.success else x0
        return {instrument: optimal_weights[i] for i, instrument in enumerate(instruments_list)}
    
    def generate_recommendations(self, capital_growth_scenario='constant', 
                               rate_scenario='base', fx_scenario='base'):
        """Генерация рекомендаций для заданных сценариев"""
        print(f"\n{'='*80}")
        print(f"РЕКОМЕНДАЦИИ ПО ПОРТФЕЛЮ")
        print(f"Сценарий изменения капитала: {capital_growth_scenario}")
        print(f"Сценарий ставок: {rate_scenario}")
        print(f"Сценарий курса: {fx_scenario}")
        print(f"{'='*80}")
        
        # Оптимизируем портфель
        optimal_weights = self.optimize_portfolio(capital_growth_scenario, rate_scenario, fx_scenario)
        
        # Симулируем результаты
        simulation = self.simulate_portfolio_performance(
            optimal_weights,
            capital_growth_scenario, rate_scenario, fx_scenario
        )
        
        # Вывод оптимального распределения
        print(f"\n📊 ОПТИМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ АКТИВОВ:")
        rub_instruments = []
        usd_instruments = []
        
        total_capital = self.initial_capital_rub + self.initial_usd_amount * self.current_usd_rub
        
        for instrument, weight in optimal_weights.items():
            if weight > 0.01:
                instrument_data = self.instruments[instrument]
                amount = total_capital * weight
                
                item = {
                    'Инструмент': instrument,
                    'Доля': f"{weight*100:.1f}%",
                    'Сумма': f"{amount:,.0f} руб." if instrument_data['currency'] == 'RUB' else f"${amount/self.current_usd_rub:,.0f}",
                    'Тип': instrument_data['type'],
                    'Валюта': instrument_data['currency'],
                    'Доходность': f"{instrument_data['yield']:.1f}%"
                }
                
                if instrument_data['currency'] == 'RUB':
                    rub_instruments.append(item)
                else:
                    usd_instruments.append(item)
        
        if rub_instruments:
            print("\nРублевые инструменты:")
            df_rub = pd.DataFrame(rub_instruments)
            print(df_rub.to_string(index=False))
        
        if usd_instruments:
            print("\nВалютные инструменты:")
            df_usd = pd.DataFrame(usd_instruments)
            print(df_usd.to_string(index=False))
        
        # Прогноз на 5 лет
        print(f"\n📈 ПРОГНОЗ НА {self.years} ЛЕТ:")
        forecast_data = []
        for year_result in simulation:
            coverage = "✅ ПОЛНОЕ" if year_result['monthly_income'] >= self.monthly_income_target else "❌ НЕДОСТАТОЧНО"
            forecast_data.append({
                'Год': year_result['year'],
                'Капитал, руб': f"{year_result['total_capital_end']:,.0f}",
                'Доходность': f"{year_result['portfolio_yield']:.1f}%",
                'Месячный доход': f"{year_result['monthly_income']:,.0f}",
                'Покрытие расходов': coverage,
                'Доля USD': f"{year_result['usd_share']:.1f}%"
            })
        
        df_forecast = pd.DataFrame(forecast_data)
        print(df_forecast.to_string(index=False))
        
        # Анализ устойчивости
        print(f"\n🔍 АНАЛИЗ УСТОЙЧИВОСТИ СТРАТЕГИИ:")
        avg_coverage = sum([r['monthly_income'] for r in simulation]) / len(simulation) / self.monthly_income_target * 100
        capital_change_pct = (simulation[-1]['total_capital_end'] - simulation[0]['total_capital_start']) / simulation[0]['total_capital_start'] * 100
        
        print(f"Среднее покрытие расходов: {avg_coverage:.0f}%")
        print(f"Капитал сохранен: {capital_change_pct:+.1f}%")
        
        if avg_coverage >= 100 and capital_change_pct >= 0:
            print("\n✅ Стратегия устойчива при заданных параметрах")
        elif avg_coverage >= 100:
            print("\n⚠️ Доход достаточен, но капитал снижается")
        else:
            print("\n❌ Стратегия не обеспечивает целевой доход")
    
    def compare_scenarios(self):
        """Сравнение различных сценариев"""
        print(f"\n{'='*80}")
        print("СРАВНЕНИЕ СЦЕНАРИЕВ")
        print(f"{'='*80}")
        
        scenarios_to_compare = [
            ('constant', 'base', 'base', 'База'),
            ('decrease_5', 'base', 'base', 'Снижение капитала 5%'),
            ('increase_5', 'base', 'base', 'Рост капитала 5%'),
            ('constant', 'pessimistic', 'pessimistic', 'Пессимистичный'),
            ('constant', 'optimistic', 'optimistic', 'Оптимистичный'),
        ]
        
        comparison_results = []
        
        for capital_scenario, rate_scenario, fx_scenario, label in scenarios_to_compare:
            print(f"\nАнализ сценария: {label}...")
            optimal_weights = self.optimize_portfolio(capital_scenario, rate_scenario, fx_scenario)
            simulation = self.simulate_portfolio_performance(
                optimal_weights, capital_scenario, rate_scenario, fx_scenario
            )
            
            avg_yield = sum([r['portfolio_yield'] for r in simulation]) / len(simulation)
            avg_income = sum([r['monthly_income'] for r in simulation]) / len(simulation)
            final_capital = simulation[-1]['total_capital_end']
            avg_coverage = avg_income / self.monthly_income_target * 100
            
            comparison_results.append({
                'Сценарий': label,
                'Ср. доходность': f"{avg_yield:.1f}%",
                'Ср. месячный доход': f"{avg_income:,.0f} руб.",
                'Итоговый капитал': f"{final_capital:,.0f} руб.",
                'Покрытие расходов': f"{avg_coverage:.0f}%"
            })
        
        print(f"\n📋 СВОДНОЕ СРАВНЕНИЕ:")
        df_comparison = pd.DataFrame(comparison_results)
        print(df_comparison.to_string(index=False))


def main():
    """Главная функция с интерактивным меню"""
    optimizer = DynamicPortfolioOptimizer()
    
    while True:
        print(f"\n{'='*80}")
        print("СИСТЕМА ОПТИМИЗАЦИИ ИНВЕСТИЦИОННОГО ПОРТФЕЛЯ")
        print(f"{'='*80}")
        print("1. Текущие рекомендации")
        print("2. Сравнение сценариев")
        print("3. Редактировать параметры")
        print("4. Показать список инструментов")
        print("5. Показать сценарии")
        print("6. Выход")
        
        choice = input("\nВыберите опцию (1-6): ").strip()
        
        if choice == '1':
            print("\nДоступные сценарии капитала: constant, decrease_5, decrease_10, increase_5, increase_10")
            capital_scenario = input("Сценарий капитала [constant]: ").strip() or 'constant'
            
            print("\nДоступные сценарии ставок: base, pessimistic, optimistic")
            rate_scenario = input("Сценарий ставок [base]: ").strip() or 'base'
            
            print("\nДоступные сценарии курса: base, pessimistic, optimistic")
            fx_scenario = input("Сценарий курса [base]: ").strip() or 'base'
            
            optimizer.generate_recommendations(capital_scenario, rate_scenario, fx_scenario)
            
        elif choice == '2':
            optimizer.compare_scenarios()
            
        elif choice == '3':
            print("\n⚙️ РЕДАКТИРОВАНИЕ ПАРАМЕТРОВ")
            try:
                new_capital_rub = input(f"Начальный капитал в RUB [{optimizer.initial_capital_rub}]: ").strip()
                if new_capital_rub:
                    optimizer.initial_capital_rub = float(new_capital_rub)
                
                new_usd = input(f"Начальный капитал в USD [{optimizer.initial_usd_amount}]: ").strip()
                if new_usd:
                    optimizer.initial_usd_amount = float(new_usd)
                
                new_rate = input(f"Текущий курс USD/RUB [{optimizer.current_usd_rub}]: ").strip()
                if new_rate:
                    optimizer.current_usd_rub = float(new_rate)
                
                new_target = input(f"Целевой месячный доход [{optimizer.monthly_income_target}]: ").strip()
                if new_target:
                    optimizer.monthly_income_target = float(new_target)
                
                new_years = input(f"Горизонт планирования (лет) [{optimizer.years}]: ").strip()
                if new_years:
                    optimizer.years = int(new_years)
                
                print("\n✅ Параметры обновлены!")
            except ValueError:
                print("\n❌ Ошибка ввода. Параметры не изменены.")
        
        elif choice == '4':
            print("\n🏦 СПИСОК ИНСТРУМЕНТОВ:")
            for i, (name, data) in enumerate(optimizer.instruments.items(), 1):
                print(f"{i}. {name}: {data}")
        
        elif choice == '5':
            print("\n📅 СЦЕНАРИИ СТАВОК ЦБ:")
            for scenario, rates in optimizer.cbr_scenarios.items():
                print(f"{scenario}: {rates}")
            
            print("\n📅 СЦЕНАРИИ КУРСА USD/RUB:")
            for scenario, rates in optimizer.fx_scenarios.items():
                print(f"{scenario}: {rates}")
            
            print("\n📅 СЦЕНАРИИ ИЗМЕНЕНИЯ КАПИТАЛА:")
            for scenario, rate in optimizer.capital_growth_scenarios.items():
                print(f"{scenario}: {rate*100:+.1f}% в год")
        
        elif choice == '6':
            print("\nДо свидания!")
            break
        
        else:
            print("\n❌ Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

