from pandas_datareader.data import DataReader as dr
import numpy as np

class Stocks:
    def __init__(self, tickers, data_source='yahoo', start=None, end=None):
        # ajusta os nomes dos tickers
        name_tickers=[i+'.SA' if i[-3:] != '.SA' and i!='IBOV' else '^BVSP' if  i=='IBOV' else i   for i in tickers]
        #self.series=[dr(t, data_source=data_source, start=start, end=end) for t in tickers]
        self.tickers={i: dr(t, data_source=data_source, start=start, end=end) for i, t in zip(tickers, name_tickers)}

    def __getitem__(self, ticker):
        return self.tickers[ticker]
    
    # Cria uma coluna com os retornos para cada ativo
    def set_returns(self):
        for i in self.tickers:
            self.tickers[i]['Return']=np.log(self.tickers[i]['Adj Close']/self.tickers[i]['Adj Close'].shift(1))
            
    # Retorna uma lista de listas de retornos
    def get_returns(self):
        self.set_returns()
        return [df['Return'].tolist()[1:] for df in self.tickers.values()]


