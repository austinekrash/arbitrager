# from coinbase import Coinbase
from luno import Luno
from fnb import FNB
from gdax import GDAX

import argparse

def log(msg, verbose):
	if verbose is True:
		print(msg)

# ZAR -> EUR, EUR -> BTC, BTC -> ZAR
def arbitrage(amount, buy_ex, sell_ex, forex_ex=None, verbose=False):
	buy_amount = amount
	start_ex = buy_ex

	if forex_ex:
		forex_price = forex_ex.get_current_rate()
		forex_fees = forex_ex.get_buy_fees(amount)
		buy_amount = (amount - forex_fees)/forex_price
		start_ex = forex_ex

	log("Arbitrage amount {:.2f}{}".format(amount, start_ex.currency_from), verbose)

	buy_price = buy_ex.get_current_rate()
	deposit_fees = buy_ex.get_receive_fees(buy_amount)
	buy_amount -= deposit_fees
	buy_fees = buy_ex.get_buy_fees(buy_amount)
	token_bought = (buy_amount - buy_fees)/buy_price

	log("Buy amount {:.2f}{}".format(buy_amount, buy_ex.currency_from), verbose)
	log("Bought {:.6f}{}".format(token_bought, buy_ex.currency_to), verbose)

	send_fees = buy_ex.get_send_fees(token_bought)
	token_recv = token_bought - send_fees

	sell_price = sell_ex.get_current_rate()
	sell_deposit_fees = sell_ex.get_receive_fees(token_recv)
	token_recv -= sell_deposit_fees

	log("Received {:.6f}{}".format(token_bought, sell_ex.currency_from), verbose)

	sell_amount = token_recv/sell_price
	sell_fees = sell_ex.get_sell_fees(sell_amount)
	sold_amount = sell_amount - sell_fees
	withdrawl_fees = sell_ex.get_send_fees(sold_amount)
	amount_out = sold_amount - withdrawl_fees

	log("Sold for {:.2f}{}".format(sold_amount, sell_ex.currency_to), verbose)
	log("Amount out {:.2f}{}".format(amount_out, sell_ex.currency_to), verbose)

	profit = amount_out - amount
	roi = profit/amount

	return(profit, roi)

# Perform the buying and selling
def perform_arbitrage(amount, buy_ex, sell_ex, forex_ex=None):
	return(0)

def parse_args():
	parser = argparse.ArgumentParser()
	return(parser.parse_args())

if __name__ == "__main__":
	args = parse_args()

	forex_ex = FNB("EUR")
	buy_ex = GDAX("","","EUR","BTC")
	sell_ex = Luno("","","BTC","ZAR")

	profit, roi = arbitrage(30000, buy_ex, sell_ex, forex_ex=forex_ex, verbose=True)

