import numpy as np
import ccxt

from exchange import Exchange

class GDAX(Exchange):
	def __init__(self, api_key, api_secret, currency_from="BTC", currency_to="ZAR"):
		super().__init__(currency_from, currency_to)

		self.exchange = ccxt.gdax()
		self.exchange.apiKey = api_key
		self.exchange.secret = api_secret

		self.set_sell_fees(variable=2.5/100)
		self.set_buy_fees(variable=0)
		self.set_send_fees(variable=0.1/100)
		self.set_receive_fees(fixed=0.0002)
		self.set_withdrawl_fees(fixed=0.15)
		self.set_deposit_fees(fixed=0.15)

	def get_current_buy_rate(self):
		market = self.exchange.load_markets(True)
		rates = float(self.exchange.fetch_ticker('BTC/EUR')['info']['price'])
		return(rates)

	def get_balances(self):
		balance = self.exchange.fetchBalance()
		amount_f = balance['info']['balance'][self.currency_from]['total']
		amount_t = balance['info']['balance'][self.currency_to]['total']
		return({self.currency_from: amount_f, self.currency_to: amount_t})

