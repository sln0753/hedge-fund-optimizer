# Hedge Fund Portfolio Optimizer

## Overview
Dynamic Portfolio Optimizer for investment portfolio optimization considering:
- Russian Central Bank rate scenarios
- Currency rate scenarios (USD/RUB)
- Capital growth/decline scenarios
- Tax optimization (13% NDFL)
- Various financial instruments

## Features
- **Multi-scenario analysis**: Base, pessimistic, and optimistic forecasts
- **Tax optimization**: Accounts for tax-free instruments (OFZ bonds)
- **Currency diversification**: RUB and USD instruments
- **5-year forecasting**: Long-term portfolio performance simulation
- **Interactive menu**: Easy parameter customization

## Installation

```bash
cd /Users/sergeynosov/AI_projects/Hedge_Fund
pip install -r requirements.txt
```

## Usage

```bash
python portfolio_optimizer.py
```

### Main Menu Options

1. **Текущие рекомендации (Current Recommendations)**
   - Get optimized portfolio allocation for specific scenarios
   - Choose capital, rate, and FX scenarios
   - See detailed 5-year forecast

2. **Сравнение сценариев (Compare Scenarios)**
   - Compare 5 key scenarios side-by-side
   - Analyze average returns and risk

3. **Редактировать параметры (Edit Parameters)**
   - Modify initial capital (RUB and USD)
   - Change current USD/RUB rate
   - Set target monthly income
   - Adjust planning horizon

4. **Показать список инструментов (Show Instruments)**
   - View all available investment instruments
   - See instrument parameters (yield, risk, currency, etc.)

5. **Показать сценарии (Show Scenarios)**
   - View CBR rate scenarios
   - View USD/RUB rate scenarios
   - View capital growth scenarios

6. **Выход (Exit)**

## Scenarios

### Capital Growth Scenarios
- `constant`: No change in capital
- `decrease_5`: 5% annual decrease
- `decrease_10`: 10% annual decrease
- `increase_5`: 5% annual increase
- `increase_10`: 10% annual increase

### CBR Rate Scenarios
- `base`: Moderate rate decline (16% → 8.5%)
- `pessimistic`: Slow rate decline (16% → 11%)
- `optimistic`: Fast rate decline (16% → 6.5%)

### USD/RUB Rate Scenarios
- `base`: Moderate weakening (90 → 102)
- `pessimistic`: Strong weakening (90 → 120)
- `optimistic`: RUB strengthening (90 → 78)

## Investment Instruments

### RUB Instruments
- **ОФЗ-25083**: Russian government bond, 15.2% yield, tax-free
- **ОФЗ-26231**: Russian government bond, 14.8% yield, tax-free
- **Вклад Сбер ЦБ-0.5%**: Sberbank deposit linked to CBR rate
- **Фонд РосОблигаций**: Russian bond ETF (BPIF)
- **Структурная облигация Сбер**: Structured bond with monthly coupons

### USD Instruments
- **Сбер-еврообл-2025**: Sberbank eurobond, 5.5% yield
- **Депозит Сбер USD**: Sberbank USD deposit, 3.0% yield
- **USD CASH**: Currency position

## Example Output

```
================================================================================
РЕКОМЕНДАЦИИ ПО ПОРТФЕЛЮ
Сценарий изменения капитала: constant
Сценарий ставок: base
Сценарий курса: base
================================================================================

📊 ОПТИМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ АКТИВОВ:

Рублевые инструменты:
Инструмент          Доля   Сумма          Тип                 Валюта  Доходность
ОФЗ-25083           15.2%  745,200 руб.   ОФЗ                 RUB     15.2%
Вклад Сбер ЦБ-0.5%  25.0%  1,225,000 руб. Депозит             RUB     15.5%

📈 ПРОГНОЗ НА 5 ЛЕТ:
Год  Капитал, руб   Доходность  Месячный доход  Покрытие расходов  Доля USD
1    4,900,000      14.2%       57,916          ✅ ПОЛНОЕ          20.0%
2    4,950,450      13.8%       56,875          ✅ ПОЛНОЕ          19.8%
...
```

## Optimization Algorithm

The optimizer uses:
- **Objective function**: Minimizes income shortfall, capital decline, and concentration risk
- **Constraints**: Sum of weights = 1, instrument-specific limits
- **Method**: Sequential Least Squares Programming (SLSQP)

## Important Notes

⚠️ **Disclaimer**:
- This is NOT individual investment advice
- Results based on forecast data (not guaranteed)
- Consult with a financial advisor before making investment decisions
- Historical performance doesn't guarantee future returns
- Consider your personal risk profile

## Author
Sergey Nosov

## License
Personal project for portfolio optimization research

