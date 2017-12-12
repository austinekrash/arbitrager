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

	def get_balances(self):
		account = self.exchange.get_accounts()

		return({self.currency_from: amount_f, self.currency_to: amount_t})


	def buy(self, amount):
		return(0)

	def sell(self, amount):
		return(0)

	def send(self, account, amount):
		account.send_money(to=account,
                   amount=amount,
                   currency=self.currency_to)
		return(0)

	def receive(self, amount):
		return(0)

	def fees(self, buy_amount):
		return(0)
