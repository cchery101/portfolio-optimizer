#import libraries
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np

c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

#creating the structures we will need when we read the data in
symbols = ["AAPL","GOOG","IBM","MSFT"]
startDate = dt.datetime(2011, 1, 1)
endDate = dt.datetime(2011, 12, 31)
timeOfDay = dt.timedelta(hours=16) 
timestamps = du.getNYSEdays(startDate, endDate, timeOfDay)

#read the data in
dataObj = da.DataAccess('Yahoo')
keys = ['close']
ldf_data = dataObj.get_data(timestamps, symbols, keys)
d_data = dict(zip(keys, ldf_data))


#create the plot
prices = d_data['close'].values


#normalize the data
normalized_prices = prices/prices[0,:]




#find normalized total portfolio value each day (sum of securities' normalized daily values)

daily_portfolio_value = normalized_prices[:,0] + normalized_prices[:,1] + normalized_prices[:,2] + normalized_prices[:,3]

daily_portfolio_value = daily_portfolio_value.copy()



print "Start Date: ",startDate
print "End Date: ",endDate
print "Symbols: ",symbols

#function to tell us the standard deviation, daily mean, Sharpe Ratio, and cumulate daily 
def simulate(startdate, enddate, symbols, weights):
    daily_return = tsu.returnize0(daily_portfolio_value)

    mean = np.mean(daily_portfolio_value)

    standard_deviation = np.std(daily_portfolio_value)

    sharpe = (np.sqrt(252) * mean)/standard_deviation

    cumulative_daily_return = np.cumprod(1 + daily_portfolio_value, axis = 0)

    return standard_deviation, mean, sharpe, cumulative_daily_return

vol, daily_ret, sharpe, cum_ret = simulate(startDate, endDate, symbols, [0.2,0.3,0.4,0.1])


print "Sharpe Ratio: ", sharpe
print "Volatility: (stdev of daily returns): ", vol
print "Average Daily Return: ",daily_ret
cum_ret = cum_ret[len(cum_ret) - 1]
print "Cumulative Return: ", cum_ret


#find the optimal portfolio

a = 0
b = 0
c = 0
d = 0

#initalize variables to 0
optimal_sharpe = 0

optimal_weights = [0,0,0,0]

startDate = dt.datetime(2011, 1, 1)
endDate = dt.datetime(2011, 12, 31)


#nested while loops to loop through each weight in .1 incremets for each security a, b, c, and d        
while a < 1.1:
    b = 0
    c = 0
    d = 0
    while b < 1.1:
        c = 0
        d = 0
        while c <= 1 - (a + b):
           
            d = 1 - (a+b+c)

            daily_portfolio_value = normalized_prices[:,0]*a + normalized_prices[:,1]*b + normalized_prices[:,2]*c + normalized_prices[:,3]*d

            daily_portfolio_value = daily_portfolio_value.copy()
            
            daily_return = tsu.returnize0(daily_portfolio_value)

            mean = np.mean(daily_portfolio_value)
    
            standard_deviation = np.std(daily_portfolio_value)

            sharpe = (np.sqrt(252) * mean)/standard_deviation

            cumulative_daily_return = np.cumprod(1 + daily_portfolio_value, axis = 0)

            
            #hold the highest Sharpe Ratio & optimal weights (check each iteration and hold the new value if it is higher than the current value
            if sharpe > optimal_sharpe:
                optimal_sharpe = sharpe
                optimal_weights = [a,b,c,d]
            
            c = c + .1
        b = b + .1
    a = a + .1

print "Optimal Sharpe Ratio: ", optimal_sharpe
print "Optimal Weights: ", optimal_weights

#end








