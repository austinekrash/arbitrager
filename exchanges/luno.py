import numpy as np
import ccxt

from .exchange import Exchange

class Luno(Exchange):
	def __init__(self, key=None, secret=None, currency_from="ZAR", currency_to="BTC"):
		super().__init__(currency_from, currency_to)

		self.exchange = ccxt.luno()
		self.exchange.apiKey = key
		self.exchange.secret = secret

		self.set_sell_fees(variable=1/100)
		# TODO: This fee is for BTC receive... I need to still add an init method to set appropriate fees
		self.set_receive_fees(fixed=0.0002)
		self.set_withdrawl_fees(fixed=8.50)

	# TODO: Add caching to rate check to prevent DDOS pretection blocking access
	def get_current_buy_rate(self):
		market = self.exchange.load_markets(True)
		rates = float(self.exchange.fetch_ticker("{}/{}".format(self.currency_to, self.currency_from))['info']['last_trade'])
		return(rates)

	def get_balances(self):
		balance = self.exchange.fetchBalance()
		amount_f = balance['info']['balance'][self.currency_from]['total']
		amount_t = balance['info']['balance'][self.currency_to]['total']
		return({self.currency_from: amount_f, self.currency_to: amount_t})

	# TODO: Add if execute... to actually perform the trade
	def buy(self, amount, include_fees=True, execute=False):
		transaction = super().buy(amount, include_fees=include_fees)

		return(transaction)

	def sell(self, amount, include_fees=True, execute=False):
		transaction = super().sell(amount, include_fees=include_fees)

		return(transaction)

if __name__ == "__main__":
	from dotenv import load_dotenv
	import os
	load_dotenv('.env')
	LUNO_KEY = os.environ.get('LUNO_KEY')
	LUNO_SECRET = os.environ.get('LUNO_SECRET')

	luno = Luno(LUNO_KEY, LUNO_SECRET, currency_from="ZAR", currency_to="BTC")
	print(luno.sell(0.156, include_fees=True))

