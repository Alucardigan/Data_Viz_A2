#imports 
import pandas as pd
import json
from  functools import reduce 
import numpy as np 
stateNames = {
    "NSW": "New South Wales",
    "Vic.":"Victoria",
    "Qld.":"Queensland",
    "WA": "Western Australia",
    "Tas.": "Tasmania",
    "NT": "Northern Territory",
    "SA":"South Australia"

}
#housing approvals 
"""
df = pd.read_excel('housing_approvals.xlsx',sheet_name='Sheet1')
df = pd.melt(df,id_vars=['Date'],var_name='State',value_name='Housing Approvals')
df['Year'] = df["Date"].dt.year
df = df.groupby(['Year','State'])['Housing Approvals'].mean().round().reset_index()
df['Housing Approvals YoY Growth (%)'] = df.groupby('State')['Housing Approvals'].pct_change() * 100
df.to_csv("HousingApprovalsByState.csv",index=False)
#pop data
#Pop Data
popDf = pd.read_excel("ausPopData.xlsx", sheet_name="Sheet1")
pivotPopDf = pd.melt(popDf,id_vars=['Date'],var_name='State',value_name='Population')
print(pivotPopDf.head())
pivotPopDf['Year'] = pivotPopDf["Date"].dt.year
popDf = pivotPopDf.groupby(['Year','State'])['Population'].mean().reset_index()
popDf.to_csv("popData.csv",index=False)
df = pd.read_csv('popData.csv')
df['Pop YOY Growth (%)'] = df.groupby('State')['Population'].pct_change() * 100
df.to_csv("popData.csv",index=False)
pop_df = pd.read_csv("popData.csv")
housing_df = pd.read_csv("HousingApprovalsByState.csv")
combined_df = pd.merge(pop_df, housing_df, on=["Year", "State"], how="outer")
combined_df.dropna(inplace=True)
print(combined_df.head(18))

combined_df.to_csv("HousingApprovalsVSPopulation.csv",index=False)
"""
df = pd.read_excel('avgIncome.xlsx',sheet_name='Sheet1')
df = pd.melt(df,id_vars=['Date'],var_name='State',value_name='MedianIncome')
df['Date'] = pd.to_datetime(df["Date"])
df['Year'] = df["Date"].dt.year
df['MedianIncome'] = df['MedianIncome']*52
df.to_csv('avgIncome.csv',index=False)
