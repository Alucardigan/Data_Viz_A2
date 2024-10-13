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
incomeDf = pd.read_excel('avgIncome.xlsx',sheet_name='Sheet1')
incomeDf= pd.melt(incomeDf,id_vars=['Date'],var_name='State',value_name='MedianIncome')
incomeDf['Date'] = pd.to_datetime(incomeDf["Date"])
incomeDf['Year'] = incomeDf["Date"].dt.year
incomeDf['MedianIncome'] = incomeDf['MedianIncome']*52
incomeDf.to_csv('avgIncome.csv',index=False)

#Median house price stuff
df = pd.read_excel("median_house_prices.xlsx", sheet_name="Data1")
print(df.head())
new_names = {}
for column in df.columns:
    if ';' in column:
        new_name = column.split(';')[-2].strip()
        if new_name.startswith("Rest"):
            new_name = stateNames[new_name.split(" ")[2]]
        new_names[column] = new_name

df.rename(columns=new_names, inplace=True)
df.rename(columns={'Unnamed: 0':"Date"},inplace=True)

numeric_df = df.select_dtypes(include=[float])

numeric_df_interpolated = numeric_df.interpolate(method='linear', axis=1)

df = pd.concat([df['Date'], numeric_df_interpolated], axis=1)

pivotDf = pd.melt(df,id_vars=['Date'],var_name='State',value_name='MedianHousingPrice')
pivotDf['Date'] = pd.to_datetime(pivotDf["Date"])
pivotDf['Year'] = pivotDf["Date"].dt.year
yearly_avg = pivotDf.groupby(['Year','State'])['MedianHousingPrice'].mean().reset_index()
print(yearly_avg.head())
yearly_avg.to_csv("MedianHousePricesByState.csv",index=False)

mergedDf = yearly_avg.merge(incomeDf,on=['State','Year'],how='inner')
mergedDf['HousingAffordability'] = (mergedDf['MedianHousingPrice']*1000)/mergedDf['MedianIncome']


mergedDf.to_csv("housingAffordability.csv",index=False)