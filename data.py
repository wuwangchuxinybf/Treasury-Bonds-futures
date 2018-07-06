# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 16:29:35 2018

@author: wuwangchuxin
"""

import pandas as pd
#import numpy as np
import os
import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
os.chdir(r'C:\Users\wuwangchuxin\Desktop\TF_SummerIntern')
marketdata = pd.read_excel(r'winddata\HPR_10years.xls')

# 计算均线
def MA(n,df):
    res = pd.rolling_mean(df,window = n)
    res[:n] = df[:n]
    return res
for n in [5,10,20,60,120]:
    marketdata['MA_%s'%n] = MA(n,marketdata['return'])

# 计算MACD
def get_EMA(df,N): 
    for i in range(len(df)):
        if i==0:
            df.loc[i,'ema']=df.loc[i,'return']
        if i>0:
            df.loc[i,'ema']=(2*df.loc[i,'return']+(N-1)*df.loc[i-1,'ema'])/(N+1)
    ema=list(df['ema'])
    return ema
def get_MACD(df,short=12,long=26,M=9):
    a=get_EMA(df,short)
    b=get_EMA(df,long)
    df['diff']=pd.Series(a)-pd.Series(b)
    for i in range(len(df)):
        if i==0:
            df.loc[i,'dea']=df.loc[i,'diff']
        if i>0:
            df.loc[i,'dea']=(2*df.loc[i,'diff']+(M-1)*df.loc[i-1,'dea'])/(M+1)
    df['macd']=2*(df['diff']-df['dea'])
    return df
data_dealed = get_MACD(marketdata,12,26,9)

# 均线策略
def MA_signal(M,N):
    if M>N:
        M,N=N,M
    elif M==N:
        return 'bad num'
    df1 = data_dealed['MA_%d'%M]  # [N:].reset_index(drop=True)
    df2 = data_dealed['MA_%d'%N]
    date = data_dealed['date']
    sig = pd.DataFrame(columns=['date','signal'])
    if len(df1)==len(df2):
        for i in range(N+1,len(df1)):
            # 金叉
            if df1[i]>df2[i] and df1[i-1]<df2[i-1]: 
                mid = pd.DataFrame([[date[i],'gold']],columns=['date','signal'])
                sig = sig.append(mid)
            # 死叉
            if df1[i]<df2[i] and df1[i-1]>df2[i-1]: 
                mid = pd.DataFrame([[date[i],'death']],columns=['date','signal'])
                sig = sig.append(mid)
        return sig
    else:
        return 'bad data'
res_5_20 = MA_signal(5,20)


def MACD_signal(df):
    data = df['macd']
    sig = pd.DataFrame(columns=['date','signal'])
    for i in range(1,len(data)):
        if data[i]>0 and data[i-1]<0:
            mid = pd.DataFrame([[df.loc[i,'date'],'buy']],columns=['date','signal'])
            sig = sig.append(mid)
        elif data[i]<0 and data[i-1]>0:
            mid = pd.DataFrame([[df.loc[i,'date'],'sell']],columns=['date','signal'])
            sig = sig.append(mid)
    return sig
res_MACD = MACD_signal(data_dealed)

#中证十年国债收益率（净值）
zz_10 = pd.read_excel(r'winddata\zz_10y_bond_netvalue.xlsx')


#backtest
res_5_20 = res_5_20[res_5_20['date']>='20090101']
res = pd.merge(zz_10,res_5_20,on='date',how='left')

# 均线策略
status=0 #持仓状态
ret_all=1 #净值
ret_curve = []
for nday in range(len(res)):
    if status==1 and nday<len(res)-1:
        ret_day = (res.loc[nday+1,'close']-res.loc[nday,'close'])/res.loc[nday-1,'close']
        ret_all = ret_all*(1+ret_day)
        ret_curve.append(ret_all)
    if res.loc[nday,'signal'] == 'death':
        status=1
    elif res.loc[nday,'signal'] == 'gold':
        status=0
plt.plot(ret_curve)

#MACD
res_MACD = res_MACD[res_MACD['date']>='20090101']
res2 = pd.merge(zz_10,res_MACD,on='date',how='left')

status2=0 #持仓状态
ret_all2=1 #净值
ret_curve2 = []
for nday2 in range(len(res2)):
    if status2==1 and nday2<len(res2)-1:
        ret_day2 = (res2.loc[nday2+1,'close']-res2.loc[nday2,'close'])/res2.loc[nday2-1,'close']
        ret_all2 = ret_all2*(1+ret_day2)
        ret_curve2.append(ret_all2)
    if res2.loc[nday2,'signal'] == 'sell':
        status2=1
    elif res2.loc[nday2,'signal'] == 'buy':
        status2=0
plt.plot(ret_curve2)

 


def main():
    




























fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(1,1,1)
#plt.plot(df['return'])
plt.plot(df['MA_5'])
#plt.plot(df['MA_10'])
plt.plot(df['MA_20'])
plt.plot(df['MA_60'])
plt.plot(df['MA_120'])


figsize = 160, 45
plt.subplots(figsize=figsize) 
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

















































