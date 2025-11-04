# 📝 Configuration Editing Guide

## 🎯 Overview

Your portfolio optimizer now uses **TWO separate configuration files**:

1. **`instruments_config.yaml`** - STATIC instrument parameters (type, risk, tax, etc.)
2. **`forecasts_config.yaml`** - DYNAMIC forecast data (CBR rates, currency, coupons)

**This makes it EASY to update forecasts without touching instrument definitions!** ✅

---

## 📁 **File Structure:**

```
Hedge_Fund/
├── instruments_config.yaml    ← Edit instrument parameters HERE
├── forecasts_config.yaml      ← Edit forecasts HERE (frequently)
├── portfolio_optimizer.py     ← Main code (rarely edit)
└── config_loader.py           ← Loader (don't edit)
```

---

## 📊 **FILE 1: instruments_config.yaml**

### **What's Inside:**

Each instrument has:
```yaml
Instrument Name:
  type: Депозит/ОФЗ/БПИФ/Акция/etc
  yield: 15.0             # Base yield (%)
  duration: 2.5           # Duration in years
  risk: низкий/средний/высокий
  tax_free: true/false    # Tax-exempt?
  currency: RUB/USD
  liquidity: высокая/средняя/низкая
  description: Text description
```

### **When to Edit:**

✅ **Edit this file when:**
- Adding NEW instruments
- Removing instruments
- Changing instrument TYPE or RISK
- Updating BASE yields (not forecast-based)
- Changing tax treatment
- Adding descriptions

❌ **DON'T edit for:**
- CBR rate forecasts → Use forecasts_config.yaml
- Currency forecasts → Use forecasts_config.yaml
- Structured bond coupons → Use forecasts_config.yaml

### **Example - Add New Instrument:**

```yaml
ОФЗ-26244-ПД:
  type: ОФЗ
  yield: 15.2
  duration: 2.0
  risk: низкий
  tax_free: true           # ОФЗ налогом не облагаются!
  currency: RUB
  liquidity: высокая
  description: |
    Облигация федерального займа
    ISIN: RU000A106ZZ9
    Погашение: 2027-07-15
    Купоны: 2 раза в год
```

---

## 📈 **FILE 2: forecasts_config.yaml**

### **What's Inside:**

Three sections:

#### **A. CBR Rate Forecasts**
```yaml
cbr_scenarios:
  base:
    rates: [16.5, 16.0, 12.0, 10.0, 10.0, 10.0]
    description: Base scenario description
```

#### **B. USD/RUB Forecasts**
```yaml
fx_scenarios:
  base:
    rates: [81.17, 83.00, 92.00, 95.00, 98.00, 100.00]
    description: Base scenario description
```

#### **C. Structured Bond Coupons**
```yaml
structured_bond_coupons:
  Структурная облигация Сбер:
    monthly_coupons:
      - month: Ноябрь 2025
        coupon: 1.01
      - month: Декабрь 2025
        coupon: 1.45
      # ... etc for 12 months
```

### **When to Edit:**

✅ **Edit this file when:**
- Getting NEW CBR forecasts (quarterly)
- Getting NEW currency forecasts (quarterly)
- Getting NEW structured bond coupon forecasts (annual)
- Market conditions change significantly

### **How Often to Update:**

| Forecast | Update Frequency | Source |
|----------|------------------|--------|
| **CBR Rates** | Quarterly | cbr.ru, analyst reports |
| **USD/RUB** | Quarterly | Bank forecasts |
| **Structured Coupons** | Annually | SBERBCMI Index |

---

## 🔧 **HOW TO EDIT FORECASTS:**

### **Step 1: Update CBR Rate Forecast**

Open `forecasts_config.yaml`, find this section:

```yaml
cbr_scenarios:
  base:
    rates: [16.5, 16.0, 12.0, 10.0, 10.0, 10.0]
```

**Change the numbers:**
```yaml
cbr_scenarios:
  base:
    rates: [17.0, 15.5, 13.0, 11.0, 10.0, 9.5]  # Updated forecast!
```

### **Step 2: Update USD/RUB Forecast**

Find:
```yaml
fx_scenarios:
  base:
    rates: [81.17, 83.00, 92.00, 95.00, 98.00, 100.00]
```

**Update current rate and future rates:**
```yaml
fx_scenarios:
  base:
    rates: [85.00, 87.00, 93.00, 96.00, 99.00, 102.00]  # New forecast!
```

### **Step 3: Update Structured Bond Coupons**

When Sberbank publishes new SBERBCMI forecast:

```yaml
structured_bond_coupons:
  Структурная облигация Сбер:
    monthly_coupons:
      - month: Ноябрь 2026        # NEW period!
        coupon: 1.10              # NEW forecast!
      - month: Декабрь 2026
        coupon: 1.35
      # ... update all 12 months
```

**Also update:**
```yaml
    average_monthly: 1.30  # Recalculate average
    average_annual: 15.6   # Sum of all 12 coupons
```

---

## 🚀 **DEPLOY UPDATED FORECASTS:**

After editing YAML files:

```bash
cd /Users/sergeynosov/AI_projects/Hedge_Fund

# Test locally first!
python portfolio_optimizer.py
# Or web app:
streamlit run web_app.py

# If works correctly, deploy:
git add forecasts_config.yaml
git commit -m "Updated CBR and FX forecasts for Q1 2026"
git push

# Streamlit Cloud auto-deploys in ~1 minute! ✅
```

---

## ✅ **ADVANTAGES OF THIS SYSTEM:**

### **1. Separation of Concerns:**
```
instruments_config.yaml  → WHAT you can invest in (changes rarely)
forecasts_config.yaml    → WHERE markets are going (update quarterly)
```

### **2. Easy to Update:**
- Edit simple YAML file (not Python code)
- No programming knowledge needed
- Can't break the code with typos
- Clear structure

### **3. Version Control:**
```
Git tracks ALL forecast changes
Can see history: "CBR forecast on Dec 1, 2025 was..."
Can revert if needed
```

### **4. Documentation Built-in:**
Each section has descriptions explaining what it is

### **5. Safe:**
- Instruments file protected (edit rarely)
- Forecasts file easy to update (edit often)
- Optimizer validates data automatically

---

## 📋 **EDITING CHECKLIST:**

### **For Quarterly Forecast Update:**

- [ ] Open `forecasts_config.yaml`
- [ ] Update `cbr_scenarios.base.rates` with new CBR forecast
- [ ] Update `fx_scenarios.base.rates` with new USD/RUB forecast
- [ ] Update `metadata.last_updated` date at bottom
- [ ] Save file
- [ ] Test locally: `python portfolio_optimizer.py`
- [ ] Commit: `git commit -m "Q1 2026 forecast update"`
- [ ] Push: `git push`
- [ ] Wait 1 minute for cloud deployment
- [ ] Test on cloud app

### **For Adding New Instrument:**

- [ ] Open `instruments_config.yaml`
- [ ] Copy template from bottom of file
- [ ] Fill in all parameters
- [ ] Add description
- [ ] Save file
- [ ] Test locally
- [ ] Commit and push
- [ ] Verify on cloud app

---

## 🎓 **EXAMPLES:**

### **Example 1: Update CBR Forecast (Feb 2026)**

```yaml
# forecasts_config.yaml

cbr_scenarios:
  base:
    # OLD (Nov 2025):
    # rates: [16.5, 16.0, 12.0, 10.0, 10.0, 10.0]
    
    # NEW (Feb 2026 - actual rates materialized):
    rates: [15.0, 14.0, 12.0, 10.5, 10.0, 9.5]
    description: |
      Обновлено Feb 2026
      ЦБ снизил ставку быстрее прогноза
      Инфляция замедлилась до 5%
```

### **Example 2: Add Corporate Bond**

```yaml
# instruments_config.yaml

Газпром БО-001P-15:
  type: Корпоративная облигация
  yield: 14.5
  duration: 2.5
  risk: низкий             # Газпром = голубая фишка
  tax_free: false
  currency: RUB
  liquidity: высокая
  description: |
    Биржевая облигация Газпрома
    ISIN: RU000AXXXXXX
    Погашение: 2028-06-15
    Купоны полугодовые
```

### **Example 3: Update Structured Bond Coupons (Nov 2026)**

```yaml
# forecasts_config.yaml

structured_bond_coupons:
  Структурная облигация Сбер:
    period: "Ноябрь 2026 - Октябрь 2027"  # NEW period
    monthly_coupons:
      - month: Ноябрь 2026
        coupon: 0.95                       # NEW data from SBERBCMI
      - month: Декабрь 2026
        coupon: 1.20
      # ... all 12 months with NEW forecast
    
    average_annual: 14.2  # Recalculate sum
```

---

## ⚠️ **IMPORTANT NOTES:**

### **YAML Syntax Rules:**

✅ **Correct:**
```yaml
rates: [16.5, 16.0, 12.0]  # List format
description: Text here     # String
tax_free: true             # Boolean (lowercase!)
```

❌ **Wrong:**
```yaml
rates: 16.5, 16.0, 12.0    # Missing brackets
description Text here      # Missing colon
tax_free: True             # Capital T (YAML prefers lowercase)
```

### **Indentation Matters:**
```yaml
cbr_scenarios:          # No indent
  base:                 # 2 spaces
    rates: [...]        # 4 spaces
    description: |      # 4 spaces
      Text              # 6 spaces
```

---

## 🎯 **WORKFLOW:**

```
MONTHLY: Check market conditions
    ↓
QUARTERLY: Update forecasts in forecasts_config.yaml
    ↓
PUSH: git push (cloud auto-updates)
    ↓
ANNUALLY: Add/remove instruments in instruments_config.yaml
    ↓
ALWAYS: Test locally before pushing!
```

---

## 📊 **CURRENT STATUS:**

✅ **instruments_config.yaml** - 4 instruments defined  
✅ **forecasts_config.yaml** - All forecasts configured  
✅ **config_loader.py** - Loader working  
✅ **portfolio_optimizer.py** - Reads from YAML  

**System tested and working!** ✅

---

## 🚀 **TO UPDATE YOUR CLOUD APP:**

```bash
cd /Users/sergeynosov/AI_projects/Hedge_Fund

# Commit all config files
git add instruments_config.yaml forecasts_config.yaml config_loader.py
git commit -m "Add modular YAML configuration system"
git push

# Cloud updates in ~1 minute!
```

---

## ✅ **BENEFITS:**

1. **Easy Updates** - Edit YAML, not Python code
2. **Clear Structure** - Instruments separate from forecasts
3. **Version Controlled** - Track all forecast changes
4. **Safe** - Can't break code with forecast updates
5. **Documented** - Comments explain everything
6. **Flexible** - Add/remove instruments easily

**Now you can update forecasts quarterly without touching any code!** 🎉

---

*See instruments_config.yaml and forecasts_config.yaml for the actual configurations*  
*Update forecasts quarterly, instruments annually*

