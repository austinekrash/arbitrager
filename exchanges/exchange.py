import numpy as np 

class Exchange:
	def __init__(self, currency_from=None, currency_to=None):
		self.currency_from = currency_from
		self.currency_to = currency_to

		self.buy_fees = {"fixed": 0, "variable": 0}
		self.sell_fees = {"fixed": 0, "variable": 0}
		self.send_fees = {"fixed": 0, "variable": 0}
		self.receive_fees = {"fixed": 0, "variable": 0}
		self.deposit_fees = {"fixed": 0, "variable": 0}
		self.withdrawl_fees = {"fixed": 0, "variable": 0}

	def _set_fees(self, fee_dict, fixed=None, variable=None):
		if fixed:
			fee_dict["fixed"] = fixed
		if variable:
			fee_dict["variable"] = variable

	def _transaction_split(self, amount, fixed_fee, var_fee, include_fees=None):
		if include_fees:
			amount = (amount - fixed_fee)/(1+var_fee)

		fees = fixed_fee + amount*var_fee
		
		return({"amount": amount, "fees": fees})

	def get_current_buy_rate(self):
		return(0)

	def get_current_sell_rate(self):
		return(self.get_current_buy_rate())

	def buy(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.buy_fees["fixed"], self.buy_fees["variable"]
		transaction = self._transaction_split(amount, fixed_fee, var_fee, include_fees=include_fees)
		rate = self.get_current_buy_rate()
		bought = transaction["amount"]/rate

		return({"bought": bought, "buy_amount": transaction["amount"], "fees": transaction["fees"], "rate": rate})

	def sell(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.sell_fees["fixed"], self.sell_fees["variable"]
		transaction = self._transaction_split(amount, fixed_fee, var_fee, include_fees=include_fees)
		rate = self.get_current_sell_rate()
		sold = transaction["amount"]*rate

		return({"sold": sold, "sell_amount": transaction["amount"], "fees": transaction["fees"], "rate": rate})

	def send(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.send_fees["fixed"], self.send_fees["variable"]
		transaction = self._transaction_split(amount, fixed_fee, var_fee, include_fees=include_fees)

		return({"sent": transaction["amount"], "fees": transaction["fees"]})

	def receive(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.receive_fees["fixed"], self.receive_fees["variable"]
		transaction = self._transaction_split(amount, fixed_fee, var_fee, include_fees=include_fees)

		return({"received": transaction["amount"], "fees": transaction["fees"]})

	def deposit(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.deposit_fees["fixed"], self.deposit_fees["variable"]
		transaction = self._transaction_split(amount, fixed_fee, var_fee, include_fees=include_fees)

		return({"deposited": transaction["amount"], "fees": transaction["fees"]})

	def withdrawl(self, amount, include_fees=True, execute=False):
		fixed_fee, var_fee = self.withdrawl_fees["fixed"], self.withdrawl_fees["variable"]
		transaction = self._transaction_split(amount, fixed_fee, var_fee, include_fees=include_fees)

		return({"withdrew": transaction["amount"], "fees": transaction["fees"]})

	def get_balances(self):
		return({self.currency_from: 0, self.currency_to: 0})

	def set_buy_fees(self, fixed=None, variable=None):
		self._set_fees(self.buy_fees, fixed, variable)

	def set_sell_fees(self, fixed=None, variable=None):
		self._set_fees(self.sell_fees, fixed, variable)

	def set_receive_fees(self, fixed=None, variable=None):
		self._set_fees(self.receive_fees, fixed, variable)

	def set_send_fees(self, fixed=None, variable=None):
		self._set_fees(self.send_fees, fixed, variable)

	def set_withdrawl_fees(self, fixed=None, variable=None):
		self._set_fees(self.withdrawl_fees, fixed, variable)

	def set_deposit_fees(self, fixed=None, variable=None):
		self._set_fees(self.deposit_fees, fixed, variable)

	def get_buy_fees(self):
		return(self.buy_fees)

	def get_sell_fees(self):
		return(self.sell_fees)

	def get_receive_fees(self):
		return(self.receive_fees)

	def get_send_fees(self):
		return(self.send_fees)
