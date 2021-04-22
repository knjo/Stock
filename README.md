# Stock

--- 
- The record for my stock prediction program
- Aim to evaluate if the stock will rise or drop within the setting
- Focus on high precision with acceptiable recall rate
---
# Main Package ( with some branchs for testing ):
## Date :
- Update everyday's Stock info
- Change while to for loop can get the whole data by the set time interval

## Process :
- Creating feature for model prediction, include Technical Analysis and institutional index
- Update or build all

## Predict : (chaos now, will be rewritten when finding good performance)
- Building the model for stock prediction

notation : 
Normal Deeplearning and lstm do not perform well.

---
# Issue & Todo

## Issue:
# Unrobustness of precision :  highly related to market ( market is good, then rise precision is high (up to 70%), vice versa.
- precision of rise and fall prediction is crossed -> should create new feature that contain market info
- Some created features is sparse -> hard to be used in tree base models
# Hard to follow the setted buy and sell
- Find the dealer providing API for program -> Build the program for automatic trading 
  
## Todo
# feature engineering
- Making new features that cross market index
- Adding feature about clustering info
- Processing the categorical data by TF-IDF or Bert
- Feature extraction
# Model testing
- LBGM
- Sparse Dictionary classifier 
- By the feature form bert : try 2DCNN
- RL for finding trading strategies
