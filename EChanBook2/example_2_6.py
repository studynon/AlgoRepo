import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from functions import *



""" This is an implementation of the example 2.6  from Ernest Chan's
book ALGORITHMIC TRADING - Winning Strategies and Their Rationale
"""
 
     
if __name__ == "__main__":
   
    #import data from CSV file
    root_path = '/Users/Javi/Documents/MarketData/'
    # the paths
    # MAC: '/Users/Javi/Documents/MarketData/'
    # WIN: 'C:/Users/javgar119/Documents/Python/Data'
    filename_x = 'EWC_EWA_daily.csv'
    #filename_y = 'ECOPETROL_ADR.csv'
    full_path_x = root_path + filename_x
    #full_path_y = root_path + filename_y
    data = pd.read_csv(full_path_x, index_col='Date')
    #create a series with the data range asked
    #start_date = '2009-10-02'
    #end_date = '2011-12-30'
    #data =  subset_dataframe(data, start_date, end_date)
    
 
    y = data['EWC']
    x = data['EWA']
    
    y_ticket = 'EWC'
    x_ticket = 'EWA'

    
   # z = data['IGE']
    k = polyfit(x,y,1)
    xx = linspace(min(x),max(x),1000)
    yy = polyval(k,xx)
 
    lookback = 100
    modelo2 = pd.ols(y=y, x=x, window_type='rolling', window=lookback)
    data = data[lookback-1:]
    betas = modelo2.beta
    #calculate the number of units for the strategy
    numunits = subtract(data[x_ticket], multiply(betas['x'], data[y_ticket]))

    model = sm.OLS(y, x)
    results = model.fit()
    #print(results.params)
    
    
    # cointegration test
    resultsCOIN = cointegration_test(x,y)
    print('****** COINTEGRATION TEST RESULTS FOR {} & [] *****'.format(x_ticket, y_ticket))
    print('cointegration t-stat: {}'.format(round(resultsCOIN[0],4)))
    print('p-value: {}'.format(round(round(resultsCOIN[1],4))))
    print('usedlag: {}'.format(round(round(resultsCOIN[2],4))))
    print('nobs: {}'.format(round(resultsCOIN[3],4)))
    print('critical values: {}'.format(resultsCOIN[4]))
        
    

    #*************************************************
    # plotting the chart
    #*************************************************    
    #plot of numunits
    fig = plt.figure()
    ax = fig.add_subplot(311)
    ax.plot(data)
    ax.set_title(x_ticket + ' & ' + y_ticket)
    ax.set_xlabel('Data points')
    ax.set_ylabel('Price')
    #ax.text(1000, -12, 'Seems like mean reverting')
    
    #plot of datapoints
    ax = fig.add_subplot(312)
    ax.plot(numunits)
    ax.set_title(x_ticket + ' - (HedgeRatio * ' +  y_ticket + ')')
    ax.set_xlabel(x_ticket)
    ax.set_ylabel(y_ticket)

    #plot of datapoints
    ax = fig.add_subplot(313)
    ax.plot(x,y,'o')
    ax.plot(xx,yy,'r')
    ax.set_title(x_ticket + ' vs. ' +  y_ticket)
    ax.set_xlabel(x_ticket)
    ax.set_ylabel(y_ticket)
    
    
    plt.show()
    
    
    
