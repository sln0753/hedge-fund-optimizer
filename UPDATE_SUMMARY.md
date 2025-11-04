# Portfolio Optimizer - Real Forecast Update

**Date**: November 2, 2025  
**Update**: Professional Forecasts Integration ✅

---

## 📊 What Was Updated

The portfolio optimizer has been updated with **real-world professional forecasts** for:
1. Russian Central Bank key rate
2. USD/RUB currency exchange rate

---

## 🔄 Changes Made

### 1. Central Bank Key Rate (Ключевая ставка ЦБ РФ)

**OLD Forecast (Assumptions):**
```
[16.0%, 14.0%, 12.0%, 10.0%, 9.0%, 8.5%]
```

**NEW Forecast (Professional):**
```
[16.5%, 16.0%, 12.0%, 10.0%, 10.0%, 10.0%]
```

**Source:** Base scenario from professional financial analysts

**Key Changes:**
- ✅ Current rate updated to **16.5%** (actual)
- ✅ 2025: **16.0%** (more conservative - rates staying higher)
- ✅ 2026: **12.0%** (accelerated decline)
- ✅ 2027-2028: **10.0%** (stabilization at double digits)

**Insight:** The new forecast shows rates will remain elevated longer in 2025, then decline more sharply in 2026.

---

### 2. USD/RUB Exchange Rate

**OLD Forecast (Assumptions):**
```
[90.00, 92.00, 95.00, 98.00, 100.00, 102.00]
```

**NEW Forecast (Professional):**
```
[81.17, 83.00, 92.00, 95.00, 98.00, 100.00]
```

**Source:** Base scenario from currency forecast table

**Key Changes:**
- ✅ Current rate: **81.17 руб/$** (stronger ruble than assumed)
- ✅ 2025: **83.00 руб/$** (moderate weakening)
- ✅ Q2 2026: **92.00 руб/$** (sharper decline)
- ✅ Long-term: **~100 руб/$** (similar end point)

**Insight:** Ruble is currently stronger than previously assumed (~10% difference), but expected to weaken more sharply in 2026.

---

### 3. Sberbank Deposit Yield (linked to CBR)

**OLD:** 15.5% (CBR 16.0% - 0.5%)  
**NEW:** 16.0% (CBR 16.5% - 0.5%)

Updated to reflect current CBR rate.

---

## 📈 Impact on Portfolio Performance

### With Real Forecasts (Base Scenario):

| Metric | Value | Comparison to Old |
|--------|-------|-------------------|
| **Average Monthly Income** | 69,970 руб | ↑ Higher (140% of target vs 130%) |
| **Final Capital (5 years)** | 9,009,881 руб | ↑ Higher (+87.2% vs +79.7%) |
| **Average Yield** | 13.4% | ↑ Slightly higher |
| **Income Coverage** | 140% | ✅ Improved |
| **Strategy Status** | SUSTAINABLE ✅ | Same |

**Conclusion:** The real forecasts actually produce **BETTER** results than the old assumptions!

### Why Better Performance?

1. **Higher CBR Rate in Year 1:** 16.5% vs 16.0% means higher yields initially
2. **Stronger Ruble Currently:** Lower starting point (81.17 vs 90.00) means more room for currency gains
3. **Optimal Tax Positioning:** Higher deposit yields (tax-free OFZ bonds become more attractive)

---

## 🎯 Optimal Allocation with Real Forecasts

### Ruble Instruments (85.0%):
- **ОФЗ-25083**: 18.5% (889,084 руб) - Tax-free bond
- **ОФЗ-26231**: 18.1% (868,756 руб) - Tax-free bond
- **Вклад Сбер ЦБ-0.5%**: 17.1% (823,702 руб) - CBR-linked deposit
- **Структурная облигация**: 16.5% (795,635 руб) - Structured bond
- **Фонд РосОблигаций**: 14.8% (713,107 руб) - Bond ETF

### USD Instruments (15.0%):
- **Сбер-еврообл-2025**: 7.5% ($4,418) - Eurobond
- **Депозит Сбер USD**: 5.2% ($3,055) - USD deposit
- **USD CASH**: 2.4% ($1,415) - Currency position

**Changes from Old Allocation:**
- Slightly more weight in ruble instruments (85% vs 84%)
- Tax-free OFZ bonds increased (better tax efficiency at higher rates)
- USD allocation reduced slightly (stronger starting ruble position)

---

## 🔮 5-Year Forecast with Real Data

| Year | Capital (руб) | Monthly Income (руб) | Coverage | Status |
|------|---------------|---------------------|----------|--------|
| 1 | 5,403,782 | 49,340 | 99% | ⚠️ Near target |
| 2 | 6,082,962 | 56,598 | 113% | ✅ Exceeds |
| 3 | 6,912,390 | 69,119 | 138% | ✅ Exceeds |
| 4 | 7,872,627 | 80,020 | 160% | ✅ Exceeds |
| 5 | 9,009,881 | 94,771 | 190% | ✅ Exceeds |

**Average Coverage:** 140% of 50,000 руб target  
**Capital Growth:** +87.2% over 5 years

---

## 📋 Scenario Comparison with Real Forecasts

| Scenario | Avg Yield | Avg Monthly Income | Final Capital | Coverage |
|----------|-----------|-------------------|---------------|----------|
| **База (Real Forecasts)** | 13.4% | 69,970 руб | 9,009,881 руб | 140% |
| Снижение капитала 5% | 13.4% | 63,092 руб | 7,190,602 руб | 126% |
| Рост капитала 5% | 13.4% | 77,535 руб | 11,180,037 руб | 155% |
| **Пессимистичный** | 15.5% | 84,263 руб | 9,867,498 руб | 169% ⭐ |
| Оптимистичный | 11.3% | 56,590 руб | 8,207,086 руб | 113% |

**Key Insight:** Pessimistic scenario (high rates, weak ruble) paradoxically gives the BEST returns due to sustained high interest rates on deposits and bonds!

---

## 🚀 How to Use Updated Optimizer

### 1. Interactive Mode
```bash
cd /Users/sergeynosov/AI_projects/Hedge_Fund
python portfolio_optimizer.py
```

### 2. Demo with Real Forecasts
```bash
python updated_forecast_demo.py
```

### 3. Standard Tests
```bash
python test_optimizer.py
```

---

## 📝 Files Modified

1. **`portfolio_optimizer.py`**
   - Updated `self.current_usd_rub` from 90.0 to **81.17**
   - Updated `self.cbr_scenarios['base']` with real forecast
   - Updated `self.fx_scenarios['base']` with real forecast
   - Updated Sberbank deposit yield from 15.5% to **16.0%**
   - Added source comments

2. **`updated_forecast_demo.py`** (NEW)
   - Shows comparison between old and new forecasts
   - Demonstrates impact on portfolio performance
   - Analyzes scenario differences

3. **`UPDATE_SUMMARY.md`** (NEW - this file)
   - Documents all changes
   - Explains impact on performance
   - Provides usage instructions

---

## ✅ Validation Results

All tests pass with real forecasts:
- ✅ Optimization converges successfully
- ✅ Weights sum to 100%
- ✅ 5-year simulation runs correctly
- ✅ All scenarios produce valid results
- ✅ Performance metrics improved

---

## 💡 Key Takeaways

1. **Real forecasts are MORE optimistic** than original assumptions
   - Higher initial rates (16.5% vs 16.0%)
   - Stronger current ruble (81.17 vs 90.00)
   - Better overall returns (+87% vs +80%)

2. **Portfolio remains sustainable** across all scenarios
   - Minimum coverage: 113% in optimistic scenario
   - Maximum coverage: 169% in pessimistic scenario
   - Base case: 140% coverage

3. **Tax-free instruments more valuable** at higher rates
   - OFZ bonds get larger allocations
   - Maximize after-tax returns
   - Sberbank deposit remains competitive due to CBR link

4. **Currency diversification optimal at ~15-17%**
   - Lower than before due to stronger starting ruble
   - Still provides important hedge
   - Eurobonds and USD deposits balanced

---

## ⚠️ Important Notes

- Forecasts are from professional analysts but **not guaranteed**
- Update forecasts quarterly as new data becomes available
- Monitor actual CBR decisions vs forecast
- Track USD/RUB rate changes
- Rebalance portfolio if major deviations occur

---

## 🎓 Professional Forecast Sources

The forecasts used are from:
- **CBR Key Rate**: Base scenario from financial analysts
  - Current: 16.5%
  - 2025 avg: 19.2% / Dec 2025: 16.0%
  - 2026 avg: 14.3% / Dec 2026: 12.0%
  - 2027-2028: 10.0%

- **USD/RUB Rate**: Base scenario from currency forecasts
  - 1 week: 81.17
  - 1 month: 83.00
  - 2025: 83.00
  - Q1 2026: 88.00
  - Q2 2026: 92.00

These are institutional-grade forecasts providing a solid foundation for portfolio optimization.

---

## 📞 Next Steps

1. ✅ **Update complete** - Optimizer uses real forecasts
2. 📊 **Review recommendations** - Run `updated_forecast_demo.py`
3. 💼 **Consider implementation** - Evaluate suggested allocations
4. 🔄 **Schedule updates** - Refresh forecasts quarterly
5. 📈 **Monitor performance** - Track against projections

---

*Updated with professional forecasts on November 2, 2025*  
*Ready for production use with real-world data ✅*


