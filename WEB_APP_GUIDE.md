# 🌐 Web Interface Guide - Portfolio Optimizer

## 🚀 Quick Start

### Launch the Web App:

```bash
cd /Users/sergeynosov/AI_projects/Hedge_Fund
streamlit run web_app.py
```

The app will automatically open in your browser at **http://localhost:8501**

---

## 📱 Features

### 🎛️ **Sidebar - Settings Panel**

**Portfolio Parameters:**
- Рублевый капитал (RUB capital)
- Валютный капитал (USD capital) 
- Курс USD/RUB (Exchange rate)
- Целевой месячный доход (Target monthly income)
- Горизонт планирования (Planning horizon in years)

**Scenario Selection:**
- Изменение капитала (Capital growth/decline)
- Ставка ЦБ (Central Bank rate scenarios)
- Курс валют (Currency rate scenarios)

**💾 Apply Settings** button to update calculations

---

### 📊 **Tab 1: Рекомендации (Recommendations)**

**What you see:**
- Optimal portfolio allocation table
- Investment amounts for each instrument
- Before/after-tax yields
- Tax status (tax-free vs taxable)

**Interactive Charts:**
- 🥧 Pie chart: Distribution by instruments
- 🥧 Pie chart: Distribution by instrument types

**Key Metrics:**
- Capital allocation percentages
- Expected yields
- Tax efficiency

---

### 📈 **Tab 2: Прогноз (Forecast)**

**5-Year Projections:**
- Capital growth over time
- Monthly income trends
- Coverage of target income

**Metrics Displayed:**
- Average income coverage (% of target)
- Final capital after 5 years
- Strategy sustainability status

**Interactive Charts:**
- 📈 Line chart: Capital growth year-by-year
- 📊 Bar chart: Monthly income by year
- 🎯 Target income reference line

**Detailed Table:**
- Year-by-year breakdown
- Portfolio yield
- Monthly income
- Coverage percentage

---

### 💵 **Tab 3: Месячные выплаты (Monthly Payments)**

**Income Breakdown:**
- Monthly income by each instrument
- Annual income projections
- Total monthly income
- Target coverage percentage

**Interactive Charts:**
- 📊 Bar chart: Monthly income by instrument (color-coded by amount)

**📅 Payment Schedule:**
- Expandable section showing when each instrument pays out
- OFZ bonds: Semi-annual coupons 🔷
- Deposits: Monthly or capitalization 🟢
- BPIF funds: Reinvestment 🔵
- Structured bonds: Monthly coupons 🟢
- Eurobonds: Semi-annual coupons 🔷

---

### 🎯 **Tab 4: Распределение (Distribution)**

**Currency Distribution:**
- Ruble instruments total
- USD instruments total
- Percentage breakdown
- Visual pie chart

**Risk Analysis:**
- Distribution by risk level (low/medium/high)
- Bar chart visualization
- Risk summary table

**Tax Efficiency:**
- Tax-free instruments (OFZ bonds)
- Taxable instruments
- Annual tax savings estimate
- Success indicator

---

### 📋 **Tab 5: Сравнение сценариев (Scenario Comparison)**

**Automatically compares 5 scenarios:**
1. **База** - Base case (constant capital, base forecasts)
2. **Снижение капитала 5%** - 5% annual capital decline
3. **Рост капитала 5%** - 5% annual capital growth
4. **Пессимистичный** - Pessimistic (high rates, weak ruble)
5. **Оптимистичный** - Optimistic (low rates, strong ruble)

**Comparison Metrics:**
- Average yield (%)
- Average monthly income (руб)
- Final capital after 5 years
- Income coverage (%)

**Interactive Charts:**
- 📊 Bar chart: Monthly income comparison
- 📊 Bar chart: Final capital comparison

---

## 🎨 **User Interface Features**

### **Real-time Updates:**
- All calculations update automatically when you change settings
- Spinners show "Calculating..." during optimization
- Charts are interactive (hover for details, zoom, pan)

### **Responsive Design:**
- Wide layout for maximum screen utilization
- Expandable sections
- Color-coded metrics (green for success, yellow for warning)

### **Visual Indicators:**
- ✅ Green checkmarks for positive outcomes
- ⚠️ Yellow warnings for areas needing attention
- Color-coded charts for easy interpretation

---

## 📊 **Interactive Chart Features**

All Plotly charts support:
- **Hover** - See exact values
- **Zoom** - Click and drag to zoom in
- **Pan** - Shift+drag to move around
- **Reset** - Double-click to reset view
- **Download** - Camera icon to save as PNG
- **Autoscale** - Automatic Y-axis scaling

---

## 💡 **Usage Tips**

### **1. Start with Current Settings:**
- Review the default values in sidebar
- Update with your actual capital amounts
- Set your target monthly income
- Click "Apply Settings"

### **2. Explore Recommendations:**
- Check Tab 1 for optimal allocation
- See which instruments are recommended
- Note the tax-free vs taxable split

### **3. Review Forecast:**
- Tab 2 shows 5-year projections
- Check if income coverage is adequate
- Review capital growth trajectory

### **4. Understand Cash Flow:**
- Tab 3 shows monthly income breakdown
- Review payment schedule (semi-annual vs monthly)
- Plan for irregular cash flows

### **5. Analyze Distribution:**
- Tab 4 shows risk and currency exposure
- Check if diversification is adequate
- Review tax efficiency

### **6. Compare Scenarios:**
- Tab 5 helps with "what-if" analysis
- See best/worst case outcomes
- Choose most likely scenario

---

## 🔄 **Workflow Example**

1. **Launch app** → `streamlit run web_app.py`
2. **Enter your capital** in sidebar (RUB and USD amounts)
3. **Set target income** (e.g., 50,000 руб/month)
4. **Choose scenario** (default: Base scenario)
5. **Click "Apply Settings"**
6. **Review Tab 1** - See recommended allocation
7. **Check Tab 2** - Verify 5-year sustainability
8. **Explore Tab 3** - Understand monthly cash flow
9. **Review Tab 4** - Check risk/currency distribution
10. **Compare Tab 5** - See alternative scenarios

---

## 🎯 **Key Metrics to Watch**

### **In Recommendations Tab:**
- ✅ Tax-free allocation (should be 30-40% for efficiency)
- ✅ USD allocation (should be 10-20% for diversification)
- ✅ Low-risk allocation (should be 60-80%)

### **In Forecast Tab:**
- ✅ Average coverage should be >100%
- ✅ Capital growth should be positive
- ✅ Strategy should show "Устойчива" (Sustainable)

### **In Distribution Tab:**
- ✅ Risk: 70-80% low-risk is ideal
- ✅ Tax savings: Higher is better
- ✅ Liquidity: 60%+ high liquidity recommended

---

## 🛠️ **Troubleshooting**

### **App won't start:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Try running again
streamlit run web_app.py
```

### **Calculations seem wrong:**
- Click "Apply Settings" to refresh
- Check sidebar values are correct
- Try selecting different scenario

### **Charts not showing:**
- Refresh the browser page
- Check console for errors
- Ensure Plotly is installed: `pip install plotly`

### **Port already in use:**
```bash
# Use different port
streamlit run web_app.py --server.port 8502
```

---

## ⌨️ **Keyboard Shortcuts**

- `R` - Rerun the app
- `C` - Clear cache
- `Ctrl/Cmd + Click` - Open link in new tab

---

## 📱 **Mobile/Tablet Support**

The app is responsive and works on:
- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Tablets (iPad, Android tablets)
- ⚠️ Mobile phones (works but some charts may be small)

---

## 🔒 **Security Notes**

- App runs **locally** on your computer
- No data is sent to external servers
- Your financial information stays private
- Default port 8501 is only accessible from your machine

---

## 🎓 **Advanced Features**

### **URL Parameters:**
You can bookmark specific scenarios (Streamlit automatically manages state)

### **Export Data:**
- Use browser "Save Page As" for reports
- Screenshot charts with built-in camera icon
- Copy tables by selecting and Ctrl/Cmd+C

### **Custom Styling:**
The app includes custom CSS for better visual hierarchy and readability

---

## 📞 **Need Help?**

1. **Check console output** for error messages
2. **Review settings** in sidebar - ensure they're realistic
3. **Try base scenario** first before custom scenarios
4. **Check requirements** are installed: `pip list | grep streamlit`

---

## ✅ **Checklist for First Use**

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Navigate to folder: `cd /Users/sergeynosov/AI_projects/Hedge_Fund`
- [ ] Launch app: `streamlit run web_app.py`
- [ ] App opens in browser automatically
- [ ] Update capital amounts in sidebar
- [ ] Set target monthly income
- [ ] Click "Apply Settings"
- [ ] Explore all 5 tabs
- [ ] Review recommendations
- [ ] Compare scenarios

---

## 🎉 **Enjoy Your Portfolio Optimizer Web App!**

**Default URL:** http://localhost:8501  
**Command to run:** `streamlit run web_app.py`

---

*Created with Streamlit + Plotly for interactive financial analysis*  
*Version 1.0 - November 2, 2025*


