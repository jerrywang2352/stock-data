import requests
import pandas as pd
import numpy as np
import csv
class AnalyzeStock:   
    def __init__(self, stocks, initial_weight,days):
        '''
        api_key (string) -> key to financialmodelingprep
        stocks (list) -> list of stock tickers
        initial_weight (np array) -> list of stock weighting
        days (int) -> number of days
        portoflio (dataframe) -> dataframe of stock closing price
        self.empresas (dict) -> dictionary of stock closing price by date
        '''
        self.api_key = "5e45f536a54b40410e7c1bc47e904dc1"
        self.stocks = stocks
        self.initial_weight = initial_weight
        self.days = days
        self.empresas = {}
        for stock in self.stocks:
            prices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={self.api_key}").json()
            prices = prices['historical'][:self.days] #gets the price for a stock for a past number of days
            prices = pd.DataFrame(prices) 
            
            self.empresas[stock] = prices.set_index('date') 
            self.empresas[stock] = self.empresas[stock]['close']
            
        self.portfolio = pd.concat(self.empresas, axis=1) #creates dataframe of stocks by columns and closing price by rows
        portfolio = pd.DataFrame(self.portfolio)
        self.return_stocks = portfolio.pct_change(-1).iloc[:-1,:]
        
    def graph_return(self):
        '''Graph cumulative return of a portfolio for past number of days'''
        return_stocks = self.portfolio.pct_change(-1)  #creates dataframe of stocks by columns and percent change by rows  
        daily_returns_portfolio_mean = return_stocks.mean() #calculates average of portfolio percent change 
        allocated_daily_returns = (self.initial_weight * daily_returns_portfolio_mean) #finds average daily return of each stock       
        portfolio_return = np.sum(allocated_daily_returns) #find average daily return of whole portfolio 
        
        # calculate portfolio daily returns
        return_stocks['portfolio_daily_returns'] = return_stocks.dot(self.initial_weight.reshape(len(self.stocks),1))
        return_stocks = return_stocks[:-1]
        
        flipArray = np.array(return_stocks['portfolio_daily_returns'])
        flipArray = np.flip(flipArray)

        return_stocks['cum_return'] = np.flip((1+flipArray).cumprod())
        plot = return_stocks['cum_return'].plot() 
        
        plot.invert_xaxis()

    def calc_risk(self):
        '''Calculate portfolio risk using covariance matrix'''
        stdev_df = self.portfolio 
        
        
        for column in stdev_df.columns: 
            mean = stdev_df[column].mean()
            
            stdev_df[column] -= mean #demeans the prices
        
        #create covariance matrix
        covariance_matrix = stdev_df.T.dot(stdev_df)
        covariance_matrix /= self.days
        

        
        portfolio_variance = self.initial_weight.dot(covariance_matrix)
        portfolio_variance = portfolio_variance.dot(self.initial_weight.T)

        portfolio_risk = np.sqrt(portfolio_variance)
        return portfolio_risk
        
    def calc_pct_risk(self):
        '''Calculate portfolio risk in percentage using covariance matrix'''
        stdev_df = self.return_stocks 
        
        
        for column in stdev_df.columns: 
            mean = stdev_df[column].mean()
            
            stdev_df[column] -= mean #demeans the prices
        
        #create covariance matrix
        covariance_matrix = stdev_df.T.dot(stdev_df)
        covariance_matrix /= self.days
        
        
        portfolio_variance = self.initial_weight.dot(covariance_matrix)
        portfolio_variance = portfolio_variance.dot(self.initial_weight.T)

        portfolio_risk = np.sqrt(portfolio_variance)
        return portfolio_risk
    
    def write_DCF_csv(self,loc,stock):
        '''writes a csv file retrieving information for a discounted cash flow model
        loc (str)-> file locations
        stocks (str) -> stock from which to retrieve data'''
        incomeStatement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{stock}?limit=120&apikey={self.api_key}").json()
        balanceSheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?limit=120&apikey={self.api_key}").json()
        cashFlow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?limit=120&apikey={self.api_key}").json()
        value = requests.get(f"https://financialmodelingprep.com/api/v3/enterprise-values/{stock}?limit=40&apikey={self.api_key}").json()
        
        revenue = ["Total Revenue"]
        growth = ["Growth",""]
        EBIT = ["EBIT"]
        margin = ["Margin"]
        FCF = ["FCF"]
        FCF_EBIT = ["FCF as % of EBIT"]
        share = ["Shares Outstanding"]
        cash = ["Cash & Cash Equivalents"]
        nonCash = ["Non-Operating Cash"]
        debt = ["Total Debt"]
        inCap = ["Invested Capital"]
        wCap = ["Working Capital"]
        cAsset = ["Current Assets"]
        cLiab = ["Current Liabilities"]
        equity = ["Shareholder Equity"]
        cap = ["Market Cap"]
        EV = ["Enterprise Value"]
        price = ["Share Price"]
        EV_EBIT = ["EV/EBIT"]
        for i in range(4,-1,-1):
            #Total Revenue
            revenue.append(incomeStatement[i]["revenue"])

            #Growth
            if i != 4:
                growth.append(incomeStatement[i]["revenue"]/incomeStatement[i+1]["revenue"]-1)
                
            
            #EBIT
            EBIT.append(incomeStatement[i]["ebitda"]-incomeStatement[i]["depreciationAndAmortization"])
            
            #Margin
            margin.append(EBIT[5-i]/revenue[5-i])

            #FCF 
            FCF.append(cashFlow[i]["freeCashFlow"])
            
            #FCF as % of EBIT
            FCF_EBIT.append(FCF[5-i]/EBIT[5-i])

            #Shares Outstanding
            share.append(balanceSheet[i]["commonStock"])

            #Cash & Cash Equivalents
            cash.append(balanceSheet[i]["cashAndCashEquivalents"])
            
            #Non-Operating Cash
            
            #Total Debt
            debt.append(balanceSheet[i]["totalDebt"])

            #Invested Capital
            inCap.append(balanceSheet[i]["totalDebt"] + balanceSheet[i]["totalEquity"])
            
            #Working Capital
            wCap.append(balanceSheet[i]["totalCurrentAssets"]-balanceSheet[i]["totalCurrentLiabilities"])
            
            #Current Assets
            cAsset.append(balanceSheet[i]["totalCurrentAssets"])
            
            #Current Liabilities
            cLiab.append(balanceSheet[i]["totalCurrentLiabilities"])
            
            #Shareholder Equity
            equity.append(balanceSheet[i]["totalStockholdersEquity"])

            #Market Cap
            cap.append(value[i]["marketCapitalization"])
            
            #Enterprise Value
            EV.append(value[i]["enterpriseValue"])
            
            #Share Price
            price.append(value[i]["stockPrice"])

            #EV/EBIT
            EV_EBIT.append(EV[5-i]/EBIT[5-i])
            
        with open(loc,'w',newline = "") as f: 
            writer = csv.writer(f)
            writer.writerow(["","2016","2017","2018","2019","2020","2021 (TTM)"])
            writer.writerow(revenue)
            writer.writerow(growth)
            writer.writerow([""])
            writer.writerow(EBIT)
            writer.writerow(margin)
            writer.writerow([""])
            writer.writerow(FCF)
            writer.writerow(FCF_EBIT)
            writer.writerow([""])
            writer.writerow(share)
            writer.writerow([""])
            writer.writerow(cash)
            writer.writerow(nonCash)
            writer.writerow(debt)
            writer.writerow([""])
            writer.writerow(inCap)
            writer.writerow(wCap)
            writer.writerow(cAsset)
            writer.writerow(cLiab)
            writer.writerow(equity)
            writer.writerow([""])
            writer.writerow(cap)
            writer.writerow(EV)
            writer.writerow(price)
            writer.writerow(EV_EBIT)
 