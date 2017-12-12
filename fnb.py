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

	def get_buy_fees(self, amount=0):
		fixed_fee = 100
		rate_fee = 0.5/100
		fees = max(min(rate_fee*amount, 660), 125) + fixed_fee
		return(fees)

if __name__ == "__main__":
	fnb = FNB("EUR", "buy")
	print(fnb.get_current_rate())
	ff, rf, fees = fnb.get_buy_fees(8000)
	print("FF: {}, RF: {}, FEES: {}".format(ff,rf,fees))
	ff, rf, fees = fnb.get_buy_fees(8000000)
	print("FF: {}, RF: {}, FEES: {}".format(ff,rf,fees))
	ff, rf, fees = fnb.get_buy_fees(53200)
	print("FF: {}, RF: {}, FEES: {}".format(ff,rf,fees))