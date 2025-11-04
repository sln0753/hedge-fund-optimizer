# 💰 Hedge Fund Portfolio Optimizer

**Professional portfolio optimization with real forecasts, tax efficiency, and beautiful web interface**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.51.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 Features

- 📊 **Portfolio Optimization** using SLSQP algorithm
- 🌐 **Interactive Web Interface** with Streamlit + Plotly
- 📈 **Real Professional Forecasts** (CBR rates, USD/RUB)
- 💰 **Tax Optimization** (13% NDFL, tax-free instruments)
- 🎯 **5-Year Projections** with multiple scenarios
- 🔐 **Password Protected** web access
- 📱 **Responsive Design** (works on tablets)
- ☁️ **Cloud Ready** - Deploy to Streamlit Cloud in minutes

---

## 🚀 Quick Start

### Local Installation:

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/hedge-fund-optimizer.git
cd hedge-fund-optimizer

# Install dependencies
pip install -r requirements.txt

# Launch web app
streamlit run web_app.py
```

**App opens at:** http://localhost:8501

**Default credentials:**
- Username: `admin`
- Password: `portfolio2025` (change in `.streamlit/secrets.toml`)

---

## ☁️ Cloud Deployment

**Deploy to Streamlit Cloud (FREE!):**

1. Fork this repository
2. Go to https://share.streamlit.io/
3. Connect your GitHub account
4. Select this repository
5. Set `web_app.py` as main file
6. Configure secrets (password)
7. Deploy!

**Detailed guide:** See [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md)

---

## 📊 What It Does

### Optimal Portfolio Allocation:
Recommends how to distribute your capital across 8 instruments:

**Ruble Instruments (5):**
- Tax-free OFZ bonds (15.2%, 14.8% yield)
- CBR-linked deposit (16.0% yield)
- Bond ETF (13.5% yield)
- Structured bond (15.36% yield)

**USD Instruments (3):**
- Eurobonds (5.5% yield)
- USD deposits (3.0% yield)
- USD cash position

### Real Forecasts (Nov 2025):
- **CBR Rate:** 16.5% → 12.0% (2026) → 10.0% (2027+)
- **USD/RUB:** 81.17 → 83.00 (2025) → 92-100 (2026+)

### Results (Base Scenario):
- **Monthly Income:** 69,970 руб (140% of 50,000 target)
- **5-Year Growth:** +87.2%
- **Tax Savings:** ~36,500 руб/year
- **Risk Profile:** 76% low-risk instruments

---

## 🖥️ Screenshots

### Web Interface:
![Portfolio Recommendations](https://via.placeholder.com/800x400?text=Portfolio+Recommendations+Tab)

### 5-Year Forecast:
![Forecast Chart](https://via.placeholder.com/800x400?text=5-Year+Forecast+Chart)

### Scenario Comparison:
![Scenario Comparison](https://via.placeholder.com/800x400?text=Scenario+Comparison)

---

## 🎯 Use Cases

1. **Retirement Planning** - Ensure sustainable income
2. **Wealth Preservation** - Capital growth + income
3. **Tax Optimization** - Maximize after-tax returns
4. **Scenario Analysis** - Plan for different outcomes
5. **Investment Strategy** - Professional recommendations

---

## 📁 Project Structure

```
hedge-fund-optimizer/
├── web_app.py                    # Web interface (main app)
├── portfolio_optimizer.py        # Optimization engine
├── requirements.txt              # Dependencies
├── .streamlit/
│   ├── config.toml               # App configuration
│   ├── secrets.toml             # Passwords (gitignored)
│   └── secrets.toml.example     # Template
├── test_optimizer.py            # Test suite
├── monthly_dividends_report.py  # Income report
├── investment_distribution.py   # Allocation report
├── README.md                    # Documentation
├── CLOUD_DEPLOYMENT.md          # Deployment guide
└── WEB_APP_GUIDE.md            # User guide
```

---

## 🛠️ Technology Stack

- **Python 3.11** - Core language
- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **SciPy** - Optimization (SLSQP)
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

---

## 📊 Web Interface Tabs

### 1. 📊 Recommendations
- Optimal portfolio allocation
- Investment amounts per instrument
- Tax efficiency metrics
- Interactive pie charts

### 2. 📈 Forecast
- 5-year capital projections
- Monthly income trends
- Sustainability analysis
- Line & bar charts

### 3. 💵 Monthly Payments
- Dividend/coupon breakdown
- Payment schedules
- Cash flow visualization

### 4. 🎯 Distribution
- Currency split (RUB/USD)
- Risk level analysis
- Tax savings estimate

### 5. 📋 Scenario Comparison
- Compare 5 scenarios
- Best/worst case analysis
- Comparative charts

---

## 🔐 Security

- ✅ Password authentication
- ✅ Credentials in secrets (not code)
- ✅ HTTPS on cloud deployment
- ✅ No data sent externally
- ✅ Session-based authentication

---

## 📈 Example Results

**Initial Capital:** 4.8M руб (4M RUB + $10K USD)  
**Target Income:** 50,000 руб/month  

**Recommendations:**
```
ОФЗ-25083:        18.5%  (889K руб)  - Tax-free
ОФЗ-26231:        18.1%  (869K руб)  - Tax-free
Вклад Сбер:       17.1%  (824K руб)  - CBR-linked
Structured Bond:  16.5%  (796K руб)
Bond ETF:         14.8%  (713K руб)
USD Instruments:  15.0%  (721K руб / $8,888)
```

**5-Year Projection:**
- Year 1: 5.4M руб, 49K руб/month (99% coverage)
- Year 2: 6.1M руб, 57K руб/month (113% coverage) ✅
- Year 3: 6.9M руб, 69K руб/month (138% coverage) ✅
- Year 4: 7.9M руб, 80K руб/month (160% coverage) ✅
- Year 5: 9.0M руб, 95K руб/month (190% coverage) ✅

**Tax Efficiency:** 38.9% in tax-free instruments → ~36K руб/year saved

---

## 🧪 Testing

```bash
# Run comprehensive test suite
python test_optimizer.py

# All tests pass ✅
# - Optimization convergence
# - Portfolio simulation
# - Tax calculations
# - Constraint satisfaction
```

---

## 📚 Documentation

- **README.md** - This file
- **WEB_APP_GUIDE.md** - Web interface user guide
- **CLOUD_DEPLOYMENT.md** - Cloud deployment instructions
- **QUICK_START.md** - Command reference
- **UPDATE_SUMMARY.md** - Real forecast details
- **PROJECT_OVERVIEW.md** - Complete overview

---

## 🔄 Updates

**To update forecasts:**

1. Edit `portfolio_optimizer.py`
2. Update `self.cbr_scenarios['base']` (CBR rates)
3. Update `self.fx_scenarios['base']` (USD/RUB)
4. Run tests: `python test_optimizer.py`
5. Push to GitHub (cloud auto-updates)

---

## ⚠️ Disclaimer

**This is NOT individual investment advice.**

- Results based on forecast data (not guaranteed)
- Consult financial advisor before investing
- Past performance ≠ future results
- Consider your personal risk tolerance
- Tax rules may change

For informational and educational purposes only.

---

## 📞 Support

- **Issues:** Open an issue on GitHub
- **Questions:** See documentation in `/docs`
- **Tests:** Run `python test_optimizer.py`

---

## 📄 License

MIT License - See LICENSE file

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🌟 Star History

If you find this useful, please star the repository! ⭐

---

## 🔗 Links

- **Demo:** [Live Demo](https://YOUR_APP.streamlit.app) (after deployment)
- **Docs:** [Full Documentation](docs/)
- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/hedge-fund-optimizer/issues)

---

## 👤 Author

**Sergey Nosov**

- Portfolio Optimization System
- Real Professional Forecasts Integration
- Modern Web Interface with Authentication

---

## 🎉 Acknowledgments

- Streamlit team for amazing framework
- Professional analysts for forecast data
- SciPy for optimization algorithms
- Plotly for beautiful charts

---

**Built with ❤️ for smart investing**

*Version 1.0 - November 2, 2025*


