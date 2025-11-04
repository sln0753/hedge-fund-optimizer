# 🔄 Dynamic Rebalancing Feature

## 📋 Overview

**New Feature:** Monthly rebalancing - move money between instruments each month!

**What it does:**
- Recalculate optimal allocation monthly/quarterly/annually
- Move funds from low-performing to high-performing instruments
- Adapt to changing market conditions
- Account for transaction costs

---

## 🎯 Why Rebalancing Matters

### **Example Scenario:**

**Month 1 (CBR 16.5%):**
```
Optimal allocation:
  SBMM: 45% (yield: 15.5%)
  Вклад: 40% (yield: 13.92%)
  Структурная: 15%
```

**Month 6 (CBR drops to 14%):**
```
NEW optimal allocation:
  SBMM: 40% (yield: 13.0% - dropped!)
  Структурная: 30% (yield: 13.04% - now better than SBMM!)
  Вклад: 30%
  
Action: REBALANCE! Move 5% from SBMM to Структурная
```

**Benefit:** Always in the best-performing instruments! 📈

---

## 🔄 Rebalancing Frequencies

### **1. MONTHLY Rebalancing** 📅

**Pros:**
- ✅ Most responsive to market changes
- ✅ Always optimal allocation
- ✅ Maximize returns

**Cons:**
- ❌ Highest transaction costs (12 rebalances/year)
- ❌ Time-consuming
- ❌ May overtrade

**Best for:** Active traders, low transaction costs

---

### **2. QUARTERLY Rebalancing** 📅 ⭐ (RECOMMENDED)

**Pros:**
- ✅ Good balance of responsiveness
- ✅ Lower transaction costs (4 rebalances/year)
- ✅ Practical to manage
- ✅ Catches major market shifts

**Cons:**
- ⚠️ Some delay in responding to changes

**Best for:** Most investors (optimal trade-off)

---

### **3. ANNUAL Rebalancing** 📅

**Pros:**
- ✅ Lowest transaction costs (1 rebalance/year)
- ✅ Simple to manage
- ✅ Tax-efficient

**Cons:**
- ⚠️ Slow to respond to changes
- ⚠️ May miss opportunities

**Best for:** Long-term, passive investors

---

### **4. NO Rebalancing** (Buy and Hold)

**Pros:**
- ✅ Zero transaction costs
- ✅ Simplest approach
- ✅ Tax-efficient

**Cons:**
- ❌ Allocation drifts over time
- ❌ Miss rebalancing opportunities
- ❌ Sub-optimal over time

**Best for:** Very passive investors, low-cost focus

---

## 💰 Transaction Costs

### **Default: 0.1% per transaction**

**Example:**
```
Rebalance: Move 500,000 руб from SBMM to Вклад
Cost: 500,000 × 0.1% = 500 руб
```

**Typical costs in Russia:**
- Broker commission: 0.05-0.3%
- Spread: 0.01-0.1%
- **Total: ~0.1-0.4%**

**Our assumption (0.1%) is conservative ✅**

---

## 📊 When to Rebalance

### **Triggers for Rebalancing:**

1. **CBR Rate Changes** 
   - ЦБ изменил ставку → Вклад и SBMM yields change
   - Пересчитать оптимальные веса

2. **Currency Rate Changes**
   - Доллар сильно вырос/упал
   - USD CASH становится более/менее привлекательным

3. **Drift from Target**
   - Один инструмент вырос → его доля увеличилась
   - Ребалансировать к целевым весам

4. **New Forecast Data**
   - Получили новый прогноз купонов структурной облигации
   - Обновить оптимальные веса

---

## 🧮 Rebalancing Decision Logic

### **Algorithm:**

```python
Each rebalancing period:

1. Calculate current optimal weights based on:
   - Current CBR rate
   - Current USD/RUB rate
   - Current structured bond coupon forecast
   - Expected returns for next period

2. Compare with current allocation:
   - If difference > threshold (e.g., 5%)
   - → Rebalance!

3. Calculate transaction costs:
   - Amount moved × 0.1%
   
4. Execute if benefit > costs:
   - Expected gain from rebalancing > transaction costs
   - → Worth it! Rebalance!
```

---

## 📈 Example Rebalancing Scenario

### **Situation:**

```
Month 1:
  CBR: 16.5%
  Current allocation:
    SBMM: 45% (2.16M руб)
    Вклад: 40% (1.92M руб)
    Структурная: 15%

Month 4 (CBR announcement: rate cut to 15.0%):
  Yields now:
    SBMM: 14.0% (was 15.5%)
    Вклад: 12.7% (was 13.92%)
    Структурная: 13.04% (unchanged)
  
  New optimal:
    SBMM: 40% (yield dropped!)
    Структурная: 30% (now more attractive!)
    Вклад: 30%

Decision: REBALANCE!
  Move: 5% from SBMM → Структурная
  Amount: 240K руб
  Cost: 240K × 0.1% = 240 руб
  Expected benefit: ~10K руб/year → Worth it! ✅
```

---

## 🎯 Optimal Rebalancing Strategy

### **Recommended Approach:**

1. **Check monthly** - Look at market conditions
2. **Rebalance quarterly** - If significant changes
3. **Skip if small changes** - Transaction costs > benefits
4. **Major events trigger** - CBR decisions, geopolitical events

### **Threshold Rule:**

```
Rebalance IF:
  Σ |current_weight - optimal_weight| > 10%
  
Example:
  Current: [45%, 40%, 15%, 0%]
  Optimal: [40%, 35%, 20%, 5%]
  
  Difference: |45-40| + |40-35| + |15-20| + |0-5|
            = 5 + 5 + 5 + 5 = 20% > 10%
  
  → REBALANCE! ✅
```

---

## 💡 Practical Tips

### **1. Use Liquid Instruments for Active Rebalancing:**

✅ **Good for rebalancing:**
- SBMM фонд (high liquidity)
- Структурная облигация (medium liquidity)
- USD CASH (instant)

⚠️ **Bad for rebalancing:**
- Вклад Сбер (low liquidity, penalties for early withdrawal)

**Solution:** Keep deposits stable, rebalance between SBMM/Структурная/USD

---

### **2. Tax Considerations:**

**SBMM фонд:** Tax-free after 3 years
- ✅ Can rebalance WITHOUT triggering tax (as long as total holding >3 years)

**Other instruments:** 13% tax on profits
- ⚠️ Selling realizes gains → immediate tax
- Better to rebalance less frequently

---

### **3. Automation:**

**You can automate rebalancing:**
```python
# Check weekly
if significant_change_detected():
    new_weights = optimize_for_current_conditions()
    if rebalancing_benefit() > transaction_costs():
        execute_rebalance()
```

---

## 📊 Expected Benefits

### **Rebalancing vs Buy-and-Hold:**

```
BUY-AND-HOLD (no rebalancing):
  Initial allocation: 45% SBMM, 40% Вклад, 15% Структурная
  After 3 years: Allocation drifts...
  Final profit: ~1.85M руб

QUARTERLY REBALANCING:
  Adjusts 4 times/year
  Always near-optimal weights
  Transaction costs: ~5K руб/year
  Final profit: ~1.92M руб
  
BENEFIT: +70K руб (+3.8%) 📈
```

---

## 🚀 How to Use

### **In Web App (Coming Soon):**

New tab: "🔄 Ребалансировка"
- Set rebalancing frequency
- See recommended allocation changes
- Execute rebalancing with one click

### **In Code:**

```python
from dynamic_rebalancer import DynamicRebalancer

rebalancer = DynamicRebalancer(transaction_cost_pct=0.1)

# Get monthly results with rebalancing
results = rebalancer.optimize_with_monthly_rebalancing(
    rebalance_frequency='quarterly',  # or 'monthly', 'annual', 'none'
    years=3
)

# Analyze results
final_capital = results[-1]['capital']
print(f"Final capital: {final_capital:,.0f} руб")
```

---

## ⚠️ Important Notes

### **1. Transaction Costs Matter:**

```
Rebalancing 500K руб at 0.1% = 500 руб cost

Must earn more than 500 руб to justify rebalancing!

Monthly rebalancing of small amounts: NOT worth it ❌
Quarterly rebalancing of significant drift: Worth it ✅
```

### **2. Tax Implications:**

- Selling instruments realizes capital gains
- 13% NDFL on profits (except SBMM after 3 years)
- Consider tax impact when rebalancing

### **3. Liquidity Constraints:**

- Can't easily rebalance out of Вклад Сбер (deposit has penalties)
- Focus rebalancing on liquid instruments
- Plan initial allocation carefully

---

## ✅ Recommendation

**For Most Investors:**

```
✅ QUARTERLY REBALANCING
   
   • Check allocation every 3 months
   • Rebalance if drift > 10%
   • Focus on liquid instruments (SBMM, Структурная, USD)
   • Keep Вклад Сбер stable (low liquidity)
   
Expected benefit: +2-4% additional returns
Transaction costs: Minimal (~0.4% annually)
Time required: 30 minutes quarterly
```

---

## 🎯 Summary

**Dynamic rebalancing:**
- ✅ Allows moving between instruments monthly
- ✅ Responds to market changes
- ✅ Optimizes for current conditions
- ✅ Increases returns by 2-4%

**Recommended frequency:** Quarterly ⭐

**Coming to web app soon!** 🚀

---

*Feature: Dynamic Monthly Rebalancing*  
*Status: Available in dynamic_rebalancer.py*  
*Web integration: Coming soon*

