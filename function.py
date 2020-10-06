import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Preparing data

# Stock price data is taken lagging 1 month from the trends and sentiment data
df = pd.read_csv('TWTR.csv')
df.set_index('Date', inplace = True)

days = df.index.to_series()
days = pd.to_datetime(days)
# Closing prices on each friday
weekend_price = df[days.dt.day_name() == 'Friday'].Close

# Google trends data on searches for term := TWTR
trend = pd.read_csv('twtr_trends.csv')
trend.set_index('Date', inplace = True)
# Scaling to make trend := [0, 1]
trend = trend['Trend'] / 100

# Sentiment data on news throughout internet related to TWTR. Downloaded from Quandl and filtered to get TWTR sentiment data
sentiment = pd.read_csv('twtr_sentiment.csv')
sentiment.set_index('Date', inplace = True)
# Scaling to make sentiment := [-1, +1]
sentiment = sentiment['Sentiment'] / 5

# making weekly closing price data stationary
d1 = weekend_price.diff(periods = 1)    # First Degree Differencing on Raw Data
# removing NaN value
d1 = d1[1:]

logged_prices = np.log(weekend_price)   
logd1 = logged_prices.diff(periods = 1)    # First Degree Differencing on Logged Data
logd1 = logd1[1:]

square_root_prices = np.sqrt(weekend_price)
sd1 = square_root_prices.diff(periods = 1)    # First Degree Differencing on Square Root Data
sd1 = sd1[1:]

def acf_pacf_plots():
    plot_acf(d1)
    plot_pacf(d1)
    
    plot_acf(sd1)
    plot_pacf(sd1)
    # As evident from plots, the transformed stock	prices essentially follow ARIMA(0,1,0) process. This is	a random walk process


# Algorithm	for computing the value	of news at a certain time based on the google trend values and news articles sentiment values for that stock
a = trend * 0
for i in range(len(trend)):
    a[i] += trend[i] * sentiment[i]
    
news = trend * 0
count = np.zeros(len(a))
for j in range(len(news)):
    for i in range(len(a)):
        # Accounting for time effect of intrinsic value of news. The value of news would be mostly reflected in about 2 weeks in stock prices
        if j >= i:
            news[j] += a[i] * np.exp(-(j-i) / 7)
            count[j] += 1

def value_news_plot():    
    print (news)
    news.plot()

n_days = news.index.to_series()
n_days = pd.to_datetime(n_days)
# News value at start of each week
weekstart_news = news[n_days.dt.day_name() == 'Monday']

def weekstart_news_plot():
    print (weekstart_news)
    weekstart_news.plot()
    
# Regression of lagged weekly stock price changes on the news values at the beginning of each week
def regression():
    weekstart_news = news[n_days.dt.day_name() == 'Monday']
    weekstart_news = sm.add_constant(weekstart_news.ravel())
    results = sm.OLS(weekend_price,weekstart_news).fit()
    print (results.summary()) 
    
    plt.scatter(weekstart_news[..., 1], weekend_price)
    x = np.arange(-1.4, 1, 0.001)
    plt.plot(x, results.params[0] + x * results.params[1])
    plt.xlim(left = -1.4, right = 1)
    plt.show()

    """
                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                  Close   R-squared:                       0.071
    Model:                            OLS   Adj. R-squared:                  0.039
    Method:                 Least Squares   F-statistic:                     2.219
    Date:                Tue, 06 Oct 2020   Prob (F-statistic):              0.147
    Time:                        20:07:50   Log-Likelihood:                -92.185
    No. Observations:                  31   AIC:                             188.4
    Df Residuals:                      29   BIC:                             191.2
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    const         34.4420      1.175     29.313      0.000      32.039      36.845
    x1             4.7313      3.176      1.490      0.147      -1.764      11.227
    ==============================================================================
    Omnibus:                        7.061   Durbin-Watson:                   0.462
    Prob(Omnibus):                  0.029   Jarque-Bera (JB):                5.889
    Skew:                           1.054   Prob(JB):                       0.0526
    Kurtosis:                       3.345   Cond. No.                         3.85
    ==============================================================================
    """
    
    # Clearly there are outlier that point well above regression line in the negative region.
    # Also the coefficient is 4.713 but the R square is just 0.071 which is very low thus the
    # regression does not explain the variance in the data results. Removing these
    # outliers we check for regression again

def regression_without_outliers():
    weekend_price_outlier_removed = pd.concat([weekend_price[:7], weekend_price[10:]])
    weekstart_news_outlier_removed = pd.concat([weekstart_news[:7], weekstart_news[10:]])
    
    weekstart_news_outlier_removed = sm.add_constant(weekstart_news_outlier_removed.ravel())
    results = sm.OLS(weekend_price_outlier_removed,weekstart_news_outlier_removed).fit()
    print (results.summary()) 
    
    plt.scatter(weekstart_news_outlier_removed[..., 1], weekend_price_outlier_removed)
    x = np.arange(-1.4, 1, 0.001)
    plt.plot(x, results.params[0] + x * results.params[1])
    plt.xlim(left = -1.4, right = 1)
    plt.show()

    """
                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                  Close   R-squared:                       0.316
    Model:                            OLS   Adj. R-squared:                  0.290
    Method:                 Least Squares   F-statistic:                     12.03
    Date:                Tue, 06 Oct 2020   Prob (F-statistic):            0.00184
    Time:                        19:59:02   Log-Likelihood:                -80.302
    No. Observations:                  28   AIC:                             164.6
    Df Residuals:                      26   BIC:                             167.3
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    const         36.4301      1.252     29.104      0.000      33.857      39.003
    x1            17.3900      5.014      3.468      0.002       7.083      27.697
    ==============================================================================
    Omnibus:                        2.941   Durbin-Watson:                   0.776
    Prob(Omnibus):                  0.230   Jarque-Bera (JB):                1.752
    Skew:                           0.591   Prob(JB):                        0.416
    Kurtosis:                       3.326   Cond. No.                         6.22
    ==============================================================================
    """
    
    # This gives really good correlation value. The coefficient has a higher value (36.4301)
    # and R square also has a much higher value than before but not that good(only explains 31.6 % of variance in data)