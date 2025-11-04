# 📐 Instrument Calculation Formulas

## Overview

This document explains **exactly** how each investment instrument's return is calculated in the portfolio optimizer.

---

## 🧮 **General Formula Structure**

All instruments follow this calculation flow:

```
1. Base Yield
   ↓
2. Dynamic Adjustments (if applicable)
   ↓
3. Tax Calculation (13% NDFL)
   ↓
4. Currency Adjustment (USD instruments)
   ↓
5. Final After-Tax Yield
```

---

## 💰 **1. Вклад Сбер ЦБ-0.5% (Sberbank CBR-Linked Deposit)**

### **Parameters:**
```python
'yield': 16.0%           # Current base (CBR 16.5% - 0.5%)
'cbr_linked': True       # DYNAMIC - follows CBR rate
'tax_free': False        # Subject to 13% NDFL
'currency': 'RUB'
```

### **Formula:**

**Step 1: Dynamic Yield Adjustment**
```
Deposit_Yield[year] = CBR_Rate[year] - 0.5%
```

**Step 2: Tax Calculation**
```
After_Tax_Yield = Deposit_Yield × (1 - 0.13)
                = Deposit_Yield × 0.87
```

### **Example Calculation (5 years):**

| Year | CBR Rate (Forecast) | Deposit Rate | After Tax (13%) | On 1.8M руб |
|------|---------------------|--------------|-----------------|-------------|
| 1 | 16.5% | 16.0% | **13.92%** | 250,560 руб/year |
| 2 | 16.0% | 15.5% | **13.49%** | 242,820 руб/year |
| 3 | 12.0% | 11.5% | **10.01%** | 180,180 руб/year |
| 4 | 10.0% | 9.5% | **8.27%** | 148,860 руб/year |
| 5 | 10.0% | 9.5% | **8.27%** | 148,860 руб/year |

**Code Reference:**
```python
# Lines 78-80
if instrument_data.get('cbr_linked', False):
    cbr_rate = self.cbr_scenarios[scenario][year]
    base_yield = cbr_rate - 0.5
```

**Key Feature:** Yield **automatically tracks CBR rate** - no manual updates needed!

---

## 📊 **2. Фонд РосОблигаций (Russian Bond ETF - BPIF)**

### **Parameters:**
```python
'yield': 13.5%           # FIXED yield estimate
'tax_free': False        # Subject to 13% NDFL
'currency': 'RUB'
'management_fee': 0.5%   # Already included in yield
```

### **Formula:**

**Simple Tax Calculation:**
```
After_Tax_Yield = Base_Yield × (1 - 0.13)
                = 13.5% × 0.87
                = 11.745%
```

### **Example Calculation:**

```
Investment: 1,500,000 руб
Base yield: 13.5%
Gross income: 1,500,000 × 13.5% = 202,500 руб
Tax (13%): 202,500 × 0.13 = 26,325 руб
NET income: 202,500 - 26,325 = 176,175 руб/year
Monthly: 176,175 / 12 = 14,681 руб/month
```

**Note:** Management fee (0.5%) is already reflected in the 13.5% yield estimate.

---

## 🎲 **3. Структурная облигация Сбер (Structured Bond)**

### **Parameters:**
```python
'yield': 15.36%          # FIXED expected yield
'tax_free': False        # Subject to 13% NDFL
'currency': 'RUB'
'monthly_coupon': True   # Monthly payments
```

### **Formula:**

**Tax Calculation:**
```
After_Tax_Yield = Base_Yield × (1 - 0.13)
                = 15.36% × 0.87
                = 13.36%
```

### **Example Calculation:**

```
Investment: 800,000 руб
Annual gross: 800,000 × 15.36% = 122,880 руб
Tax: 122,880 × 0.13 = 15,974 руб
Net annual: 122,880 - 15,974 = 106,906 руб
Monthly coupon: 106,906 / 12 = 8,909 руб
```

**Note:** Actual coupon may vary based on structured product conditions.

---

## 🌍 **4. Сбер-еврообл-2025 (Sberbank Eurobond)**

### **Parameters:**
```python
'yield': 5.5%            # USD yield
'tax_free': False        # Subject to 13% NDFL
'currency': 'USD'        # USD-denominated
```

### **Formula:**

**Step 1: Interest After Tax**
```
Interest_After_Tax = USD_Yield × (1 - 0.13)
                   = 5.5% × 0.87
                   = 4.785%
```

**Step 2: Currency Gain/Loss**
```
FX_Gain = (USD/RUB[future] - USD/RUB[current]) / USD/RUB[current] × 100
```

**Step 3: Total Return in RUB**
```
Total_Return_RUB = Interest_After_Tax + FX_Gain
```

### **Example Calculation (Year 3):**

```
Investment: $5,000 (at 81.17 = 405,850 руб)

Interest income (USD):
  $5,000 × 5.5% = $275 gross
  Tax: $275 × 0.13 = $35.75
  Net: $275 - $35.75 = $239.25 USD/year
  
Currency appreciation:
  Start: 81.17 руб/$
  Year 3: 92.00 руб/$
  Initial value: $5,000 × 81.17 = 405,850 руб
  Year 3 value: $5,000 × 92.00 = 460,000 руб
  FX gain: 460,000 - 405,850 = 54,150 руб
  
Total return in RUB:
  Interest: $239.25 × 92 = 22,011 руб
  FX gain: 54,150 руб
  TOTAL: 76,161 руб (18.77% of initial 405,850)
  
Components:
  Interest: 4.785% (in USD terms)
  FX gain: 13.35%
  TOTAL: 18.14% in RUB terms 🎯
```

---

## 💵 **5. Депозит Сбер USD (USD Deposit)**

### **Formula:**

Same as Eurobond:
```
Total_Return = (USD_Interest × 0.87) + FX_Gain
             = (3.0% × 0.87) + FX_Gain
             = 2.61% + FX_Gain
```

### **Example (Year 1):**
```
Deposit: $3,000
Interest: 3.0% × 0.87 = 2.61%
FX gain: (83.00 - 81.17) / 81.17 = 2.25%
Total: 4.86% in RUB terms
```

---

## 💵 **6. USD CASH (Currency Hedge)**

### **Formula:**

```
Total_Return = 0% + FX_Gain
```

**Pure currency play** - no interest, only exchange rate changes.

### **Example (Year 3):**
```
Holding: $2,000
Interest: 0%
FX gain: (92.00 - 81.17) / 81.17 = 13.35%

If dollar rises:
  Initial: $2,000 × 81.17 = 162,340 руб
  Year 3: $2,000 × 92.00 = 184,000 руб
  Gain: 21,660 руб (13.35%)
```

---

## 🎓 **Tax Calculation Detail:**

### **Russian Tax Law (NDFL):**

**Interest/Coupon Income:**
```
Tax rate: 13% (НДФЛ)
Net income = Gross × (1 - 0.13)
           = Gross × 0.87
```

**Tax-Free Exceptions:**
- OFZ bond coupons (removed from your portfolio)
- Currency exchange gains (if held >3 years)
- Some qualified dividends

**In Your Portfolio:**
- 3 instruments are taxable (Sber deposit, Bond fund, Structured bond)
- 3 USD instruments are taxable (on interest, not FX gains)

---

## 🧮 **Portfolio Return Calculation:**

**Total Portfolio Return:**
```python
# Lines 120-134
for instrument, weight in weights.items():
    adjusted_yield = calculate_after_tax_yield(instrument, base_yield, year, scenario)
    instrument_contribution = weight × adjusted_yield / 100
    portfolio_yield += instrument_contribution
    monthly_income += (total_capital × weight × adjusted_yield / 100) / 12

annual_income = total_capital × portfolio_yield
```

**In Plain Math:**
```
Portfolio_Yield = Σ (Weight[i] × After_Tax_Yield[i])

Monthly_Income = Total_Capital × Portfolio_Yield / 12

Annual_Income = Total_Capital × Portfolio_Yield
```

---

## 📊 **Summary Table:**

| Instrument | Yield Type | Tax Treatment | Currency Effect | Formula Complexity |
|------------|------------|---------------|-----------------|-------------------|
| Вклад Сбер | **Dynamic** | Taxable | None | ⭐⭐⭐ (CBR-linked) |
| Фонд РосОблигаций | Fixed | Taxable | None | ⭐ (simple) |
| Структурная обл. | Fixed | Taxable | None | ⭐ (simple) |
| Сбер-еврообл | Fixed | Taxable | **FX gain** | ⭐⭐⭐ (two components) |
| Депозит USD | Fixed | Taxable | **FX gain** | ⭐⭐⭐ (two components) |
| USD CASH | Zero | Tax-free | **Pure FX** | ⭐⭐ (FX only) |

---

## 💡 **Key Insights:**

1. **Sberbank deposit is SMART** - auto-adjusts to CBR rate
2. **USD instruments have TWO returns** - interest + currency gain
3. **Tax reduces yield by ~13%** on all taxable instruments
4. **Currency can boost or hurt** USD instruments significantly
5. **Formulas are TRANSPARENT** - you can verify every calculation

---

## 🔧 **How to Verify Calculations:**

You can manually check any instrument:

```python
from portfolio_optimizer import DynamicPortfolioOptimizer

optimizer = DynamicPortfolioOptimizer()

# Check Sberbank deposit in year 3
yield_year3 = optimizer.calculate_after_tax_yield(
    'Вклад Сбер ЦБ-0.5%', 
    16.0,     # base yield (will be recalculated)
    year=2,   # Year 3 (0-indexed)
    scenario='base'
)
print(f"Sber deposit Year 3 yield: {yield_year3:.2f}%")
# Output: 10.01% (CBR 12% - 0.5% = 11.5%, then × 0.87 = 10.01%)
```

---

## ✅ **All Formulas Are:**

- ✅ **Transparent** - Open source, visible in code
- ✅ **Verifiable** - You can check manually
- ✅ **Tested** - Comprehensive test suite
- ✅ **Realistic** - Based on real tax laws and market behavior
- ✅ **Dynamic** - CBR-linked deposits adjust automatically

---

*Reference: portfolio_optimizer.py, lines 73-95*  
*Last updated: November 3, 2025*

