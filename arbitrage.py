from coinbase import Coinbase
from luno import Luno

import argparse

# ZAR -> EUR, EUR -> BTC, BTC -> ZAR
def arbitrage(amount, buy_ex, sell_ex, forex_ex=None, verbose=False):
	buy_amount = amount

	if forex_ex:
		forex_price = forex_ex.get_current_rate()
		forex_ff, forex_rf = forex_ex.get_buy_fee()
		forex_fees = forex_ff + (amount*forex_rf)
		buy_amount = (amount - forex_fees)/forex_price

	buy_price = buy_ex.get_current_rate()
	buy_rec_ff, buy_rec_rf = buy_ex.get_receive_fee()
	buy_ff, buy_rf = buy_ex.get_buy_fee()
	send_ff, send_rf = buy_ex.get_send_fee()

	sell_price = sell_ex.get_current_rate()
	sell_rec_ff, sell_rec_rf = sell_ex.get_receive_fee()
	sell_ff, sell_rf = sell_ex.get_sell_fee()
	withdraw_ff, withdraw_rf = sell_ex.get_send_fee()

	deposit_fees = buy_rec_ff + (buy_amount * buy_rec_rf)
	buy_amount = buy_amount - deposit_fees
	buy_fees = buy_ff + (buy_amount * buy_rf)
	token_bought = (buy_amount - buy_fees)/buy_price

	send_fees = send_ff + (token_bought * send_rf)
	token_recv = token_bought - send_fees
	recv_fees = sell_rec_ff + (token_recv * sell_rec_rf)
	token_recv = token_recv - recv_fees

	sell_fees = sell_ff + (token_recv * sell_rf)
	sold_amount = (token_recv/sell_price) - sell_fees
	withdrawl_fees = withdraw_ff + (sold_amount * withdraw_rf)
	amount_out = sold_amount - withdrawl_fees

	profit = amount_out - amount
	roi = profit/amount

	return(profit, roi)

# Perform the buying and selling
def perform_arbitrage(amount, buy_ex, sell_ex, forex_ex=None):
	return(0)

def parse_args():
	parser = ArgumentParser()
	return(parser.parse_args())

if __name__ == "__main__":
	args = parse_args()