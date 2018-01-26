from .exchange import Exchange
import pandas as pd

class FNB(Exchange):
	def __init__(self, currency_from="ZAR", currency_to="EUR"):
		# ZAR is the benchmark currency so
		if currency_from == "ZAR":
			super().__init__(currency_from, currency_to)
		elif currency_to == "ZAR":
			super().__init__(currency_to, currency_from)

		self.types = {
            'buy': 'Bank Selling Rate',
            'sell': 'Bank Buying TT',
        }

		self._get_rate()
		self.set_buy_fees(fixed=110, variable=0.55/100)
		self.set_sell_fees(fixed=0, variable=0.55/100)

	def _get_rate(self, rate_type="buy"):
		self.exchange = pd.read_html('https://www.fnb.co.za/Controller?nav=rates.forex.list.ForexRatesList',
            index_col=1, header=0, match=self.currency_to)[0]
		rate = self.exchange.loc[self.currency_to, self.types[rate_type]]
		return(float(rate))

	def get_current_buy_rate(self):
		return(self._get_rate("buy"))

	def get_current_sell_rate(self):
		return(self._get_rate("sell"))

	# Overload the parent buy and sell methods as FNB has min max fee structure
	def buy(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.buy_fees["fixed"], self.buy_fees["variable"]
		buy_amount = amount

		if include_fees:
			amount = ((1 - fixed_fee/amount)/(1 + max(min(var_fee, 650/amount), 150/amount)))*amount

		fees = max(min(var_fee*amount, 650), 150) + fixed_fee
		rate = self.get_current_buy_rate()

		bought = amount/rate

		return({"bought": bought, "buy_amount": amount, "fees": fees, "rate": rate})

	def sell(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.sell_fees["fixed"], self.sell_fees["variable"]

		rate = self.get_current_sell_rate()
		sold = amount*rate

		fees = max(min(var_fee*sold, 650), 150) + fixed_fee

		if include_fees:
			sold -= fees

		return({"sold": sold, "sell_amount": amount, "fees": fees, "rate": rate})

if __name__ == "__main__":
	fnb = FNB("EUR", "buy")
	print(fnb.buy(30000))
	print(fnb.buy(30000, include_fees=False))
