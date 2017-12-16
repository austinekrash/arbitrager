import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from datetime import datetime

def plot_transaction_log(log, start_date="", end_date=""):
    ts = [ mdate.date2num(datetime.fromtimestamp(d)) for d in log["timestamp"].values ]
    xformat = mdate.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax = plt.gca()
    plt.subplots_adjust(bottom=0.2, right=0.8)
    plt.xticks(rotation=25)
    ax.xaxis.set_major_locator(mdate.MinuteLocator(interval=60))
    ax.xaxis.set_major_formatter(xformat)
    ax2 = plt.twinx(ax=ax)
    ax3 = plt.twinx(ax=ax)

    ax.set_ylabel("Profit")
    ax2.set_ylabel("EUR Buy Price")
    ax2.tick_params('EBP', colors='b')
    ax3.set_ylabel("ZAR Sell Price")
    ax3.tick_params('ZSP', colors='k')

    # Move the last y-axis spine over to the right by 20% of the width of the axes
    ax3.spines['right'].set_position(('axes', 1.1))
    ax3.set_frame_on(True)
    ax3.patch.set_visible(False)

    p = ax.plot(ts, log["profit"].values, "r", label="Profit")
    p2 = ax2.plot(ts, log["token_buy_rate"].values, "b", label="Buy Price")
    p3 = ax3.plot(ts, log["token_sell_rate"].values, "k", label="Sell Price")

    plt.draw()
    plt.show()

def load_log(f_name):
    return(pd.read_csv(f_name))

if __name__=="__main__":
    df = load_log("log_arbitrage.csv")
    plot_transaction_log(df)
