import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración inicial
np.random.seed(0)

# Parámetros del movimiento browniano geométrico
mu = 0.01  # Tasa de retorno media (ajustado para un comportamiento más realista)
sigma = 0.02  # Volatilidad del precio

# Número de días para simular
n_days = 365

# Tiempo de simulación (t)
t = np.linspace(0, n_days, n_days)

# Generar el proceso de Wiener
w = np.random.normal(loc=0, scale=sigma, size=n_days)

# Simular los precios con movimiento browniano geométrico
prices = np.cumprod(np.exp(mu * t + sigma * w))  # Usamos cumprod para obtener precios históricos

# Crear un DataFrame de pandas para almacenar los precios simulados
df_simulated_prices = pd.DataFrame({
    'Fecha': pd.date_range(start=datetime.now() - timedelta(days=n_days), periods=n_days),
    'Bitcoin (BTC)': prices,
    'Ethereum (ETH)': prices * 1.5,  # Simulemos una diferencia en el precio
    'Solana (SOL)': prices * 0.8   # Simulemos otra diferencia en el precio
})

# Crear un DataFrame con los precios simulados y formatearlo para mostrar en el gráfico de líneas
df_line_chart = df_simulated_prices[['Fecha', 'Bitcoin (BTC)', 'Ethereum (ETH)', 'Solana (SOL)']].set_index('Fecha')

# Layout del dashboard
st.title("Crypto Analysis Dashboard")

# Panel Lateral con Filtros
start_date = st.sidebar.date_input('Fecha inicial', value=df_simulated_prices['Fecha'].min())
end_date = st.sidebar.date_input('Fecha final', value=df_simulated_prices['Fecha'].max())

# Filtrear los datos según el rango de fechas seleccionado
df_filtered = df_simulated_prices[(df_simulated_prices['Fecha'] >= start_date) & (df_simulated_prices['Fecha'] <= end_date)]

# Gráfico de Líneas Comparativo
st.line_chart(df_filtered[['Bitcoin (BTC)', 'Ethereum (ETH)', 'Solana (SOL)']])

# Cards de Métricas
for i, (crypto, price) in enumerate(df_filtered[['Bitcoin (BTC)', 'Ethereum (ETH)', 'Solana (SOL)']].iloc[-1].items()):
    st.metric(label=crypto, value=f'${price:.2f}', delta=f'+{df_filtered[crypto].pct_change().tail(1).values[0]:.2%} 24h')

# Dependencias externas
# pip install streamlit pandas numpy