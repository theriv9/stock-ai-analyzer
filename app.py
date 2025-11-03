# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("AI Stock Analyzer – MVP")
st.markdown("**Your logic. Your code. Now live.**")

# Sidebar Input
st.sidebar.header("Stock Settings")
ticker = st.sidebar.text_input("Ticker", "MSFT").upper()
period = st.sidebar.selectbox("Time Period", ["1y", "2y", "5y", "max"], index=0)

# Fetch Data
@st.cache_data
def load_data(ticker, period):
    df = yf.download(ticker, period=period)
    if df.empty:
        st.error("No data found. Check ticker.")
        return None
    return df

df = load_data(ticker, period)
if df is None:
    st.stop()

# # === YOUR EXACT CODE BELOW ===
# df['MA20'] = df['Close'].rolling(20).mean()

# delta = df['Close'].diff()
# gain = delta.clip(lower=0)
# loss = delta.clip(upper=0)
# avg_gain = gain.rolling(14).mean()
# avg_loss = loss.rolling(14).mean().abs()
# RS = avg_gain / avg_loss

# df = df.dropna().copy()

# df['RSI'] = 100 - (100 / (1 + RS))

# RSI_Diff = df['RSI'].diff()
# df['RSI_Rising_2D'] = (RSI_Diff > 0) & (RSI_Diff.shift(1) > 0)
# df['RSI_Falling_2D'] = (RSI_Diff < 0) & (RSI_Diff.shift(1) < 0)

# df['Signal'] = 'HOLD'

# close = df['Close'].values.flatten()

# buy = (
#     (close < df['MA20']) &
#     (df['RSI'] < 30) &
#     (df['RSI_Rising_2D'])
# )
# sell = (
#     (close > df['MA20']) &
#     (df['RSI'] > 70) &
#     (df['RSI_Falling_2D'])
# )

# df.loc[buy, 'Signal'] = 'BUY'
# df.loc[sell, 'Signal'] = 'SELL'
# # === END OF YOUR CODE ===

# # Latest Signal
# latest = df.iloc[-1]
# signal = latest['Signal']
# color = {"BUY": "green", "SELL": "red", "HOLD": "gray"}[signal]

# st.markdown(f"## **{ticker} → {signal}**")
# st.markdown(f"<h2 style='color: {color};'>LATEST: {signal}</h2>", unsafe_allow_html=True)

# col1, col2, col3 = st.columns(3)
# col1.metric("Close", f"${latest['Close']:.2f}")
# col2.metric("MA20", f"${latest['MA20']:.2f}")
# col3.metric("RSI", f"{latest['RSI']:.1f}")

# # === YOUR PLOT (enhanced) ===
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

# # Price + MA20
# ax1.plot(df.index, df['Close'], label='Close', color='black', linewidth=1.2)
# ax1.plot(df.index, df['MA20'], label='MA20', color='orange', linewidth=1.5)

# # BUY/SELL Markers
# buy_signals = df['Signal'] == 'BUY'
# sell_signals = df['Signal'] == 'SELL'

# ax1.scatter(df.index[buy_signals], df.loc[buy_signals, 'Close'], 
#             color='green', marker='^', s=60, label='BUY', zorder=5, edgecolors='black', linewidth=0.5)
# ax1.scatter(df.index[sell_signals], df.loc[sell_signals, 'Close'], 
#             color='red', marker='v', s=60, label='SELL', zorder=5, edgecolors='black', linewidth=0.5)

# ax1.set_title(f'{ticker} – AI Signals (Your MVP)')
# ax1.legend()
# ax1.grid(True, alpha=0.3)

# # RSI
# ax2.plot(df.index, df['RSI'], color='purple', linewidth=1.2)
# ax2.axhline(70, color='red', linestyle='--', alpha=0.7)
# ax2.axhline(30, color='green', linestyle='--', alpha=0.7)
# ax2.fill_between(df.index, 30, 70, color='gray', alpha=0.1)
# ax2.set_ylim(0, 100)
# ax2.set_ylabel('RSI')
# ax2.grid(True, alpha=0.3)

# st.pyplot(fig)

# # Summary
# st.markdown("### Signal Summary")
# st.write(df['Signal'].value_counts())

# st.markdown("### Your Logic")
# st.success("**BUY**: Close < MA20, RSI < 30, RSI rising 2 days")
# st.error("**SELL**: Close > MA20, RSI > 70, RSI falling 2 days")

# st.caption("Built with your code. Deployed with Streamlit.")
