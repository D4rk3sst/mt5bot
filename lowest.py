from config.mt5conf import mt5, passwd, server
from termcolor import colored

def initialize():
    print(colored("[INFO]", 'blue'), "Logging in to mt5")
    if not mt5.initialize(
        login=156998448,
        password=passwd,
        server=server
    ):
        print("initialize() failed, error code =", mt5.last_error())
        return False
    return True

def is_currency_pair(symbol_name):
    # Check if the symbol name is a 6-letter pair optionally followed by an 'm'
    return (len(symbol_name) == 7 and symbol_name[:6].isalpha() and symbol_name[6] == 'm')

def fetch_low_spread_symbols():
    # Fetch all symbols
    symbols = mt5.symbols_get()
    if symbols is None:
        print("Failed to fetch symbols, error code =", mt5.last_error())
        return

    # Print pairs with a spread under 5 for currency pairs only
    print(colored("[INFO]", 'blue'), "Currency pairs with spread under 5:")
    for symbol in symbols:
        if is_currency_pair(symbol.name):  # Check if it's a currency pair with 'm'
            # Ensure symbol is active
            if mt5.symbol_select(symbol.name, True):
                # Get symbol's info, including bid and ask prices
                symbol_info = mt5.symbol_info(symbol.name)
                symbol_tick = mt5.symbol_info_tick(symbol.name)
                
                if symbol_info is None or symbol_tick is None or not symbol_info.visible:
                    continue

                # Calculate spread in points
                spread = (symbol_tick.ask - symbol_tick.bid) / symbol_info.point

                # Print the pair if spread is under 5
                if spread < 10 and symbol_tick.ask > 0 and symbol_tick.bid > 0:
                    print(f"{symbol.name}: Spread = {spread:.2f}")

if __name__ == "__main__":
    if initialize():
        fetch_low_spread_symbols()
