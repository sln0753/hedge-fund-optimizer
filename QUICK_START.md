# Quick Start Guide - Portfolio Optimizer

## 📍 Location
```bash
cd /Users/sergeynosov/AI_projects/Hedge_Fund
```

## 🚀 Quick Commands

### 1. See What's New (Real Forecasts Demo)
```bash
python updated_forecast_demo.py
```
**Shows:**
- Comparison of old vs new forecasts
- Impact on portfolio performance
- Optimal allocation with real data
- 5-year projections
- Scenario analysis

**Runtime:** ~30 seconds

---

### 2. Interactive Portfolio Optimizer
```bash
python portfolio_optimizer.py
```
**Features:**
- Menu-driven interface
- Get recommendations for any scenario
- Compare multiple scenarios
- Edit parameters (capital, target income, etc.)
- View all instruments and scenarios

**Choose options:**
1. Текущие рекомендации - Get specific recommendations
2. Сравнение сценариев - Compare 5 key scenarios
3. Редактировать параметры - Change your capital/income targets
4. Показать список инструментов - View all 8 instruments
5. Показать сценарии - View CBR and FX forecasts
6. Выход - Exit

---

### 3. Run Tests (Verify Everything Works)
```bash
python test_optimizer.py
```
**Tests:**
- Portfolio optimization
- 5-year simulation
- Recommendation generation
- Multiple scenarios
- All instruments

**Expected:** All tests pass ✅

---

### 4. Quick Demo (Original)
```bash
python quick_demo.py
```
**Shows:**
- Base scenario optimization
- Pessimistic scenario
- Full scenario comparison

---

## 📊 Current Settings (with Real Forecasts)

### Portfolio Parameters:
- **Initial capital (RUB):** 4,000,000 руб
- **Initial capital (USD):** $10,000
- **Current USD/RUB rate:** 81.17 ✅ (updated from real forecast)
- **Target monthly income:** 50,000 руб
- **Planning horizon:** 5 years

### CBR Key Rate Forecast (Base):
```
[16.5%, 16.0%, 12.0%, 10.0%, 10.0%, 10.0%]
```
✅ Updated from professional analyst forecasts

### USD/RUB Forecast (Base):
```
[81.17, 83.00, 92.00, 95.00, 98.00, 100.00]
```
✅ Updated from currency forecast table

---

## 🎯 Expected Results (Base Scenario with Real Forecasts)

| Metric | Value |
|--------|-------|
| Average Monthly Income | 69,970 руб (140% of target) |
| Final Capital (5 years) | 9,009,881 руб |
| Capital Growth | +87.2% |
| Strategy Status | ✅ SUSTAINABLE |

---

## 📚 Documentation Files

1. **README.md** - Complete user guide
2. **UPDATE_SUMMARY.md** - Real forecast integration details
3. **DEPLOYMENT_SUMMARY.md** - Technical deployment info
4. **QUICK_START.md** - This file

---

## 🔧 Customization

### Change Your Capital:
1. Run `python portfolio_optimizer.py`
2. Choose option 3 (Редактировать параметры)
3. Enter your actual amounts

### Update Forecasts:
Edit `portfolio_optimizer.py` lines 25-39:
- `self.cbr_scenarios['base']` - Central Bank rates
- `self.fx_scenarios['base']` - USD/RUB rates
- `self.current_usd_rub` - Current exchange rate

### Add/Remove Instruments:
Edit `portfolio_optimizer.py` method `_initialize_instruments()`

---

## 💡 Tips

1. **Start with the demo:**
   ```bash
   python updated_forecast_demo.py
   ```

2. **Then try interactive mode** to explore different scenarios:
   ```bash
   python portfolio_optimizer.py
   ```

3. **Update forecasts quarterly** as new analyst data becomes available

4. **Compare scenarios** (option 2 in interactive mode) to see range of outcomes

5. **Focus on tax-free instruments** (OFZ bonds) when rates are high

---

## ⚠️ Important Reminders

- This is NOT individual investment advice
- Forecasts are professional but not guaranteed
- Consult with a financial advisor
- Update forecasts regularly
- Consider your risk tolerance

---

## 📞 Need Help?

**Documentation:**
- README.md - Full usage guide
- UPDATE_SUMMARY.md - What changed with real forecasts
- problem_posing.txt - Original specification (Russian)

**Test everything works:**
```bash
python test_optimizer.py
```

**Quick results:**
```bash
python updated_forecast_demo.py
```

---

*Last updated: November 2, 2025*  
*Using real professional forecasts ✅*


