# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:41:40 2021

@author: kevin
"""
import pandas as pd
import numpy as np
import math

## building fall class
def drop_estimate(df, day , upper , lower):
    i=0
    label = "d" + str(day) + "_" + str(upper)
    list_ = []
    while i < len(df):
        try :
            UP = df['收盤價'][i+1:i+day+1].tolist()
            LP = df['最高價'][i+1:i+day+1].tolist()
            U =(min(UP)-float(df['開盤價'][i+1]))/float(df['開盤價'][i+1]+0.0001)
            L =(max(LP)-float(df['開盤價'][i+1]))/float(df['開盤價'][i+1]+0.0001) 
            
            if ( U < -upper ) :
                if (L > -lower ) and (LP.index(max(LP)) < UP.index(min(UP))):
                    list_.append(0)
                else:
                    list_.append(1)                   
            else :
                list_.append(0)
        except Exception as e:
            print(e, i )
            list_.append(0)
        i+=1
    df[label] = list_
    
## building rise class
def rise_estimate(df, day , upper , lower):
    i=0
    label = "p" + str(day) + "_" + str(upper)
    list_ = []
    while i < len(df):
        try :
            UP = df['收盤價'][i+1:i+day+1].tolist()
            LP = df['最低價'][i+1:i+day+1].tolist()
            U =(max(UP)-float(df['開盤價'][i+1]))/float(df['開盤價'][i+1]+0.0001)
            L =(min(LP)-float(df['開盤價'][i+1]))/float(df['開盤價'][i+1]+0.0001)
            
            if U > upper :
                if ((L < lower) and ( LP.index(min(LP)) < UP.index(max(UP)))) :
                    list_.append(0)
                else:
                    list_.append(1)
            else :
                list_.append(0)
        except Exception as e:
            print(e, i )
            list_.append(0)
        i+=1
    df[label] = list_

# featur-------------------------------------
def shift_price(df, day , upper ):
    i=0
    label_drop = "pre" + str(day) + "d" + str(upper)
    label_rise = "pre" + str(day) + "p" + str(upper)
    list_d = [0 for x in range(day)]
    list_p = [0 for x in range(day)]
    while i < (len(df) -day):
        try :        
            D =((df['最低價'][i-day])-float(df['收盤價'][i]))/float(df['收盤價'][i])
            if -D > upper :
                list_d.append(1)
            else :
                list_d.append(0)                
        except Exception as e:
            if i > 5:
                print(e , i)
            list_d.append(0)
            
        try : 
            U =((df['最高價'][i-day])-float(df['收盤價'][i]))/float(df['收盤價'][i])
            if U > upper :
                list_p.append(1)
            else :
                list_p.append(0)                
        except Exception as e:
            if i > 5:
                print(e , i)
            list_p.append(0)
        i+=1
    df[label_drop] = list_d
    df[label_rise] = list_p

def 前高(df,test_):
    i=0
    LP = 0 
    day = 0
    while i<len(df):         
        try:
            if (i < 60):
                test_.append(0)
            else:
                P = max(df['最高價'][i-60:i])
                if (P > LP) :
                    test_.append(P)
                    LP = P
                    day = i
                elif (day < (i-250)) :
                    test_.append(P)
                    LP = P
                    day = i
                else :
                    test_.append(LP)
        except Exception as e:
            print(e , i)
            test_.append(0)
        i+=1


def 波段前高(df,test_):
    i=0
    while i<len(df):         
        try:
            if (i < 60):
                test_.append(0)
            else:
                P = max(df['最高價'][i-60:i])
                test_.append(P)
        except Exception as e:
            print(e , i)
            test_.append(0)
        i+=1

def 增加技術指標MA(df,day,label,test_):
    i=0    
    while i<len(df):
        try:
            if (i < day-1):
                test_.append(0)
            else :
                test_.append(sum(df[label][i-day:i+1])/day)
        except:
            if i > day :
                print("Hi, i got troble in ", i)
            test_.append(0)
        i+=1
        
def MA交叉型態(df):
    i=0
    list_=[]   
    while i <len(df):
        try:
            if(df['MA5'][i]>df['MA10'][i]):
                if(df['MA5'][i-1]<df['MA10'][i-1]):
                    list_.append(1)
                    list_.append(1)
                    i += 1
                else:
                    list_.append(0)
            else:
                if(df['MA5'][i-1]>df['MA10'][i-1]):
                    list_.append(-1)
                    list_.append(-1)
                    i += 1
                else:
                    list_.append(0)
        except Exception as e:
            print(e)
            list_.append(0)
        i+=1
    df['MA交叉型態'] = list_
    
def KD(df):
    i=0
    list_K = []
    list_D = []
    while i < len(df):
        try:
            RSV=(float(df['收盤價'][i])-min(df['最低價'][i-9:i]))/((max(df['最高價'][i-9:i])-min(df['最低價'][i-9:i]))+0.0001)*100
            K = 2/3*list_K[i-1] + 1/3*RSV
            
            if K > 99 :
                K = 99
            elif K < 1 :
                K = 1

            list_K.append(K)
            list_D.append(2/3*list_D[i-1]+1/3*list_K[i-1])
        except Exception as e :
            list_K.append(50)
            list_D.append(50)
            if i > 9 :
                print(e)
                print (i,list_K[i-1])            
        i+=1
    df['K'] = list_K
    df['D'] = list_D    
    
#黃金交叉=1 死亡交叉=2 沒有交叉=3
def KD交叉型態(df):
    i=0
    list_ = []   
    while i<len(df):
        try:
            if(df['K'][i]>df['D'][i]):
                if(df['K'][i-1]<df['D'][i-1]):
                    list_.append(1)
                else:
                    list_.append(0)
            else:
                if(df['K'][i-1]>df['D'][i-1]):
                    list_.append(-1)
                else:
                    list_.append(0)
        except Exception as e:
            list_.append(0)
            if i >0 :                
                print(e)
        i+=1
    df['KD交叉型態'] = list_
    
# keep the index for the later three days
def KD交叉型態2(df):
    i=0
    list_ = []   
    while i<len(df):
        try:
            if(df['K'][i]>df['D'][i]):
                if(df['K'][i-1]<df['D'][i-1]):
                    list_.append(1)
                    list_.append(1)
                    list_.append(1)
                    i+=2
                else:
                    list_.append(0)
            else:
                if(df['K'][i-1]>df['D'][i-1]):
                    list_.append(-1)
                    list_.append(-1)
                    list_.append(-1)
                    i+=2
                else:
                    list_.append(0)
        except Exception as e:
            if i >0 :                
                print(e)
            list_.append(0)
        i+=1
    df['KD交叉型態2'] = list_[0:len(df['date'])]

def 漲跌(df):
    i=0
    list_ = []
    while i < len(df):
        try:
            list_.append(round((float(df['收盤價'][i])-float(df['收盤價'][i-1]))/(float(df['收盤價'][i-1])+0.00001)*100,2))
        except Exception as e:
            list_.append(0)
            if i >0 :                
                print(e)
        i+=1
    df['漲跌'] = list_

#均線值是昨日的均線值
def 增加技術指標RSI(df):
    i=0
    list_5=[]
    while i<len(df):        
        try:
            temp5=df["漲跌"][i-5:i]
            list_5.append(len(temp5[temp5>0])/(len(temp5[temp5<=0])+len(temp5[temp5>0]))*100)            
        except Exception as e:
            print(e ,"zero", i)
            list_5.append(10)
        i+=1
    df['RSI5']=list_5

def power_Slope(df , feature , label):
    list_ = []
    i = 0
    while i<len(df):
      
        try:
            if df[label][i-1] == 0 :
                list_.append(0)
                i += 1
                continue
                
            K = (df[label][i]-df[label][i-1])/(df[label][i-1])*10
            if K < 0 :
                list_.append(-round(K**2 , 4))
            else : 
                list_.append( round(K**2 , 4))
        except Exception as e:
            list_.append(0)
            if i >0:
                print(e)                
        i+=1
    df[feature] = list_

def Slope(df , feature , label):
    list_ = []
    i = 0
    while i<len(df):
        try:
            K = (df[label][i]-df[label][i-1])/(df[label][i-1]+0.001)*100
            list_.append(round(K , 4))
        except Exception as e:
            list_.append(0)
            if i >0:
                print(e)                
        i+=1
    df[feature] = list_

def RSI鈍化(df):
    i = 0 
    list_=[]
    while i<len(df):
        try:
            if(df['RSI5'][i]>75):
                if df['收盤價'][i] > df['MA5'][i] :
                    list_.append(1)
                else:
                    list_.append(0)
            elif(df['RSI5'][i]<20):
                if df['收盤價'][i] < df['MA5'][i] :
                    list_.append(-1)
                else:
                    list_.append(0) 
            else:
                list_.append(0)

        except Exception as e:
            print(e)
            list_.append (0)
        i+=1
    df['RSI5鈍化'] = list_

def intercept(df , feature , label1 , label2):
    list_ = []
    i = 0
    while i<len(df):
      
        try:
            K = df[label1][i]*df[label2][i]
            list_.append(K)
        except Exception as e:
            print(e)
            list_.append(0)
            
        i+=1
    df[feature] = list_

def 紅棒(df , feature , feature2):
    list_longbar = []
    list_antenna = []
    i = 0
    while i<len(df):
        try:
            if (df['漲跌'][i] > 2):
                K  = (df['最高價'][i]-df['開盤價'][i]) / df['開盤價'][i] * 100
                if K > (df['漲跌'][i]*2) :
                    list_antenna.append(1)
                    list_longbar.append(0)
                else :
                    list_antenna.append(0)
                    list_longbar.append(1)
            else :
                list_antenna.append(0)
                list_longbar.append(0)
        except Exception as e:
            print(e)
            list_antenna.append(0)
            list_longbar.append(0)
        i+=1
    df[feature] = list_longbar
    df[feature2] = list_antenna


def 黑棒(df , feature , feature2):
    list_longbar = []
    list_antenna = []
    i = 0
    while i<len(df):
        try:
            if (df['漲跌'][i] < -2):
                K  = (df['最低價'][i]-df['開盤價'][i]) / df['開盤價'][i] * 100
                if K < (df['漲跌'][i]*2) :
                    list_antenna.append(1)
                    list_longbar.append(0)
                else :
                    list_antenna.append(0)
                    list_longbar.append(1)
            else :
                list_antenna.append(0)
                list_longbar.append(0)
        except Exception as e:
            print(e)
            list_antenna.append(0)
            list_longbar.append(0)
        i+=1
    df[feature] = list_longbar
    df[feature2] = list_antenna

def 避雷針(df , feature , feature2):
    list_U = []
    list_D = []
    i = 0
    while i<len(df['date']):
        try:
            K  = (df['最高價'][i]-df['開盤價'][i]) / df['開盤價'][i] * 100
            D  = (df['最低價'][i]-df['開盤價'][i]) / df['開盤價'][i] * 100
            if (K > df['漲跌'][i]*3) and (K > 3):
                list_U.append(1)
            else :
                list_U.append(0)    
                
            if ( D < df['漲跌'][i]*3) and (D < -3) : 
                list_D.append(1)
            else :
                list_D.append(0)
        except Exception as e:
            print(e)
            list_U.append(0)
            list_D.append(0)
        i+=1
    df[feature] = list_U
    df[feature2] = list_D

def 連續(df , feature ):
    list_U = []
    i = 0
    K = 0
    while i<len(df['date']):
        try:
            if ((df['實紅棒'][i] ==1) or (df['紅棒天線'][i] ==1) ):
                if K < 0 :
                    K = 0
                else : 
                    K += 1
                list_U.append(K)
                
            elif ((df['實黑棒'][i] ==1) or (df['黑棒天線'][i] ==1) ):
                if K > 0 :
                    K = 0
                else :
                    K -= 1
                list_U.append(K)
            else :
                if list_U[-1] == K:
                    list_U.append(K)                  
                else:
                    K = 0
                    list_U.append(K)
                
        except Exception as e:
            print(e)
            list_U.append(0)
        i+=1
    df[feature] = list_U

def distance(df , feature ,label1 , label2):
    list_ = []
    i = 0
    while i<len(df):
        
        try:
            K = round((df[label1][i] - df[label2][i])/(df[label1][i]+0.001),2)
            list_.append(K)
        except Exception as e:
            print(e)
            list_.append(0)
        i+=1
    df[feature] = list_

def Updown_state(df , feature ,label1 , label2):
    list_ = []
    i = 0
    while i<len(df):
        
        try:
            if df[label1][i] > (df[label2][i] * 1.01):
                list_.append(1)
            elif df[label1][i] < (df[label2][i] * 0.95):
                list_.append(-1)
            else:
                list_.append(0)
        except Exception as e:
            print(e)
            list_.append(0)
        i+=1
    df[feature] = list_

def 均線糾結(df):
    i = 0 
    list_=[]
    list_2 = [] 
    while i<len(df):
        try:
            MA5 = df['MA5'][i]
            MA10 = df['MA10'][i]
            MA20 = df['MA20'][i]
            MA60 = df['MA60'][i]
            d = min(MA5,MA10,MA20) / max(MA5,MA10,MA20) 
            d2 = min(MA5,MA10,MA20,MA60) / max(MA5,MA10,MA20,MA60) 
            if(d >0.96) :
                list_.append(1)
            else:
                list_.append(0)
            if(d2 >0.95) :
                list_2.append(1)
            else:
                list_2.append(0)
                
        except Exception as e:
            if (max(MA5,MA10,MA20,MA60) !=0) :
                print(e)
            list_.append (0)
        i+=1
    df['均線糾結1'] = list_
    df['均線糾結2'] = list_2

def 三陽開泰 (df):
    i = 0
    list_ = []
    while i<len(df):
        try:
            if df['連漲跌'][i] > 6:
                i+=1
                list_.append(0)
                continue
            
            P = max(df.MA5[i],df.MA10[i],df.MA20[i])
            if ((df['收盤價'][i] > P) & (df['收盤價'][i] > df['開盤價'][i]) ):
                if (max(list_[-10:])!= 1):
                    list_.append(1)
                else:
                    list_.append(0)
            else :
                list_.append(0)
        except Exception as e:
            print(e , i)
            list_.append(0)
        i+=1
    df['三陽開泰'] = list_

def 突破前高(df):
    i = 0
    list_ = []
    while i<len(df):
        try:
            if((df['年前高'][i]!=0) & (df['收盤價'][i] > df['年前高'][i])):
                list_.append(1)
            else :
                list_.append(0)
        except Exception as e:
            print(e , i)
            list_.append(0)
            
        i+=1
    df['突破前高'] = list_

def 突破整理(df):
    i = 0
    list_ = []
    while i<len(df):
        try:
            if((max(df['均線糾結1'][i-10:i])==1) & (df['收盤價'][i] > df['季前高'][i])) :
                if (max(list_[-10:]) != 1):
                    list_.append(1)
                else :
                    list_.append(0)
            else :
                list_.append(0)
        except Exception as e:
            print(e , i)
            list_.append(0)
            
        i+=1
    df['突破前高'] = list_

def Ratio(df , feature , label1 , label2):
    list_ = []
    i = 0
    while i<len(df):
      
        try:
            K = df[label1][i] / (df[label2][i]+0.001)
            list_.append(K)
        except Exception as e:
            print(e)
            list_.append(0)
            
        i+=1
    df[feature] = list_

def day_Volatility (df , feature) :
    list_ = []
    i = 0
    while i<len(df):
      
        try:
            K = round(((df['最高價'][i]- df['最低價'][i])*100/(df['最低價'][i]+0.001))**2 , 4 )
            list_.append(K)
        except Exception as e:
            print(e)
            list_.append(0)
        i+=1
    df[feature] = list_
    
def Implied_Volatility (df , feature , day) :   
    list_ = []
    i = 0
    while i<len(df):
        if i < day :
            list_.append(0)
            i+=1
            continue
        try:
            K = round(sum(df['日振幅'][i-day:i+1])/day , 2)
            list_.append(K)
        except Exception as e:
            print(e)
            list_.append(0)
        i+=1
    df['波動率'] = list_

def 季均漲跌天數(df , day) :
    list_rise = []
    list_fall = []
    i = 0
    while i<len(df):
        if i < day :
            list_rise.append(0)
            list_fall.append(0)
            i+=1
            continue
        try:
            interval_day = df['連漲跌'][i-day:i+1]
            
            P = interval_day[interval_day > 0]
            D = interval_day[interval_day < 0]
            if len(P) == 0 :
                list_rise.append(0)
            else :
                list_rise.append(round(sum(P)/len(P)))
            if len(D) == 0 :
                list_fall.append(0)
            else :
                list_fall.append(round(sum(D)/len(D)))
        except Exception as e:
            print(e)
            list_rise.append(0)
            list_fall.append(0)
        i+=1
    df['均漲天數'] = list_rise
    df['均跌天數'] = list_fall

def 超漲跌(df) :
    list_ = []
    i = 0
    while i<len(df):        
        try:
            if df['連漲跌'][i] > df['均漲天數'][i] :
                list_.append(1)
            elif df['連漲跌'][i] < df['均跌天數'][i] :
                list_.append(-1)
            else :
                list_.append(0)
        except Exception as e:
            print(e)
            list_.append(0)
        i+=1
    df['超漲跌'] = list_

