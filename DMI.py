import yfinance as yf
import matplotlib.pyplot as plt
from ta.trend import ADXIndicator
import streamlit as st
import pandas as pd

# Define available currency pairs
currency_pairs = {
    'EUR/USD': 'EURUSD=X',
    'GBP/USD': 'GBPUSD=X',
    'AUD/USD': 'AUDUSD=X',
    'USD/CAD': 'USDCAD=X',
    'USD/CHF': 'USDCHF=X',
    'NZD/USD': 'NZDUSD=X',
    'USD/JPY': 'JPY=X'
}

# Create a dropdown for selecting currency pairs
selected_currency = st.selectbox("Select a currency pair", list(currency_pairs.keys()))

# Fetching data based on selected currency pair
currency_data = yf.download(currency_pairs[selected_currency], start='2023-01-01', end='2024-09-27')

# Initialize ADXIndicator
adx = ADXIndicator(high=currency_data['High'], low=currency_data['Low'], close=currency_data['Close'])

# Calculate DMI, +DI, and -DI
currency_data['DMI'] = adx.adx()
currency_data['+DI'] = adx.adx_pos()
currency_data['-DI'] = adx.adx_neg()

# Smoothing the DMI, +DI, and -DI with a moving average
smoothing_window = 14  # Adjust the window size as needed
currency_data['DMI_Smooth'] = currency_data['DMI'].rolling(window=smoothing_window).mean()
currency_data['+DI_Smooth'] = currency_data['+DI'].rolling(window=smoothing_window).mean()
currency_data['-DI_Smooth'] = currency_data['-DI'].rolling(window=smoothing_window).mean()

# Drop NaN values if any
currency_data.dropna(inplace=True)

# Plotting
st.subheader(f'{selected_currency} Price and Directional Movement Index (DMI)')

# Create a new figure for plotting
fig, ax = plt.subplots(2, 1, figsize=(14, 10))

# Plot closing price
ax[0].plot(currency_data['Close'], label=f'{selected_currency} Close', color='blue', linewidth=2)
ax[0].set_title(f'{selected_currency} Closing Price', fontsize=16)
ax[0].set_xlabel('Date', fontsize=12)
ax[0].set_ylabel('Price', fontsize=12)
ax[0].grid(True)
ax[0].legend()

# Plot Smoothed DMI
ax[1].plot(currency_data['DMI_Smooth'], label='Smoothed DMI (ADX)', color='purple', linewidth=2)
ax[1].plot(currency_data['+DI_Smooth'], label='Smoothed +DI', color='green', linewidth=1.5)
ax[1].plot(currency_data['-DI_Smooth'], label='Smoothed -DI', color='red', linewidth=1.5)
ax[1].set_title('Smoothed Directional Movement Index (DMI)', fontsize=16, pad=20)
ax[1].set_xlabel('Date', fontsize=12)
ax[1].set_ylabel('Index Value', fontsize=12)
ax[1].axhline(25, color='gray', linestyle='--', label='DMI Threshold (25)', linewidth=1)  # Threshold line
ax[1].grid(True)
ax[1].legend()

# Show the plots in Streamlit
st.pyplot(fig)

# Additional information for users
st.write("🔍 **Reversal Signals**: When the ADX (purple line) peaks above 30, it might indicate a trend reversal, presenting good opportunities for buying or selling!")
