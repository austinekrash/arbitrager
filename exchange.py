
class Exchange:
	def __init__(self, currency_from, currency_to):
		self.currency_from = currency_from
		self.currency_to = currency_to

	def get_current_rate(self):
		return(0)

	def buy(self, amount):
		return(0)

	def sell(self, amount):
		return(0)

	def send(self, amount):
		return(0)

	def receive(self, amount):
		return(0)

	def get_balances(self):
		return(0)

	# Returns fixed_fee, rate_fee
	def get_buy_fees(self):
		return(0)

	def get_sell_fees(self):
		return(0)

	def get_receive_fees(self):
		return(0)

	def get_send_fees(self):
		return(0)
