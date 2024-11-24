from config.mt5conf import mt5, passwd, server
from termcolor import colored
def initialize():
    if not mt5.initialize(
    login = 156998448,
    password = passwd,
    server = server
):
        print("initialize() failed, error code =",mt5.last_error())


def account_info():
    account_info = mt5.account_info()
    if account_info:
        print(colored('-------------------', 'blue'), colored(account_info.login, "red"))
        print(f'Company : {account_info.company}')
        print(f"Server : {account_info.server}")
        print(f"Balance : {account_info.balance}", account_info.currency)
        print(f"leverage : {account_info.leverage}")
        print(f"Margin free : {account_info.margin_free}")


def info(symbol):
    print(colored('-------------------', 'blue'), colored(symbol, "green"))
    syminfo = mt5.symbol_info(symbol)
    print("Ask Price:", syminfo.ask)
    print("Bid Price:", syminfo.bid)
    size(symbol, syminfo)

def size(symbol, syminfo):
    print(colored('-------------------', 'blue'), colored("Calculation", "green"))
    tick = mt5.symbol_info_tick(symbol)
    print("tick value:", syminfo.trade_tick_value)
    account_info = mt5.account_info()
    balance = account_info.balance
    value = int(balance) / 100
    lot = value * 0.04
    print(f"lot size: {lot}")

def pretrade(pair, direction):
    print(colored('-------------------', 'blue'), colored("Calculation", "green"))
    syminfo = mt5.symbol_info(pair)
    account_info = mt5.account_info()
    balance = account_info.balance
    value = int(balance) / 100
    lot = value * 0.04
    lot = round(lot, 2)
    pip_size = 0.01
    pip_value = pip_size * lot
    pip_value = round(pip_value, 3)
    
    if direction == "BUY":
        price = syminfo.ask
        tp = price + 1
        sl = price - 1.5
    elif direction == "SELL":
        price = syminfo.bid
        tp = price - 1
        sl = price + 1.5

    print(f"Tp: {tp}, SL : {sl}")
    
    print(f"Tick value : {syminfo.trade_tick_value}")
    print(f"Lot size : {lot}")
    print(f"Pip value : {pip_value}")
    
    return lot, tp, sl

def main():
    initialize()
    account_info()
    info("XAUUSDm")
    print(colored('-------------------', 'blue'))
if __name__ == "__main__":
    main()