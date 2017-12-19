import numpy as np
import ccxt

from .exchange import Exchange

class Bitstamp(Exchange):
	def __init__(self, key=None, secret=None, currency_from="EUR", currency_to="BTC"):
		super().__init__(currency_from=currency_from, currency_to=currency_to)

		self.exchange = ccxt.bitstamp()
		self.exchange.apiKey = key
		self.exchange.secret = secret

		self.set_sell_fees(variable=0.25/100)
		self.set_buy_fees(variable=0.25/100)
		self.set_send_fees(variable=0.1/100)
		self.set_receive_fees(fixed=0)
		self.set_withdrawl_fees(fixed=15, variable=0.09/100)
		self.set_deposit_fees(fixed=7.5, variable=0.05/100)

	def get_current_buy_rate(self):
		market = self.exchange.load_markets(True)
		rates = float(self.exchange.fetch_ticker("{}/{}".format(self.currency_to, self.currency_from))['info']['last'])
		return(rates)

	def get_balances(self):
		balance = self.exchange.fetchBalance()
		amount_f = balance['info']['balance'][self.currency_from]['total']
		amount_t = balance['info']['balance'][self.currency_to]['total']
		return({self.currency_from: amount_f, self.currency_to: amount_t})

