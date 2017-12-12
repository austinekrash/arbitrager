from exchange import Exchange
import pandas as pd

class FNB(Exchange):
	def __init__(self, currency_to="BTC", ex_type="buy"):
		super().__init__("ZAR", currency_to)

		types = {
            'buy': 'Bank Selling Rate',
            'sell': 'Bank Buying TT',
        }

		self.exchange = pd.read_html('https://www.fnb.co.za/Controller?nav=rates.forex.list.ForexRatesList',
            index_col=1, header=0, match=self.currency_to)[0]
		self.type = types[ex_type]

	def get_current_rate(self):
		self.exchange = pd.read_html('https://www.fnb.co.za/Controller?nav=rates.forex.list.ForexRatesList',
            index_col=1, header=0, match=self.currency_to)[0]

		rate = self.exchange.loc[self.currency_to, self.type]

		return(float(rate))

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
		fixed_fee = 100
		rate_fee = (0.5/100)*buy_amount
		fees = max(min(rate_fee, 660), 125) + fixed_fee
		return(fixed_fee, rate_fee, fees)


if __name__ == "__main__":
	fnb = FNB("EUR", "buy")
	print(fnb.get_current_rate())
	fnb = FNB("EUR", "sell")
	print(fnb.get_current_rate())