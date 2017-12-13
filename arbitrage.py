import os
from dotenv import load_dotenv

from luno import Luno
from fnb import FNB
from gdax import GDAX
from coinbase_ex import CoinbaseEx

import argparse

def log(msg, verbose):
	if verbose is True:
		print(msg)

# ZAR -> EUR, EUR -> BTC, BTC -> ZAR
def arbitrage(amount, buy_ex, sell_ex, forex_ex, verbose=False, execute=False):
	initial_amount = amount

	log("Arbitrage amount {:.2f}{}".format(amount, forex_ex.currency_from), verbose)

	transaction = forex_ex.buy(amount, include_fees=False, execute=execute)

	log("Bought {:.2f} {} at a rate of {:.4f} {}".format(transaction["bought"], forex_ex.currency_to,
		transaction["rate"],forex_ex.currency_from), verbose)

	transaction = buy_ex.deposit(transaction["bought"], include_fees=True, execute=execute)
	log("Deposited {:.2f} {}".format(transaction["deposited"], buy_ex.currency_from), verbose)

	transaction = buy_ex.buy(transaction["deposited"], include_fees=True, execute=execute)

	log("Bought {:.6f} {} at a rate of {:.2f} {}".format(transaction["bought"], buy_ex.currency_to,
		transaction["rate"],buy_ex.currency_from), verbose)

	transaction = buy_ex.send(transaction["bought"], include_fees=True, execute=execute)
	log("Sent {:.6f}{}".format(transaction["sent"], buy_ex.currency_to), verbose)

	transaction = sell_ex.receive(transaction["sent"], include_fees=True, execute=execute)
	log("Received {:.6f} {}".format(transaction["received"], sell_ex.currency_to), verbose)

	transaction = sell_ex.sell(transaction["received"], include_fees=True, execute=execute)
	log("Sold {:.2f} {} at a rate of {:.2f} {}".format(transaction["sold"], sell_ex.currency_from,
		transaction["rate"],sell_ex.currency_from), verbose)

	transaction = sell_ex.withdrawl(transaction["sold"], include_fees=True, execute=execute)
	log("Withdrew {:.2f} {}".format(transaction["withdrew"], sell_ex.currency_from), verbose)
	
	profit = transaction["withdrew"] - initial_amount
	margin = profit/initial_amount*100

	log("Profit: {:.2f} {}\tMargin:{:.3f}".format(profit, sell_ex.currency_from, margin), verbose)

	return(profit, margin)

def parse_args():
	parser = argparse.ArgumentParser()
	return(parser.parse_args())

if __name__ == "__main__":
	args = parse_args()

	load_dotenv('.env')
	CB_KEY = os.environ.get('CB_KEY')
	CB_SECRET = os.environ.get('CB_SECRET')
	LUNO_KEY = os.environ.get('LUNO_KEY')
	LUNO_SECRET = os.environ.get('LUNO_SECRET')

	forex_ex = FNB("EUR")
	# buy_ex = GDAX("","","EUR","BTC")
	buy_ex = CoinbaseEx(CB_KEY, CB_SECRET,"EUR","BTC")
	sell_ex = Luno(LUNO_KEY,LUNO_SECRET, currency_from="ZAR", currency_to="BTC")

	profit, roi = arbitrage(30000, buy_ex, sell_ex, forex_ex, verbose=True)

