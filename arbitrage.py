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
def arbitrage(amount, buy_ex, sell_ex, forex_ex=None, forex_fees=True, verbose=False, execute=False):
	initial_amount = amount
	forex_transaction = None

	start_ex = buy_ex
	if forex_ex:
		start_ex = forex_ex

	log("Arbitrage amount {:.2f} {}".format(amount, start_ex.currency_from), verbose)

	if forex_ex:
		forex_transaction = forex_ex.buy(amount, include_fees=forex_fees, execute=execute)
		log("Bought {:.2f} {} at a rate of {:.4f} {}".format(forex_transaction["bought"], forex_ex.currency_to,
			forex_transaction["rate"],forex_ex.currency_from), verbose)
		amount = forex_transaction["bought"]

	transaction = buy_ex.deposit(amount, include_fees=True, execute=execute)
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

	if forex_ex and forex_fees is False:
		profit -= forex_transaction["fees"]

	margin = profit/initial_amount*100

	log("Profit: {:.2f} {}\tMargin:{:.3f}".format(profit, sell_ex.currency_from, margin), verbose)

	return(profit, margin)

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--forex", default="EUR", choices=["EUR", "USD", "ZAR"], help="Forex currency to use")
	parser.add_argument("--amount", type=float, help="Specify an amount to arbitrage")
	parser.add_argument("--local", default="ZAR", choices=["EUR", "USD", "ZAR"], help="Local currency to use for sale of tokens")
	parser.add_argument("--token", default="BTC", choices=["BTC", "ETH"], help="Token to arbitrage")
	parser.add_argument("--no_forex_buy", action="store_true", help="This will assume the arbitrage amount is already in Forex currency specified")
	parser.add_argument("--forex_with_fees", action="store_true", help="Assumes we want to include the forex fees in the arbitrage amount")
	parser.add_argument("--fmt", default="STDOUT", choices=["CSV", "STDOUT", "VERBOSE"], help="How to display the output")

	return(parser.parse_args())

def evaluate_arbitrage(args):
	load_dotenv('.env')
	CB_KEY = os.environ.get('CB_KEY')
	CB_SECRET = os.environ.get('CB_SECRET')
	LUNO_KEY = os.environ.get('LUNO_KEY')
	LUNO_SECRET = os.environ.get('LUNO_SECRET')

	forex_ex = None
	if args.no_forex_buy is False:
			forex_ex = FNB(args.forex)

	buy_ex = GDAX("","", args.forex, args.token)
	#buy_ex = CoinbaseEx(CB_KEY, CB_SECRET,"EUR","BTC")
	sell_ex = Luno(LUNO_KEY,LUNO_SECRET, currency_from=args.local, currency_to=args.token)

	profit, margin = arbitrage(args.amount, buy_ex, sell_ex, forex_ex=forex_ex, forex_fees=args.forex_with_fees, verbose=True, execute=False)

if __name__ == "__main__":
	args = parse_args()
	evaluate_arbitrage(args)
