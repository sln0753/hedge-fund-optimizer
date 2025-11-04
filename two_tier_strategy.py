"""
Two-Tier Portfolio Strategy
Fixed deposit + Dynamic SBMM/USD rebalancing
"""

from portfolio_optimizer import DynamicPortfolioOptimizer
import pandas as pd
import numpy as np

class TwoTierStrategy(DynamicPortfolioOptimizer):
    """
    Стратегия с двумя уровнями:
    1. ФИКСИРОВАННЫЙ: Депозит (заблокирован на 3 года)
    2. ДИНАМИЧЕСКИЙ: SBMM ↔ USD (ежемесячная ребалансировка)
    """
    
    def __init__(self, deposit_allocation=0.30, use_yaml_config=True):
        super().__init__(use_yaml_config)
        self.deposit_allocation = deposit_allocation  # Фиксированная доля в депозите
        self.dynamic_allocation = 1.0 - deposit_allocation  # Остаток для SBMM/USD
        
    def optimize_two_tier(self, years=3, rate_scenario='base', fx_scenario='base'):
        """
        Оптимизация двухуровневой стратегии
        
        Уровень 1: Фиксированный депозит
        Уровень 2: Динамическая ребалансировка SBMM ↔ USD
        """
        
        total_capital = self.initial_capital_rub + self.initial_usd_amount * self.current_usd_rub
        
        # TIER 1: Fixed deposit allocation
        deposit_capital = total_capital * self.deposit_allocation
        
        # TIER 2: Dynamic capital (for SBMM/USD rebalancing)
        dynamic_capital = total_capital * self.dynamic_allocation
        
        print("="*100)
        print("ДВУХУРОВНЕВАЯ СТРАТЕГИЯ ПОРТФЕЛЯ")
        print("TWO-TIER PORTFOLIO STRATEGY")
        print("="*100)
        
        print(f"\nОбщий капитал: {total_capital:,.0f} руб")
        print(f"\n🔒 УРОВЕНЬ 1: ФИКСИРОВАННЫЙ (Депозит)")
        print(f"   Вклад Сбер ЦБ-0.5%: {deposit_capital:,.0f} руб ({self.deposit_allocation*100:.0f}%)")
        print(f"   Срок: 3 года (без изменений)")
        print(f"   Ликвидность: Низкая (заблокирован)")
        
        print(f"\n🔄 УРОВЕНЬ 2: ДИНАМИЧЕСКИЙ (SBMM ↔ USD)")
        print(f"   Доступно для ребалансировки: {dynamic_capital:,.0f} руб ({self.dynamic_allocation*100:.0f}%)")
        print(f"   Инструменты: SBMM фонд ↔ USD CASH")
        print(f"   Ребалансировка: Ежемесячно по условиям")
        
        # Simulate with month-by-month decisions
        monthly_results = []
        current_sbmm = dynamic_capital  # Start with all in SBMM
        current_usd_rub = 0
        
        for month in range(years * 12):
            year_idx = month // 12
            
            # Calculate yields for this month
            cbr_rate = self.cbr_scenarios[rate_scenario][min(year_idx, len(self.cbr_scenarios[rate_scenario])-1)]
            
            # SBMM yield this year
            sbmm_annual_yield = (cbr_rate - 1.0)  # RUONIA = CBR - 1%
            sbmm_monthly_yield = sbmm_annual_yield / 12 / 100
            
            # USD expected gain for NEXT month
            fx_current = self.fx_scenarios[fx_scenario][min(year_idx, len(self.fx_scenarios[fx_scenario])-1)]
            fx_next_month = self.fx_scenarios[fx_scenario][min(year_idx, len(self.fx_scenarios[fx_scenario])-1)]
            # Approximate monthly USD change (simplified)
            if month < 12:
                fx_next = self.fx_scenarios[fx_scenario][1]
            elif month < 24:
                fx_next = self.fx_scenarios[fx_scenario][2]
            else:
                fx_next = self.fx_scenarios[fx_scenario][3]
            
            usd_expected_monthly = ((fx_next - fx_current) / fx_current / 12) * 100 if fx_next > fx_current else 0
            
            # Decision: Where should capital be this month?
            # If SBMM yield > USD expected → Keep in SBMM
            # If USD expected > SBMM yield → Move to USD
            
            if sbmm_annual_yield / 12 > usd_expected_monthly:
                # SBMM better → allocate more to SBMM
                optimal_sbmm_share = 0.9  # 90% of dynamic capital
            else:
                # USD better → allocate more to USD
                optimal_sbmm_share = 0.5  # 50-50 split
            
            # Calculate returns this month
            sbmm_income = current_sbmm * sbmm_monthly_yield
            
            # USD income (simplified - just FX gain)
            current_usd_dollars = current_usd_rub / fx_current if current_usd_rub > 0 else 0
            # Assume USD appreciates gradually
            usd_monthly_gain_pct = usd_expected_monthly / 100 if current_usd_rub > 0 else 0
            usd_income = current_usd_rub * usd_monthly_gain_pct
            
            # Deposit income (fixed tier)
            deposit_annual_yield = (cbr_rate - 0.5) * 0.87 / 100  # After tax
            deposit_monthly_income = deposit_capital * deposit_annual_yield / 12
            
            # Total monthly income
            total_monthly_income = sbmm_income + usd_income + deposit_monthly_income
            
            # Update capital
            current_sbmm += sbmm_income
            current_usd_rub += usd_income
            
            monthly_results.append({
                'month': month + 1,
                'year': year_idx + 1,
                'deposit_capital': deposit_capital,
                'sbmm_capital': current_sbmm,
                'usd_capital_rub': current_usd_rub,
                'total_capital': deposit_capital + current_sbmm + current_usd_rub,
                'monthly_income': total_monthly_income,
                'sbmm_yield': sbmm_annual_yield,
                'cbr_rate': cbr_rate
            })
        
        return monthly_results
    
    def display_two_tier_results(self):
        """Показать результаты двухуровневой стратегии"""
        
        results = self.optimize_two_tier()
        
        print(f"\n{'='*100}")
        print("РЕЗУЛЬТАТЫ ДВУХУРОВНЕВОЙ СТРАТЕГИИ:")
        print(f"{'='*100}\n")
        
        # Summary by year
        for year in [1, 2, 3]:
            year_months = [r for r in results if r['year'] == year]
            
            year_deposit = year_months[0]['deposit_capital']
            year_sbmm_start = year_months[0]['sbmm_capital']
            year_sbmm_end = year_months[-1]['sbmm_capital']
            year_usd_start = year_months[0]['usd_capital_rub']
            year_usd_end = year_months[-1]['usd_capital_rub']
            year_total_start = year_months[0]['total_capital']
            year_total_end = year_months[-1]['total_capital']
            year_income = sum([m['monthly_income'] for m in year_months])
            avg_monthly = year_income / 12
            
            print(f"ГОД {year}:")
            print(f"  Депозит (фиксированный):  {year_deposit:>12,.0f} руб")
            print(f"  SBMM (динамический):      {year_sbmm_start:>12,.0f} → {year_sbmm_end:>12,.0f} руб")
            print(f"  USD (динамический):       {year_usd_start:>12,.0f} → {year_usd_end:>12,.0f} руб")
            print(f"  Итого капитал:            {year_total_start:>12,.0f} → {year_total_end:>12,.0f} руб")
            print(f"  Годовой доход:            {year_income:>12,.0f} руб ({year_income/year_total_start*100:.2f}%)")
            print(f"  Средний мес. доход:       {avg_monthly:>12,.0f} руб ({avg_monthly/50000*100:.1f}% цели)")
            print(f"  CBR ставка:               {year_months[0]['cbr_rate']:>12.1f}%")
            print()
        
        # Total results
        final_result = results[-1]
        total_profit = final_result['total_capital'] - (self.initial_capital_rub + self.initial_usd_amount * self.current_usd_rub)
        
        print(f"{'='*100}")
        print("ИТОГИ ЗА 3 ГОДА:")
        print(f"{'='*100}")
        print(f"Итоговый капитал:   {final_result['total_capital']:>15,.0f} руб")
        print(f"Прибыль:            {total_profit:>15,.0f} руб ({total_profit/(self.initial_capital_rub + self.initial_usd_amount * self.current_usd_rub)*100:.2f}%)")
        print(f"{'='*100}\n")


if __name__ == "__main__":
    strategy = TwoTierStrategy(deposit_allocation=0.30)
    strategy.display_two_tier_results()

