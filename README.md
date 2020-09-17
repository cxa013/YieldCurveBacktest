# Yield Curve strategy

My first attempt at rolling-my-own backtest. Done because I wanted to try a Yield Curve-based long-short S&P500 strategy, but the most readily accessible data was monthly, making other backtesting frameworks more difficult to use.

Not significantly tested -- mostly created out of curiosity with the Yield Curve/stock market relationship. Strategy does not work very well.

## Strategy
Long or short positions in S&P 500, based on the spread between 10y Treasuries and 3m T-bills.

Basically, invert the position to short each time the spread went negative and then invert back to a long position when it was no longer negative. 

A variety of alternative approaches were tried, e.g., inverting the position only when it was negative or positive on average over the month. None performed better than holding long.