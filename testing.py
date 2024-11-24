from config.mt5conf import mt5, passwd, server
import pandas as pd
import numpy as np
from termcolor import colored
import asyncio
# Initialize connection to MetaTrader 5 terminal
def initialize():
    print(colored("[INFO]", 'blue'), "Logging in to mt5")
    if not mt5.initialize(
        login=156998448,
        password=passwd,
        server=server
    ):
        print("initialize() failed, error code =", mt5.last_error())

# Fetch the last 3 candles for a symbol
def get_candles(symbol):
    candles = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 4)  #0 to start from current candle, 4 to retrieve the last 4

    if candles is None:
        print(f"Failed to retrieve candles, error code: {mt5.last_error()}")
        mt5.shutdown()
        quit()

    df = pd.DataFrame(candles)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert time from seconds to datetime
    df['time'] = df['time'].dt.strftime('%H:%M')
    return df

def calculate_heiken_ashi(df):
    ha_df = pd.DataFrame(index=df.index, columns=['HA_Open', 'HA_High', 'HA_Low', 'HA_Close'])
    
    # Calculate Heiken Ashi Close
    ha_df['HA_Close'] = (df['close'] + df['open'] + df['high'] + df['low']) / 4
    
    # Calculate Heiken Ashi Open
    ha_df['HA_Open'] = (df['open'].shift(1) + df['close'].shift(1)) / 2
    ha_df['HA_Open'] = ha_df['HA_Open'].fillna((df['open'] + df['close']) / 2)
    
    # Calculate Heiken Ashi High
    ha_df['HA_High'] = pd.concat([ha_df['HA_Open'], ha_df['HA_Close'], df['high']], axis=1).max(axis=1)
    
    # Calculate Heiken Ashi Low
    ha_df['HA_Low'] = pd.concat([ha_df['HA_Open'], ha_df['HA_Close'], df['low']], axis=1).min(axis=1)
    
    return ha_df
def classify_candle(row):
    if np.isclose(row['HA_Open'], row['HA_Close'], atol=0.0001):
        return "Doji"
    elif row['HA_Close'] > row['HA_Open']:
        return "Bullish"
    elif row['HA_Close'] < row['HA_Open']:
        return "Bearish"
    else:
        return "Sideways"
    
def save_candles_to_variables(df):
    ha_df = calculate_heiken_ashi(df)
    ha_df['Candle_Type'] = ha_df.apply(classify_candle, axis=1)
    
    # Save candle types to a dictionary
    candle_types = ha_df['Candle_Type'].tolist()
    candle_dict = {f'candle_{i+1}': candle for i, candle in enumerate(candle_types)}
    
    # Access candle types using correct keys
    candle_1 = candle_dict.get('candle_1', 'N/A')
    candle_2 = candle_dict.get('candle_2', 'N/A')
    candle_3 = candle_dict.get('candle_3', 'N/A')
    candle_4 = candle_dict.get('candle_4', 'N/A')

    return candle_1, candle_2, candle_3, candle_4

symbol = "XAUUSDm"
initialize()
df = get_candles(symbol)
candle_1, candle_2, candle_3, candle_4 = save_candles_to_variables(df)
print(candle_1)
print(candle_2)
print(candle_3)
print(candle_4)
#ha_df = calculate_heiken_ashi(df)
