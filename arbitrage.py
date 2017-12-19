import os
from datetime import datetime

from exchanges import ExchangeFactory

import pandas as pd
import argparse
import yaml

TRANSACTION_LOG_ITEM = {
	"timestamp": 0,
	"forex_type": "",
	"local_type": "",
	"token_type": "",
	"initial": 0,
	"forex": 0,
	"forex_rate": 0,
	"tokens": 0,
	"token_buy_rate": 0,
	"token_sell_rate": 0,
	"local": 0,
	"margin": 0,
	"profit": 0,
}

def log(msg, verbose):
	if verbose is True:
		print(msg)

# ZAR -> EUR, EUR -> BTC, BTC -> ZAR
def arbitrage(amount, buy_ex, sell_ex, forex_ex=None, forex_fees=True, log_mode="V", execute=False):
	initial_amount = amount
	forex_transaction = None

	verbose = False
	if log_mode == "V":
		verbose = True

	trans_store = TRANSACTION_LOG_ITEM.copy()

	trans_store["timestamp"] = datetime.utcnow().timestamp()
	trans_store["forex_type"] = buy_ex.currency_from
	trans_store["local_type"] = sell_ex.currency_from
	trans_store["token_type"] = buy_ex.currency_to
	trans_store["initial"] = amount

	start_ex = buy_ex
	if forex_ex:
		start_ex = forex_ex

	log("Arbitrage amount {:.2f} {}".format(amount, start_ex.currency_from), verbose)

	if forex_ex:
		forex_transaction = forex_ex.buy(amount, include_fees=forex_fees, execute=execute)
		log("Bought {:.2f} {} at a rate of {:.4f} {}".format(forex_transaction["bought"], forex_ex.currency_to,
			forex_transaction["rate"],forex_ex.currency_from), verbose)
		amount = forex_transaction["bought"]
		trans_store["forex_rate"] = forex_transaction["rate"]

	transaction = buy_ex.deposit(amount, include_fees=True, execute=execute)
	log("Deposited {:.2f} {}".format(transaction["deposited"], buy_ex.currency_from), verbose)

	trans_store["forex"] = transaction["deposited"]

	transaction = buy_ex.buy(transaction["deposited"], include_fees=True, execute=execute)

	log("Bought {:.6f} {} at a rate of {:.2f} {}".format(transaction["bought"], buy_ex.currency_to,
		transaction["rate"],buy_ex.currency_from), verbose)

	trans_store["token_buy_rate"] = transaction["rate"]

	transaction = buy_ex.send(transaction["bought"], include_fees=True, execute=execute)
	log("Sent {:.6f}{}".format(transaction["sent"], buy_ex.currency_to), verbose)

	transaction = sell_ex.receive(transaction["sent"], include_fees=True, execute=execute)
	log("Received {:.6f} {}".format(transaction["received"], sell_ex.currency_to), verbose)

	trans_store["tokens"] = transaction["received"]

	transaction = sell_ex.sell(transaction["received"], include_fees=True, execute=execute)
	log("Sold {:.2f} {} at a rate of {:.2f} {}".format(transaction["sold"], sell_ex.currency_from,
		transaction["rate"],sell_ex.currency_from), verbose)

	trans_store["token_sell_rate"] = transaction["rate"]

	transaction = sell_ex.withdrawl(transaction["sold"], include_fees=True, execute=execute)
	log("Withdrew {:.2f} {}".format(transaction["withdrew"], sell_ex.currency_from), verbose)

	profit = transaction["withdrew"] - initial_amount

	if forex_ex and forex_fees is False:
		profit -= forex_transaction["fees"]

	margin = profit/initial_amount*100

	trans_store["local"] = transaction["withdrew"]
	trans_store["profit"] = profit
	trans_store["margin"] = margin

	log("Profit: {:.2f} {}\tMargin:{:.3f}".format(profit, sell_ex.currency_from, margin), verbose)

	log_transaction(trans_store, mode=log_mode)

	return(profit, margin, trans_store)

def log_transaction(transaction, mode="STD"):
	if mode == "STD":
		print(transaction)
	elif mode == "CSV":
		df = pd.DataFrame.from_records([transaction])
		header = not os.path.exists("log_arbitrage.csv")
		df.to_csv("log_arbitrage.csv", mode='a', header=header, index=False)
		print("Logged to CSV: profit: {:.2f} margin: {:.2f}".format(transaction["profit"], transaction["margin"]))

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--forex", default="EUR", choices=["EUR", "USD", "ZAR"], help="Forex currency to use")
	parser.add_argument("--amount", type=float, help="Specify an amount to arbitrage")
	parser.add_argument("--local", default="ZAR", choices=["EUR", "USD", "ZAR"], help="Local currency to use for sale of tokens")
	parser.add_argument("--token", default="BTC", choices=["BTC", "ETH"], help="Token to arbitrage")
	parser.add_argument("--forex_ex", default="fnb", choices=ExchangeFactory.get_names() + ['none'], help="Exchange to use to buy forex")
	parser.add_argument("--sell_ex", default="luno", choices=ExchangeFactory.get_names(), help="Local exchange to sell on")
	parser.add_argument("--buy_ex", default="bitstamp", choices=ExchangeFactory.get_names(), help="Foreign exchange to buy on")
	parser.add_argument("--forex_with_fees", action="store_true", help="Assumes we want to include the forex fees in the arbitrage amount")
	parser.add_argument("--fmt", default="STD", choices=["CSV", "STD", "V"], help="How to display the output")
	parser.add_argument("--watch", type=int, default=0, help="Number of seconds to grab data in a loop, if zero will only run once")

	return(parser.parse_args())

def main(args):
	api_config = yaml.load(open("secrets.yml"))
	
	forex_ex = None
	if args.forex_ex != "none":
			forex_ex = ExchangeFactory.get("fnb", currency_to=args.forex)

	buy_keys = {"key": None, "secret": None}
	sell_keys = {"key": None, "secret": None}

	if args.buy_ex.lower() in api_config.keys():
		buy_keys = api_config[args.buy_ex.lower()]

	if args.sell_ex.lower() in api_config.keys():
		sell_keys = api_config[args.sell_ex.lower()]

	buy_ex = ExchangeFactory.get(args.buy_ex, **buy_keys, currency_from=args.forex, currency_to=args.token)
	sell_ex = ExchangeFactory.get(args.sell_ex, **sell_keys, currency_from=args.local, currency_to=args.token)

	verbose = False
	if args.fmt == "V":
		verbose = True

	if args.watch == 0:
		profit, margin, transaction = arbitrage(args.amount, buy_ex, sell_ex, forex_ex=forex_ex, forex_fees=args.forex_with_fees, execute=False, log_mode=args.fmt)
	else:
		from apscheduler.schedulers.background import BlockingScheduler
		scheduler = BlockingScheduler()
		scheduler.add_job(arbitrage, args=[args.amount, buy_ex, sell_ex], kwargs={"forex_ex":forex_ex, "forex_fees":args.forex_with_fees, "execute":False, "log_mode":args.fmt},
							trigger='interval', seconds=args.watch, id='arbitrager')
		scheduler.start()

if __name__ == "__main__":
	args = parse_args()
	main(args)
