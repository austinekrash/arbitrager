from exchange import Exchange
import pandas as pd

class FNB(Exchange):
	def __init__(self, currency_to="BTC"):
		super().__init__("ZAR", currency_to)

		self.types = {
            'buy': 'Bank Selling Rate',
            'sell': 'Bank Buying TT',
        }

		self.exchange = pd.read_html('https://www.fnb.co.za/Controller?nav=rates.forex.list.ForexRatesList',
            index_col=1, header=0, match=self.currency_to)[0]
		self.set_buy_fees(fixed=110, variable=0.55/100)

	def get_current_buy_rate(self):
		self.exchange = pd.read_html('https://www.fnb.co.za/Controller?nav=rates.forex.list.ForexRatesList',
            index_col=1, header=0, match=self.currency_to)[0]

		rate = self.exchange.loc[self.currency_to, self.types["buy"]]

		return(float(rate))

	# Overload the parent buy method as FNB has min max fee structure
	def buy(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.buy_fees["fixed"], self.buy_fees["variable"]
		buy_amount = amount

		if include_fees:
			buy_amount = ((1 - fixed_fee/amount)/(1 + max(min(var_fee, 660/amount), 125/amount)))*amount

		fees = max(min(var_fee*buy_amount, 660), 125) + fixed_fee
		rate = self.get_current_buy_rate()

		bought = buy_amount/rate

		return({"bought": bought, "buy_amount": buy_amount, "fees": fees, "rate": rate})

if __name__ == "__main__":
	fnb = FNB("EUR", "buy")
	print(fnb.buy(30000))
	print(fnb.buy(30000, include_fees=False))