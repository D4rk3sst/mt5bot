import MetaTrader5 as mt5
from config.mt5conf import account, server, passwd
import time

# Initialize the MetaTrader 5 platform
if not mt5.initialize():
    print("Initialization failed")
    mt5.shutdown()

# Connect to your broker account
login = 156998448# Replace with your Exness account number
password = passwd # Replace with your Exness account password
  # Replace with your Exness server

if not mt5.login(login, password, server):
    print("Login failed")
    mt5.shutdown()
else:
    print("Connected to broker")

# Define the trade function
def open_trade(symbol, lot_size, order_type):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"{symbol} not found, cannot proceed")
        mt5.shutdown()
        return
    
    # Check if the symbol is available for trading
    if not symbol_info.visible:
        print(f"{symbol} is not visible, trying to activate")
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to activate {symbol}, cannot proceed")
            mt5.shutdown()
            return
    
    # Set up the trade request
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
    deviation = 20  # Maximum price deviation in points
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "sl": 0.00 , #price - 100 * point if order_type == mt5.ORDER_TYPE_BUY else price + 100 * point,
        "tp": 0.00, #price + 100 * point if order_type == mt5.ORDER_TYPE_BUY else price - 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "Python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Send the trade request
    result = mt5.order_send(request)
    
    return result

# Function to monitor the trade until it is closed
def monitor_trade(order_ticket):
    print(f"Monitoring trade {order_ticket}...")
    while True:
        # Check the trade status
        trade = mt5.positions_get(ticket=order_ticket)
        if not trade:
            print("Trade closed.")
            break
        else:
            print("Trade is still open...")
            time.sleep(5)  # Wait 5 seconds before checking again

    # Check the history of the order to see if it was profitable
    history = mt5.history_deals_get(ticket=order_ticket)
    if history and history[0].profit > 0:
        print(f"Trade {order_ticket} won with profit: {history[0].profit}")
    else:
        print(f"Trade {order_ticket} lost with profit: {history[0].profit if history else 'Unknown'}")

# Test the trade function and monitor it
symbol = "XAUUSDm"  # Replace with your preferred trading symbol
lot_size = 0.1234
lot_size = round(lot_size, 2)  # Example lot size
order_type = mt5.ORDER_TYPE_BUY  # Buy order

'''result = open_trade(symbol, lot_size, order_type)
print(mt5.last_error())
if result.retcode == mt5.TRADE_RETCODE_DONE:
    print(f"Trade successfully placed: {result}")
    monitor_trade(result.order)
else:
    print(f"Trade failed: {result}")

# Shutdown MetaTrader 5
mt5.shutdown()
'''