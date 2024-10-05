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

df = pd.read_excel('housing_approvals.xlsx',sheet_name='Sheet1')
df = pd.melt(df,id_vars=['Date'],var_name='State',value_name='Housing Approvals')
df['Year'] = df["Date"].dt.year
df = df.groupby(['Year','State'])['Housing Approvals'].mean().round().reset_index()
df['YoY Growth (%)'] = df.groupby('State')['Housing Approvals'].pct_change() * 100
df.to_csv("HousingApprovalsByState.csv",index=False)

df = pd.read_csv('popData.csv')
df['YoY Growth (%)'] = df.groupby('State')['Population'].pct_change() * 100
df.to_csv("popData.csv",index=False)
