# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# titles
st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("AI Stock Analyzer – MVP")
st.markdown("**20 Day Moving Average & RSI BUY/SELL Flag**")

# Sidebar Input
st.sidebar.header("Stock Settings")
ticker = st.sidebar.text_input("Ticker", "MSFT").upper()
period = st.sidebar.selectbox("Time Period", ["1y", "2y", "5y", "max"], index=0)

# Fetch Data & catch missing data
@st.cache_data
def load_data(ticker, period):
    df = yf.download(ticker, period=period)
    if df.empty:
        st.error("No data found. Check ticker.")
        return None
    return df

# Load data
df = load_data(ticker, period)
if df is None:
    st.stop()

# === CALCULATE INDICATORS & SIGNALS ===
df['MA20'] = df['Close'].rolling(20).mean()
delta = df['Close'].diff()
gain = delta.clip(lower=0)
loss = delta.clip(upper=0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean().abs()
RS = avg_gain / avg_loss

df = df.dropna().copy()

df['RSI'] = 100 - (100 / (1 + RS))

RSI_Diff = df['RSI'].diff()
df['RSI_Rising_2D'] = (RSI_Diff > 0) & (RSI_Diff.shift(1) > 0)
df['RSI_Falling_2D'] = (RSI_Diff < 0) & (RSI_Diff.shift(1) < 0)

df['Signal'] = 'HOLD'

close = df['Close'].values.flatten()

buy = (
     (close < df['MA20']) &
     (df['RSI'] < 30) &
     (df['RSI_Rising_2D'])
 )
sell = (
     (close > df['MA20']) &
     (df['RSI'] > 70) &
     (df['RSI_Falling_2D'])
 )

df.loc[buy, 'Signal'] = 'BUY'
df.loc[sell, 'Signal'] = 'SELL'
 
# === PLOT: Price + BUY/SELL Signals ===
fig, ax = plt.subplots(figsize=(14, 7))

# Price line
ax.plot(df.index, df['Close'], label='Close Price', color='black', linewidth=1.5)

# BUY signals (green up arrows)
buy_signals = df['Signal'] == 'BUY'
ax.scatter(df.index[buy_signals], df.loc[buy_signals, 'Close'],
           color='green', marker='^', s=100, label='BUY', zorder=5,
           edgecolors='darkgreen', linewidth=1.2)

# SELL signals (red down arrows)
sell_signals = df['Signal'] == 'SELL'
ax.scatter(df.index[sell_signals], df.loc[sell_signals, 'Close'],
           color='red', marker='v', s=100, label='SELL', zorder=5,
           edgecolors='darkred', linewidth=1.2)

# Styling
ax.set_title(f'{ticker} – BUY/SELL Flags', fontsize=16, fontweight='bold')
ax.set_ylabel('Price ($)', fontsize=12)
ax.set_xlabel('Time', fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

# Show in Streamlit
st.pyplot(fig)
