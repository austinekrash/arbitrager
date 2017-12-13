from coinbase.wallet.client import Client
from coinbase.wallet.error import TwoFactorRequiredError

from exchange import Exchange

class CoinbaseEx(Exchange):
	def __init__(self, api_key, api_secret, currency_from="EUR", currency_to="BTC"):
		super().__init__(currency_from, currency_to)

		self.exchange = Client(api_key, api_secret)
		self.exchange.apikey = api_key
		self.exchange.secret = api_secret

		self.set_buy_fees(variable=0.0149)
		self.set_sell_fees(variable=0.0149)

	def get_current_buy_rate(self):
		rates = self.exchange.get_buy_price(currency_pair = "{}-{}".format(self.currency_from, self.currency_to))

		assert rates["base"] == self.currency_to
		assert rates["currency"] == self.currency_from

		return(float(rates["amount"]))

	def buy(self, amount, include_fees=True, execute=False):
		transaction = super().buy(amount, include_fees=include_fees)
		return(transaction)


if __name__ == "__main__":
	from dotenv import load_dotenv
	import os

	load_dotenv('.env')
	CB_KEY = os.environ.get('CB_KEY')
	CB_SECRET = os.environ.get('CB_SECRET')

	c = CoinbaseEx(CB_KEY, CB_SECRET)
	print(c.buy(1839.79, True))
	print(c.buy(1839.79, False))