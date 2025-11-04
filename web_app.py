"""
Portfolio Optimizer - Web Interface
Interactive web application using Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from portfolio_optimizer import DynamicPortfolioOptimizer
import sys

# Page config
st.set_page_config(
    page_title="Hedge Fund Portfolio Optimizer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] == st.secrets["passwords"]["admin_user"] and \
           st.session_state["password"] == st.secrets["passwords"]["admin_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
            del st.session_state["username"]  # Don't store username
        else:
            st.session_state["password_correct"] = False

    # Return True if password is validated
    if st.session_state.get("password_correct", False):
        return True

    # Show login form
    st.markdown('<p class="main-header">🔐 Portfolio Optimizer Login</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px;'>
            <h3>Secure Access Required</h3>
            <p>Please enter your credentials to access the Portfolio Optimizer</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input("Username", key="username", placeholder="Enter username")
        st.text_input("Password", type="password", key="password", placeholder="Enter password")
        st.button("Login", on_click=password_entered, use_container_width=True)
        
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Username or password incorrect")
        
        st.markdown("""
        <div style='text-align: center; margin-top: 2rem; color: #666;'>
            <p><small>🔒 Secure connection | All data encrypted</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    return False

# Check authentication
if not check_password():
    st.stop()  # Stop execution if not authenticated

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    .warning-text {
        color: #ffc107;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = DynamicPortfolioOptimizer()

optimizer = st.session_state.optimizer

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/money-bag.png", width=80)
    st.title("⚙️ Настройки")
    
    st.subheader("Капитал")
    initial_capital_rub = st.number_input(
        "Рублевый капитал (руб)", 
        min_value=100000, 
        value=optimizer.initial_capital_rub,
        step=100000,
        format="%d"
    )
    
    initial_usd_amount = st.number_input(
        "Валютный капитал (USD)", 
        min_value=0, 
        value=optimizer.initial_usd_amount,
        step=1000,
        format="%d"
    )
    
    current_usd_rub = st.number_input(
        "Курс USD/RUB", 
        min_value=50.0, 
        max_value=150.0,
        value=optimizer.current_usd_rub,
        step=0.1,
        format="%.2f"
    )
    
    st.subheader("Целевой доход")
    monthly_income_target = st.number_input(
        "Месячный доход (руб)", 
        min_value=10000, 
        value=optimizer.monthly_income_target,
        step=5000,
        format="%d"
    )
    
    years = st.slider(
        "Горизонт планирования (лет)", 
        min_value=1, 
        max_value=10,
        value=optimizer.years
    )
    
    if st.button("💾 Применить настройки", use_container_width=True):
        optimizer.initial_capital_rub = initial_capital_rub
        optimizer.initial_usd_amount = initial_usd_amount
        optimizer.current_usd_rub = current_usd_rub
        optimizer.monthly_income_target = monthly_income_target
        optimizer.years = years
        st.success("Настройки применены!")
        st.rerun()
    
    st.divider()
    
    st.subheader("Сценарии")
    capital_scenario = st.selectbox(
        "Изменение капитала",
        options=['constant', 'decrease_5', 'decrease_10', 'increase_5', 'increase_10'],
        format_func=lambda x: {
            'constant': 'Постоянный',
            'decrease_5': 'Снижение 5%/год',
            'decrease_10': 'Снижение 10%/год',
            'increase_5': 'Рост 5%/год',
            'increase_10': 'Рост 10%/год'
        }[x]
    )
    
    rate_scenario = st.selectbox(
        "Ставка ЦБ",
        options=['base', 'pessimistic', 'optimistic'],
        format_func=lambda x: {
            'base': 'Базовый',
            'pessimistic': 'Пессимистичный',
            'optimistic': 'Оптимистичный'
        }[x]
    )
    
    fx_scenario = st.selectbox(
        "Курс валют",
        options=['base', 'pessimistic', 'optimistic'],
        format_func=lambda x: {
            'base': 'Базовый',
            'pessimistic': 'Пессимистичный',
            'optimistic': 'Оптимистичный'
        }[x]
    )

# Main header
st.markdown('<p class="main-header">💰 Hedge Fund Portfolio Optimizer</p>', unsafe_allow_html=True)

# Calculate total capital
total_capital = optimizer.initial_capital_rub + optimizer.initial_usd_amount * optimizer.current_usd_rub

# Top metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Общий капитал", f"{total_capital:,.0f} руб")
with col2:
    st.metric("Рублевый капитал", f"{optimizer.initial_capital_rub:,.0f} руб")
with col3:
    st.metric("Валютный капитал", f"${optimizer.initial_usd_amount:,.0f}")
with col4:
    st.metric("Целевой доход", f"{optimizer.monthly_income_target:,.0f} руб/мес")

st.divider()

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Рекомендации", 
    "📈 Прогноз", 
    "💵 Месячные выплаты",
    "🎯 Распределение",
    "📋 Сравнение сценариев",
    "🏦 Инструменты",
    "📅 Прогнозы"
])

# Tab 1: Recommendations
with tab1:
    st.subheader("Оптимальное распределение активов")
    
    with st.spinner("Оптимизация портфеля..."):
        optimal_weights = optimizer.optimize_portfolio(capital_scenario, rate_scenario, fx_scenario)
        
    # Prepare allocation data
    allocation_data = []
    for instrument, weight in optimal_weights.items():
        if weight > 0.01:
            instrument_info = optimizer.instruments[instrument]
            capital_allocated = total_capital * weight
            base_yield = instrument_info['yield']
            adjusted_yield = optimizer.calculate_after_tax_yield(instrument, base_yield, 0, rate_scenario)
            
            if instrument_info['currency'] == 'USD':
                capital_display = f"${capital_allocated/optimizer.current_usd_rub:,.0f}"
            else:
                capital_display = f"{capital_allocated:,.0f} руб"
            
            allocation_data.append({
                'Инструмент': instrument,
                'Тип': instrument_info['type'],
                'Доля': f"{weight*100:.1f}%",
                'Сумма': capital_display,
                'Валюта': instrument_info['currency'],
                'Доходность': f"{base_yield:.1f}%",
                'После налогов': f"{adjusted_yield:.1f}%",
                'Налог': 'Нет' if instrument_info.get('tax_free') else 'НДФЛ 13%',
                'weight': weight,
                'capital_rub': capital_allocated
            })
    
    df_allocation = pd.DataFrame(allocation_data)
    
    # Display table
    st.dataframe(
        df_allocation[['Инструмент', 'Доля', 'Сумма', 'Тип', 'Доходность', 'После налогов', 'Налог']],
        use_container_width=True,
        hide_index=True
    )
    
    # Pie chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Распределение по инструментам")
        fig_pie = px.pie(
            df_allocation,
            values='weight',
            names='Инструмент',
            title='Доли инструментов в портфеле'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Распределение по типам")
        type_summary = df_allocation.groupby('Тип')['capital_rub'].sum().reset_index()
        type_summary.columns = ['Тип', 'Капитал']
        fig_type = px.pie(
            type_summary,
            values='Капитал',
            names='Тип',
            title='Распределение по типам инструментов'
        )
        st.plotly_chart(fig_type, use_container_width=True)

# Tab 2: Forecast
with tab2:
    st.subheader("Прогноз на 5 лет")
    
    with st.spinner("Расчет прогноза..."):
        simulation = optimizer.simulate_portfolio_performance(
            optimal_weights, capital_scenario, rate_scenario, fx_scenario
        )
    
    # Prepare forecast data
    forecast_data = []
    for result in simulation:
        forecast_data.append({
            'Год': result['year'],
            'Капитал (руб)': result['total_capital_end'],
            'Доходность (%)': result['portfolio_yield'],
            'Месячный доход (руб)': result['monthly_income'],
            'Покрытие цели (%)': result['monthly_income'] / optimizer.monthly_income_target * 100
        })
    
    df_forecast = pd.DataFrame(forecast_data)
    
    # Metrics
    avg_coverage = df_forecast['Покрытие цели (%)'].mean()
    final_capital = df_forecast.iloc[-1]['Капитал (руб)']
    capital_growth = (final_capital - total_capital) / total_capital * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Среднее покрытие цели", f"{avg_coverage:.0f}%", 
                 delta=f"{avg_coverage-100:.0f}%" if avg_coverage >= 100 else None)
    with col2:
        st.metric("Итоговый капитал", f"{final_capital:,.0f} руб",
                 delta=f"+{capital_growth:.1f}%")
    with col3:
        status = "✅ Устойчива" if avg_coverage >= 100 and capital_growth >= 0 else "⚠️ Требует внимания"
        st.metric("Стратегия", status)
    
    # Line chart
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=df_forecast['Год'],
        y=df_forecast['Капитал (руб)'],
        mode='lines+markers',
        name='Капитал',
        line=dict(color='#1f77b4', width=3)
    ))
    fig_forecast.update_layout(
        title='Рост капитала',
        xaxis_title='Год',
        yaxis_title='Капитал (руб)',
        hovermode='x unified'
    )
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Income chart
    fig_income = go.Figure()
    fig_income.add_trace(go.Bar(
        x=df_forecast['Год'],
        y=df_forecast['Месячный доход (руб)'],
        name='Месячный доход',
        marker_color='#2ca02c'
    ))
    fig_income.add_hline(
        y=optimizer.monthly_income_target,
        line_dash="dash",
        line_color="red",
        annotation_text="Целевой доход"
    )
    fig_income.update_layout(
        title='Месячный доход по годам',
        xaxis_title='Год',
        yaxis_title='Доход (руб)',
        hovermode='x unified'
    )
    st.plotly_chart(fig_income, use_container_width=True)
    
    # Table
    st.dataframe(df_forecast.style.format({
        'Капитал (руб)': '{:,.0f}',
        'Доходность (%)': '{:.1f}%',
        'Месячный доход (руб)': '{:,.0f}',
        'Покрытие цели (%)': '{:.0f}%'
    }), use_container_width=True, hide_index=True)

# Tab 3: Monthly Payments
with tab3:
    st.subheader("Месячные выплаты дивидендов/купонов")
    
    # Calculate monthly income by instrument
    monthly_data = []
    total_monthly = 0
    
    for item in allocation_data:
        instrument = item['Инструмент']
        capital = item['capital_rub']
        
        # Get adjusted yield
        base_yield = optimizer.instruments[instrument]['yield']
        adjusted_yield = optimizer.calculate_after_tax_yield(instrument, base_yield, 0, rate_scenario)
        
        # Calculate monthly income
        annual_income = capital * adjusted_yield / 100
        monthly_income = annual_income / 12
        total_monthly += monthly_income
        
        monthly_data.append({
            'Инструмент': instrument,
            'Месячный доход': monthly_income,
            'Годовой доход': annual_income
        })
    
    df_monthly = pd.DataFrame(monthly_data)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Месячный доход", f"{total_monthly:,.0f} руб")
    with col2:
        st.metric("Годовой доход", f"{total_monthly*12:,.0f} руб")
    with col3:
        coverage = total_monthly / optimizer.monthly_income_target * 100
        st.metric("Покрытие цели", f"{coverage:.1f}%")
    
    # Bar chart
    fig_monthly = px.bar(
        df_monthly,
        x='Инструмент',
        y='Месячный доход',
        title='Месячный доход по инструментам',
        color='Месячный доход',
        color_continuous_scale='Greens'
    )
    fig_monthly.update_layout(showlegend=False)
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Table
    st.dataframe(df_monthly.style.format({
        'Месячный доход': '{:,.0f} руб',
        'Годовой доход': '{:,.0f} руб'
    }), use_container_width=True, hide_index=True)
    
    # Payment schedule
    with st.expander("📅 График выплат по инструментам"):
        for item in allocation_data:
            instrument = item['Инструмент']
            inst_type = optimizer.instruments[instrument]['type']
            
            if 'ОФЗ' in inst_type:
                frequency = "🔷 2 раза в год (купоны раз в полгода)"
            elif 'Депозит' in inst_type:
                frequency = "🟢 Ежемесячно (или капитализация)"
            elif 'БПИФ' in inst_type:
                frequency = "🔵 Реинвестирование (выплаты при продаже)"
            elif 'Структурная' in inst_type:
                frequency = "🟢 Ежемесячно (структурный купон)"
            elif 'Еврооблигация' in inst_type:
                frequency = "🔷 Полугодовые купоны"
            else:
                frequency = "⚪ По условиям инструмента"
            
            st.write(f"**{instrument}** - {frequency}")

# Tab 4: Distribution
with tab4:
    st.subheader("Распределение инвестиций")
    
    # Currency distribution
    rub_total = sum([item['capital_rub'] for item in allocation_data if optimizer.instruments[item['Инструмент']]['currency'] == 'RUB'])
    usd_total = sum([item['capital_rub'] for item in allocation_data if optimizer.instruments[item['Инструмент']]['currency'] == 'USD'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Рублевые инструменты", f"{rub_total:,.0f} руб", f"{rub_total/total_capital*100:.1f}%")
    with col2:
        st.metric("Валютные инструменты", f"${usd_total/optimizer.current_usd_rub:,.0f}", f"{usd_total/total_capital*100:.1f}%")
    
    # Currency pie chart
    currency_data = pd.DataFrame([
        {'Валюта': 'RUB', 'Сумма': rub_total},
        {'Валюта': 'USD', 'Сумма': usd_total}
    ])
    fig_currency = px.pie(
        currency_data,
        values='Сумма',
        names='Валюта',
        title='Валютное распределение',
        color='Валюта',
        color_discrete_map={'RUB': '#1f77b4', 'USD': '#2ca02c'}
    )
    st.plotly_chart(fig_currency, use_container_width=True)
    
    # Risk distribution
    st.subheader("Распределение по уровню риска")
    risk_summary = {}
    for item in allocation_data:
        risk = optimizer.instruments[item['Инструмент']].get('risk', 'низкий')
        if risk not in risk_summary:
            risk_summary[risk] = 0
        risk_summary[risk] += item['capital_rub']
    
    risk_df = pd.DataFrame([
        {'Риск': risk.capitalize(), 'Сумма': amount, 'Доля': f"{amount/total_capital*100:.1f}%"}
        for risk, amount in risk_summary.items()
    ])
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_risk = px.bar(
            risk_df,
            x='Риск',
            y='Сумма',
            title='Распределение по риску',
            color='Риск',
            color_discrete_map={'Низкий': '#28a745', 'Средний': '#ffc107', 'Высокий': '#dc3545'}
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    with col2:
        st.dataframe(risk_df, use_container_width=True, hide_index=True)
    
    # Tax efficiency
    st.subheader("Налоговая эффективность")
    tax_free = sum([item['capital_rub'] for item in allocation_data if optimizer.instruments[item['Инструмент']].get('tax_free', False)])
    taxable = total_capital - tax_free
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tax-free (ОФЗ)", f"{tax_free:,.0f} руб", f"{tax_free/total_capital*100:.1f}%")
    with col2:
        st.metric("Налогооблагаемые", f"{taxable:,.0f} руб", f"{taxable/total_capital*100:.1f}%")
    
    tax_savings = tax_free * 0.15 * 0.13  # Approximate annual tax savings
    st.success(f"💡 Годовая экономия на налогах за счет ОФЗ: ~{tax_savings:,.0f} руб")

# Tab 5: Scenario Comparison
with tab5:
    st.subheader("Сравнение сценариев")
    
    scenarios = [
        ('constant', 'base', 'base', 'База'),
        ('decrease_5', 'base', 'base', 'Снижение капитала 5%'),
        ('increase_5', 'base', 'base', 'Рост капитала 5%'),
        ('constant', 'pessimistic', 'pessimistic', 'Пессимистичный'),
        ('constant', 'optimistic', 'optimistic', 'Оптимистичный'),
    ]
    
    comparison_data = []
    
    with st.spinner("Сравнение сценариев..."):
        for capital_s, rate_s, fx_s, label in scenarios:
            weights = optimizer.optimize_portfolio(capital_s, rate_s, fx_s)
            sim = optimizer.simulate_portfolio_performance(weights, capital_s, rate_s, fx_s)
            
            avg_yield = sum([r['portfolio_yield'] for r in sim]) / len(sim)
            avg_income = sum([r['monthly_income'] for r in sim]) / len(sim)
            final_cap = sim[-1]['total_capital_end']
            coverage = avg_income / optimizer.monthly_income_target * 100
            
            comparison_data.append({
                'Сценарий': label,
                'Ср. доходность': avg_yield,
                'Ср. месячный доход': avg_income,
                'Итоговый капитал': final_cap,
                'Покрытие расходов': coverage
            })
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Display table
    st.dataframe(df_comparison.style.format({
        'Ср. доходность': '{:.1f}%',
        'Ср. месячный доход': '{:,.0f} руб',
        'Итоговый капитал': '{:,.0f} руб',
        'Покрытие расходов': '{:.0f}%'
    }), use_container_width=True, hide_index=True)
    
    # Comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_comp_income = px.bar(
            df_comparison,
            x='Сценарий',
            y='Ср. месячный доход',
            title='Средний месячный доход',
            color='Ср. месячный доход',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_comp_income, use_container_width=True)
    
    with col2:
        fig_comp_capital = px.bar(
            df_comparison,
            x='Сценарий',
            y='Итоговый капитал',
            title='Итоговый капитал через 5 лет',
            color='Итоговый капитал',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_comp_capital, use_container_width=True)

# Tab 6: Instruments
with tab6:
    st.subheader("🏦 База инвестиционных инструментов")
    
    st.info("📝 Для редактирования инструментов откройте файл: `instruments_config.yaml`")
    
    # Display all instruments
    instruments_list = []
    for name, data in optimizer.instruments.items():
        instruments_list.append({
            'Инструмент': name,
            'Тип': data['type'],
            'Доходность': f"{data['yield']:.2f}%",
            'Валюта': data['currency'],
            'Риск': data.get('risk', 'низкий'),
            'Ликвидность': data.get('liquidity', 'высокая'),
            'Налог': '0%' if data.get('tax_free') else '13% НДФЛ',
            'Особенности': ', '.join([
                'CBR-linked' if data.get('cbr_linked') else '',
                'Переменные купоны' if data.get('variable_coupon') else '',
                'Месячные выплаты' if data.get('monthly_coupon') else ''
            ]).strip(', ') or '-'
        })
    
    df_instruments = pd.DataFrame(instruments_list)
    st.dataframe(df_instruments, use_container_width=True, hide_index=True)
    
    # Show details for each instrument
    st.subheader("Детальная информация по инструментам")
    
    for name, data in optimizer.instruments.items():
        with st.expander(f"📄 {name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Основные параметры:**")
                st.write(f"• Тип: {data['type']}")
                st.write(f"• Базовая доходность: {data['yield']:.2f}%")
                st.write(f"• Валюта: {data['currency']}")
                st.write(f"• Риск: {data.get('risk', 'низкий')}")
            
            with col2:
                st.markdown("**Дополнительно:**")
                st.write(f"• Ликвидность: {data.get('liquidity', 'высокая')}")
                st.write(f"• Налог: {'Освобожден' if data.get('tax_free') else '13% НДФЛ'}")
                st.write(f"• Срок (duration): {data.get('duration', 0)} лет")
            
            # Special features
            if data.get('cbr_linked'):
                st.success("⚡ Доходность автоматически следует за ставкой ЦБ РФ")
            
            if data.get('variable_coupon'):
                st.warning("📊 Переменные месячные купоны (см. вкладку 'Прогнозы')")
            
            if data.get('description'):
                st.markdown("**Описание:**")
                st.write(data['description'])
    
    st.divider()
    st.info("💡 Чтобы добавить новый инструмент, отредактируйте `instruments_config.yaml` и выполните `git push`")

# Tab 7: Forecasts
with tab7:
    st.subheader("📅 Прогнозные данные")
    
    st.info("📝 Для редактирования прогнозов откройте файл: `forecasts_config.yaml`")
    
    # CBR Rate Forecasts
    st.subheader("1️⃣ Прогнозы ключевой ставки ЦБ РФ")
    
    cbr_data = []
    for scenario_name, rates in optimizer.cbr_scenarios.items():
        scenario_display = {
            'base': 'Базовый',
            'pessimistic': 'Пессимистичный',
            'optimistic': 'Оптимистичный'
        }.get(scenario_name, scenario_name)
        
        cbr_data.append({
            'Сценарий': scenario_display,
            'Сейчас': f"{rates[0]:.1f}%",
            'Год 1': f"{rates[1]:.1f}%",
            'Год 2': f"{rates[2]:.1f}%",
            'Год 3': f"{rates[3]:.1f}%",
            'Год 4': f"{rates[4]:.1f}%",
            'Год 5': f"{rates[5]:.1f}%"
        })
    
    df_cbr = pd.DataFrame(cbr_data)
    st.dataframe(df_cbr, use_container_width=True, hide_index=True)
    
    # CBR chart
    cbr_chart_data = []
    for scenario_name, rates in optimizer.cbr_scenarios.items():
        scenario_display = {'base': 'Базовый', 'pessimistic': 'Пессимистичный', 'optimistic': 'Оптимистичный'}.get(scenario_name, scenario_name)
        for year, rate in enumerate(rates):
            cbr_chart_data.append({
                'Год': year,
                'Ставка (%)': rate,
                'Сценарий': scenario_display
            })
    
    df_cbr_chart = pd.DataFrame(cbr_chart_data)
    fig_cbr = px.line(
        df_cbr_chart,
        x='Год',
        y='Ставка (%)',
        color='Сценарий',
        title='Прогноз ключевой ставки ЦБ РФ',
        markers=True
    )
    st.plotly_chart(fig_cbr, use_container_width=True)
    
    st.divider()
    
    # USD/RUB Forecasts
    st.subheader("2️⃣ Прогнозы курса USD/RUB")
    
    fx_data = []
    for scenario_name, rates in optimizer.fx_scenarios.items():
        scenario_display = {
            'base': 'Базовый',
            'pessimistic': 'Пессимистичный',
            'optimistic': 'Оптимистичный'
        }.get(scenario_name, scenario_name)
        
        fx_data.append({
            'Сценарий': scenario_display,
            'Сейчас': f"{rates[0]:.2f}",
            'Год 1': f"{rates[1]:.2f}",
            'Год 2': f"{rates[2]:.2f}",
            'Год 3': f"{rates[3]:.2f}",
            'Год 4': f"{rates[4]:.2f}",
            'Год 5': f"{rates[5]:.2f}"
        })
    
    df_fx = pd.DataFrame(fx_data)
    st.dataframe(df_fx, use_container_width=True, hide_index=True)
    
    # FX chart
    fx_chart_data = []
    for scenario_name, rates in optimizer.fx_scenarios.items():
        scenario_display = {'base': 'Базовый', 'pessimistic': 'Пессимистичный', 'optimistic': 'Оптимистичный'}.get(scenario_name, scenario_name)
        for year, rate in enumerate(rates):
            fx_chart_data.append({
                'Год': year,
                'Курс (руб/$)': rate,
                'Сценарий': scenario_display
            })
    
    df_fx_chart = pd.DataFrame(fx_chart_data)
    fig_fx = px.line(
        df_fx_chart,
        x='Год',
        y='Курс (руб/$)',
        color='Сценарий',
        title='Прогноз курса USD/RUB',
        markers=True
    )
    st.plotly_chart(fig_fx, use_container_width=True)
    
    st.divider()
    
    # Structured Bond Coupons
    st.subheader("3️⃣ Купоны структурной облигации (SBERBCMI)")
    
    if 'Структурная облигация Сбер' in optimizer.instruments:
        struct_bond = optimizer.instruments['Структурная облигация Сбер']
        
        if 'coupon_forecast' in struct_bond:
            coupons = struct_bond['coupon_forecast']
            
            months = [
                'Ноябрь 2025', 'Декабрь 2025', 'Январь 2026', 'Февраль 2026',
                'Март 2026', 'Апрель 2026', 'Май 2026', 'Июнь 2026',
                'Июль 2026', 'Август 2026', 'Сентябрь 2026', 'Октябрь 2026'
            ]
            
            coupon_data = []
            cumulative = 0
            for i, (month, coupon) in enumerate(zip(months, coupons), 1):
                cumulative += coupon
                coupon_data.append({
                    '№': i,
                    'Месяц': month,
                    'Купон': f"{coupon:.2f}%",
                    'Накопительно': f"{cumulative:.2f}%"
                })
            
            df_coupons = pd.DataFrame(coupon_data)
            st.dataframe(df_coupons, use_container_width=True, hide_index=True)
            
            # Coupon bar chart
            fig_coupons = px.bar(
                df_coupons,
                x='Месяц',
                y=[float(c.rstrip('%')) for c in df_coupons['Купон']],
                title='Месячные купоны структурной облигации',
                labels={'y': 'Купон (%)'},
                color=[float(c.rstrip('%')) for c in df_coupons['Купон']],
                color_continuous_scale='Greens'
            )
            fig_coupons.update_xaxes(tickangle=45)
            st.plotly_chart(fig_coupons, use_container_width=True)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Средний купон", f"{sum(coupons)/len(coupons):.2f}%/мес")
            with col2:
                st.metric("Минимум", f"{min(coupons):.2f}%")
            with col3:
                st.metric("Максимум", f"{max(coupons):.2f}%")
            with col4:
                st.metric("Годовой доход", f"{sum(coupons):.2f}%")
            
            st.success("📊 Источник: SBERBCMI Index (https://indices.sberbank-cib.com/?indexid=SBERBCMI)")
        else:
            st.warning("Прогноз купонов не загружен")
    else:
        st.info("Структурная облигация не включена в портфель")
    
    st.divider()
    st.info("💡 Обновляйте прогнозы ежеквартально в файле `forecasts_config.yaml`, затем выполните `git push`")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Hedge Fund Portfolio Optimizer</strong> v1.0</p>
    <p>⚠️ Это не индивидуальная инвестиционная рекомендация. Проконсультируйтесь с финансовым советником.</p>
    <p>Использованы реальные прогнозы профессиональных аналитиков</p>
</div>
""", unsafe_allow_html=True)

