#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  💰 CRYPTO DASHBOARD - Financial Analysis Platform                          ║
║  Real-time cryptocurrency price analysis with Streamlit                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════════════════
# 📊 PAGE CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyberpunk theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    .stMetric {
        background-color: rgba(0, 255, 159, 0.05);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00ff9f;
    }
    h1 {
        color: #00ff9f;
        text-shadow: 0 0 10px rgba(0, 255, 159, 0.8);
    }
    h2, h3 {
        color: #ff00ff;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 🎲 SYNTHETIC DATA GENERATION
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def generate_crypto_data(days=30):
    """
    Generate realistic synthetic cryptocurrency price data using Geometric Brownian Motion.
    
    Args:
        days: Number of days to simulate
        
    Returns:
        DataFrame with dates and prices for BTC, ETH, SOL
    """
    np.random.seed(42)  # For reproducibility
    
    # Starting prices (realistic as of 2025)
    start_prices = {
        'Bitcoin': 45000,
        'Ethereum': 2500,
        'Solana': 100
    }
    
    # Volatility parameters (annual volatility)
    volatilities = {
        'Bitcoin': 0.60,    # 60% annual volatility
        'Ethereum': 0.75,   # 75% annual volatility
        'Solana': 1.20      # 120% annual volatility (more volatile)
    }
    
    # Drift (expected daily return)
    drift = {
        'Bitcoin': 0.0003,
        'Ethereum': 0.0005,
        'Solana': 0.0008
    }
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate prices using Geometric Brownian Motion
    data = {'Date': dates}
    
    for crypto in ['Bitcoin', 'Ethereum', 'Solana']:
        # Daily volatility (annual vol / sqrt(252 trading days))
        daily_vol = volatilities[crypto] / np.sqrt(252)
        
        # Generate random returns
        returns = np.random.normal(
            loc=drift[crypto],
            scale=daily_vol,
            size=days
        )
        
        # Generate price path
        prices = [start_prices[crypto]]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        data[crypto] = prices
    
    df = pd.DataFrame(data)
    return df


# ══════════════════════════════════════════════════════════════════════════════
# 📈 METRICS CALCULATION
# ══════════════════════════════════════════════════════════════════════════════

def calculate_metrics(df, crypto):
    """Calculate financial metrics for a cryptocurrency."""
    prices = df[crypto].values
    
    # Current price
    current_price = prices[-1]
    
    # 24h change
    if len(prices) >= 2:
        change_24h = ((prices[-1] - prices[-2]) / prices[-2]) * 100
    else:
        change_24h = 0
    
    # ROI from start of period
    roi = ((prices[-1] - prices[0]) / prices[0]) * 100
    
    # Volatility (standard deviation of daily returns)
    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns) * 100  # As percentage
    
    return {
        'current_price': current_price,
        'change_24h': change_24h,
        'roi': roi,
        'volatility': volatility
    }


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # Header
    st.title("💰 Crypto Analysis Dashboard")
    st.markdown("**Real-time cryptocurrency price analysis** | Powered by Neo-Tokyo Dev v3.0")
    
    # Sidebar
    st.sidebar.title("📊 Filters")
    st.sidebar.markdown("---")
    
    # Generate full dataset (30 days)
    full_df = generate_crypto_data(days=30)
    
    # Date range filter
    min_date = full_df['Date'].min().date()
    max_date = full_df['Date'].max().date()
    
    start_date = st.sidebar.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )
    
    end_date = st.sidebar.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    filtered_df = full_df[
        (full_df['Date'].dt.date >= start_date) &
        (full_df['Date'].dt.date <= end_date)
    ].copy()
    
    if filtered_df.empty:
        st.error("❌ No data available for selected date range")
        return
    
    # Crypto selector
    st.sidebar.markdown("---")
    selected_cryptos = st.sidebar.multiselect(
        "Select Cryptocurrencies",
        options=['Bitcoin', 'Ethereum', 'Solana'],
        default=['Bitcoin', 'Ethereum', 'Solana']
    )
    
    # ──────────────────────────────────────────────────────────────────
    # METRICS CARDS
    # ──────────────────────────────────────────────────────────────────
    
    st.markdown("## 📊 Key Metrics")
    
    cols = st.columns(3)
    
    for idx, crypto in enumerate(['Bitcoin', 'Ethereum', 'Solana']):
        metrics = calculate_metrics(filtered_df, crypto)
        
        with cols[idx]:
            # Icon based on crypto
            icons = {'Bitcoin': '₿', 'Ethereum': 'Ξ', 'Solana': '◎'}
            
            st.markdown(f"### {icons[crypto]} {crypto}")
            
            st.metric(
                label="Current Price",
                value=f"${metrics['current_price']:,.2f}",
                delta=f"{metrics['change_24h']:+.2f}% (24h)"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="ROI",
                    value=f"{metrics['roi']:+.2f}%"
                )
            with col2:
                st.metric(
                    label="Volatility",
                    value=f"{metrics['volatility']:.2f}%"
                )
    
    st.markdown("---")
    
    # ──────────────────────────────────────────────────────────────────
    # PRICE CHART
    # ──────────────────────────────────────────────────────────────────
    
    st.markdown("## 📈 Price Comparison")
    
    if selected_cryptos:
        # Create interactive chart with Plotly
        fig = go.Figure()
        
        colors = {
            'Bitcoin': '#f7931a',    # Orange
            'Ethereum': '#627eea',   # Blue
            'Solana': '#00ff9f'      # Green (neon)
        }
        
        for crypto in selected_cryptos:
            fig.add_trace(go.Scatter(
                x=filtered_df['Date'],
                y=filtered_df[crypto],
                mode='lines',
                name=crypto,
                line=dict(color=colors[crypto], width=3)
            ))
        
        fig.update_layout(
            title="Price History",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode='x unified',
            template='plotly_dark',
            height=500,
            plot_bgcolor='rgba(10, 14, 39, 0.8)',
            paper_bgcolor='rgba(10, 14, 39, 0.8)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Please select at least one cryptocurrency")
    
    # ──────────────────────────────────────────────────────────────────
    # DATA TABLE
    # ──────────────────────────────────────────────────────────────────
    
    st.markdown("## 📋 Raw Data")
    
    with st.expander("View Price Data"):
        display_df = filtered_df.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        
        # Format prices
        for crypto in ['Bitcoin', 'Ethereum', 'Solana']:
            display_df[crypto] = display_df[crypto].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(display_df, use_container_width=True)
    
    # ──────────────────────────────────────────────────────────────────
    # STATISTICS
    # ──────────────────────────────────────────────────────────────────
    
    st.markdown("## 📊 Period Statistics")
    
    stats_cols = st.columns(3)
    
    for idx, crypto in enumerate(['Bitcoin', 'Ethereum', 'Solana']):
        prices = filtered_df[crypto].values
        
        with stats_cols[idx]:
            st.markdown(f"### {crypto}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Max Price", f"${np.max(prices):,.2f}")
                st.metric("Avg Price", f"${np.mean(prices):,.2f}")
            with col2:
                st.metric("Min Price", f"${np.min(prices):,.2f}")
                st.metric("Std Dev", f"${np.std(prices):,.2f}")
    
    # Footer
    st.markdown("---")
    st.markdown("**💡 Note:** All data is synthetically generated using Geometric Brownian Motion")
    st.markdown("**🔮 Powered by Neo-Tokyo Dev v3.0** | Financial Dashboard Boss Fight #1")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()

