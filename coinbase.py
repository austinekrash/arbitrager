from coinbase.wallet.client import Client
from coinbase.wallet.error import TwoFactorRequiredError

from exchange import Exchange

class Coinbase(Exchange):
	def __init__(self, api_key, api_secret, currency_from="EUR", currency_to="BTC"):
		super().__init__(currency_from, currency_to)

		self.exchange = Client(api_key, api_secret)
		self.exchange.apiKey = api_key
		self.exchange.secret = api_secret

	def get_current_rate(self):
		rates = self.exchange.get_buy_price(currency_pair = "{}-{}".format(self.currency_from, self.currency_to))
		return(rates)
