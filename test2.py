from flask import Flask, request, jsonify
from config.mt5conf import mt5, passwd, server
from termcolor import colored

app = Flask(__name__)

class Signal:
    def __init__(self, direction, pair):
        self.direction = direction
        self.pair = pair

    def to_dict(self):
        return {"direction": self.direction, "pair": self.pair}


@app.route('/webhook', methods=['POST'])
def webhook():
    content_type = request.content_type

    if content_type.startswith('text/plain'):
        data = request.data.decode('utf-8')
        print(data)
        
        if "Box Buy" in data:
            direction = "buy"
            direction = direction.upper()
            parts = data.split(' ')
            # The pair should be in the 5th position (index 4)
            pair = parts[5] if len(parts) > 4 else 'Unknown'
            pair = f"{pair}m"
            signal = Signal(direction=direction, pair=pair)
        
        elif "Buy" in data:
            direction = "BUY"
            parts = data.split(' ')
            pair = parts[4] if len(parts) > 4 else 'Unknown'
            pair = f"{pair}m"
            signal = Signal(direction=direction, pair=pair)

        elif "Sell" in data:
            direction = "sell"
            direction = direction.upper()
            parts = data.split(' ')
            # The pair should be in the 4th position (index 3)
            pair = parts[4] if len(parts) > 3 else 'Unknown'
            pair = f"{pair}m"
        # Create the signal object
        signal = Signal(direction=direction, pair=pair)
        
        allinone(signal)

        return jsonify(signal.to_dict()), 200

    return jsonify({"status": "error", "message": "Unsupported content type"}), 400


def allinone(signal):
    print(colored('-------------------', 'blue'))
    pair = signal.pair
    if pair == 'US100m':
        pair = "USTECm"
    direction = signal.direction
    signal_recieved(pair, direction)
    initialize()
    info(pair)
    lot, tp, sl = pretrade(pair, direction)
    status = trade(lot, direction , pair, tp, sl)
    if status.retcode == 10009:
        print(colored('INFO', 'blue'), "TRADE OPENED")
    elif status.retcode == 10016:
        print("trade failed rapid chart, trying again")
        allinone(signal)
    else:
        print(colored("INFO", 'red'), f"TRADE FAILED : RETCODE {status.retcode}")



def signal_recieved(pair, direction):
    print(colored('SIGNAL RECEIVED', 'yellow'))
    print(colored("Pair:", 'cyan'),  pair)
    print(colored("Direction:", 'magenta'), direction)
    print(colored('-------------------', 'green'))


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
    

def info(pair):
    print(colored('-------------------', 'blue'), colored(pair, "green"))
    symbol_info = mt5.symbol_info(pair)
    print("Ask Price:", symbol_info.ask)
    print("Bid Price:", symbol_info.bid)
    spread = symbol_info.ask - symbol_info.bid
    spread = round(spread, 5)
    print(f'Spread : {spread}')


def pretrade(pair, direction):
    print(colored('-------------------', 'blue'), colored("Calculation", "green"))
    account_info = mt5.account_info()
    balance = account_info.balance
    value = int(balance) / 100
    lot = value * 0.04
    lot = round(lot, 2)
    pip_size = 0.01
    pip_value = pip_size * lot
    pip_value = round(pip_value, 3)

    if pair == "USDTECm":
        if direction == "BUY":
            syminfo = mt5.symbol_info(pair)
            price = syminfo.ask
            tp = 0.00
            sl = 0.00
        elif direction == "SELL":
            syminfo = mt5.symbol_info(pair)
            price = syminfo.bid
            tp = price - 1
            sl = price + 1.5
    else:
        if direction == "BUY":
            syminfo = mt5.symbol_info(pair)
            price = syminfo.ask
            tp = price + 0.5
            sl = price - 1
        elif direction == "SELL":
            syminfo = mt5.symbol_info(pair)
            price = syminfo.bid
            tp = price - 0.5
            sl = price + 1

    print(f"Tp: {tp}, SL : {sl}")
    
    print(f"Tick value : {syminfo.trade_tick_value}")
    print(f"Lot size : {lot}")
    print(f"Pip value : {pip_value}")
    
    return lot, tp, sl


def trade(lot, direction, pair, tp, sl):
    print(colored('-------------------', 'blue'), colored("Executing trade", "green"))
    if direction == 'BUY':
        order_type = mt5.ORDER_TYPE_BUY
    elif direction == 'SELL':
        order_type  = mt5.ORDER_TYPE_SELL
    request = {
        "action" : mt5.TRADE_ACTION_DEAL,
        "symbol" : pair,
        "type" : order_type,
        "volume" : lot,
        "sl" : sl,
        "tp" : tp,
        "magic" : 234000,
        "comment" : 'Bot py',
        "type_time" : mt5.ORDER_TIME_GTC,
        "type_filling" : mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
