# Stock-Price-Forecasting-Using-Information-from-Yahoo-Finance-and-Google
Predicting Stock Price on the basis of a combination of fundamenta data (google trends data and sentiment data) and technical data(stock price) collected for TWTR (Twitter Inc)

TL;DR
-------

Through this paper, we first apply the conventional ARMA time series analysis on the historical weekly stock prices of TWTR and obtain forecasting results. Then we propose an algorithm to evaluate news/events related to TWTR stock using information from the sentiment values and the Google trend website. We then regress the changes in weekly stock prices on the values of the news at the beginning of the week. We aim to use this regression result to study the relationship between news and stock price changes and improve the performance of the conventional stock price forecasting process.

Install
-------

This project uses [backtrader](https://www.backtrader.com/). Go check them out if you don't have them locally installed.

```source-shell
$ pip install backtrader[plotting]
```
Datasets
-------

This work is based on the attached paper. Read through the paper to get a good understanding on how to approach a combination of fundamental and technical data for understanding stock price movements. I could not find Key Development Features (Yahoo has discontinued that API as it violated policies because yahoo extracted most information from external news websites like Reuters) so had to use sentiment indicator which I found on Quandl [here](https://www.quandl.com/databases/NS1/data). I filtered the TWTR ticker data from sample data of this dataset. Accordingly I downloaded the appropriate [OHLC data](https://in.finance.yahoo.com/quote/TWTR/history?p=TWTR) and [google trends](https://trends.google.com/trends/?geo=US) (for TWTR). I have added all time adjusted in this repo. I have added all the resultant plots in plots folder.



Contributing
------------

Feel free to dive in! Open an issue or submit PRs.

