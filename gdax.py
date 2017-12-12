import numpy as np
import ccxt

from exchange import Exchange

class GDAX(Exchange):
	def __init__(self, api_key, api_secret, currency_from="BTC", currency_to="ZAR"):
		super().__init__(currency_from, currency_to)

		self.exchange = ccxt.gdax()
		self.exchange.apiKey = api_key
		self.exchange.secret = api_secret

	def get_current_rate(self):
		market = self.exchange.load_markets(True)
		rates = float(self.exchange.fetch_ticker('BTC/EUR')['info']['price'])
		return(rates)

	def get_balances(self):
		balance = self.exchange.fetchBalance()
		amount_f = balance['info']['balance'][self.currency_from]['total']
		amount_t = balance['info']['balance'][self.currency_to]['total']
		return({self.currency_from: amount_f, self.currency_to: amount_t})


	def buy(self, amount):
		return(0)

	def sell(self, amount):
		return(0)

	def send(self, amount):
		return(0)

	def receive(self, amount):
		return(0)

	def fees(self, buy_amount):
		return(0)
