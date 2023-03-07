import numpy as np

class BuyAndHold():
    def __init__(self,df,col):
        self.df =df
        self.col =col

    def drop_na(self):
        self.df = self.df[~self.df.isin([np.nan,np.inf,np.inf]).any(1)]
        return self.df
    
    def add_col(self):
        self.df["daily_rtn"] = self.df[self.col].pct_change()
        self.df["st_rtn"]  = (1 + self.df["daily_rtn"]).cumprod()
        return self.df

    
    ## 백테스팅 함수
    def testing(self) : 
        self.historical_max = self.df[self.col].cumsum()
        self.daily_drawdown = self.df[self.col]/self.historical_max -1.0
        self.historical_min = self.daily_drawdown.cummin()
        self.last_date = self.df.index[-1]
        self.CAGR = self.df.loc[self.last_date,'st_rtn'] **(252/len(self.df))-1
        self.sharpe = np.mean(self.df['daily_rtn']) / np.std(self.df["daily_rtn"]) * np.sqrt(252)
        self.VOL = np.std(self.df['daily_rtn'])*np.sqrt(252)
        self.MDD = self.historical_min.min()
        return [self.CAGR,self.sharpe,self.VOL,self.MDD]

class Bollinger():
    def __init__(self,df,col,start):
        self.df = df
        self.col =col
        self.start =start

    def testing(self):
         ## 결측치 , 이상치를 제거
        self.df = self.df[~self.df.isin([np.nan, np.inf, -np.inf]).any(1)]
        ## 해당 컬럼만 남기고 나머지 컬럼은 삭제
        self.df = self.df.loc[:, [self.col]]
        ## 이동 평균선, 상단 밴드, 하단 밴드 생성
        self.df['center'] = self.df[self.col].rolling(20).mean()
        self.df['ub'] = self.df['center'] + ( 2 * self.df[self.col].rolling(20).std() )
        self.df['lb'] = self.df['center'] - ( 2 * self.df[self.col].rolling(20).std() )

        self.df = self.df.loc[self.start :]

        self.df['trade']=""

        ## trade에 거래 내역 추가
        for i in self.df.index:
            if self.df.loc[i,self.col] > self.df.loc[i,'ub']:
                if self.df.shift(1).loc[i, 'trade'] == "buy":
                    self.df.loc[i, 'trade'] = ""
                else : 
                    self.df.loc[i, 'trade'] = ""
            elif self.df.loc[i, self.col] < self.df.loc[i, 'lb']:
                if self.df.shift(1).loc[i, 'trade'] == "buy":
                    self.df.loc[i, 'trade'] = 'buy'
                else : 
                    self.df.loc[i, 'trade'] = 'buy'
            elif self.df.loc[i, self.col] >= self.df.loc[i, 'lb'] and \
                self.df.loc[i, self.col] <= self.df.loc[i, 'ub']:
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = 'buy'
                else:
                    self.df.loc[i, 'trade'] = ""
    
    ##retun 이라는 컬럼 생성 값은 1
        self.df['return'] = 1
        self.rtn = 1
        self.buy = 0
        self.sell = 0
        for i in self.df.index:
             ## 구매가를 출력
            if self.df.shift(1).loc[i, "trade"] == '' and \
                self.df.loc[i, 'trade'] == 'buy':
                self.buy = self.df.loc[i, self.col]
                print('진입일 :', i, "구매 가격 :", self.buy)
            ## 판매가를 출력
            elif self.df.shift(1).loc[i, 'trade'] == 'buy' and \
                self.df.loc[i, 'trade'] == '':
                self.sell = self.df.loc[i, self.col]
                self.rtn = (self.sell - self.buy) / self.buy + 1
                self.df.loc[i, 'return'] = self.rtn
                print('청산일 :', i, "판매 가격 :", self.sell, "수익율 :", round(self.rtn, 4))
            
            ## buy, sell 변수를 초기화
            if self.df.loc[i, 'trade'] == "":
                self.buy = 0.0
                self.sell = 0.0
        
        self.acc_rtn = 1.0

        for i in self.df.index:
            self.rtn = self.df.loc[i, 'return']
            self.acc_rtn *= self.rtn
            self.df.loc[i, 'acc_rtn'] = self.acc_rtn
        
        print("누적수익율 : " ,round(self.acc_rtn,2))

        return self.df