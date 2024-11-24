from config.mt5conf import mt5, passwd, server
from termcolor import colored
import pandas as pd


def initialize():
    print(colored("[INFO]", 'blue'), "Logging in to mt5")
    if not mt5.initialize(
    login = 156998448,
    password = passwd,
    server = server
):
        print("initialize() failed, error code =",mt5.last_error())

    account_info = mt5.account_info()
    if account_info:
        print(colored('-------------------', 'blue'), colored(account_info.login, "red"))
        print(f"Balance : {account_info.balance}", account_info.currency)
        print(f"leverage : {account_info.leverage}")
        print(f"Margin free : {account_info.margin_free}")  

def get_data():
    print(colored('-------------------', 'blue'), colored("", "red"))
    symbol = "USTECm"
    timeframe = mt5.TIMEFRAME_M1
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 3)  # Get the past 2 candles
    if rates is None:
        print("Error retrieving rates")
        mt5.shutdown()
        quit()
    data = pd.DataFrame(rates)
    return data

def calculate_heikin_ashi(df):
    df['HA_Close'] = (df['close'] + df['open'] + df['high'] + df['low']) / 4
    
    # Initialize HA_Open for the first candle
    df['HA_Open'] = (df['open'] + df['close']) / 2
    for i in range(1, len(df)):
        df['HA_Open'].iloc[i] = (df['HA_Open'].iloc[i-1] + df['HA_Close'].iloc[i-1]) / 2

    df['HA_High'] = df[['high', 'HA_Open', 'HA_Close']].max(axis=1)
    df['HA_Low'] = df[['low', 'HA_Open', 'HA_Close']].min(axis=1)

    return df[['time', 'HA_Open', 'HA_High', 'HA_Low', 'HA_Close']]

def main():
    initialize()
    data = get_data()
    hek = calculate_heikin_ashi(data)
    print(hek)

if __name__ == '__main__':
    main()