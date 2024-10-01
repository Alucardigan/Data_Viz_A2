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
yearly_avg.to_csv("MedianHousePricesByState.csv",index=False)

#Pop Data
popDf = pd.read_excel("ausPopData.xlsx", sheet_name="Sheet1")
pivotPopDf = pd.melt(popDf,id_vars=['Date'],var_name='State',value_name='Population')
print(pivotPopDf.head())
pivotPopDf['Year'] = pivotPopDf["Date"].dt.year
popDf = pivotPopDf.groupby(['Year','State'])['Population'].mean().reset_index()
popDf.to_csv("popData.csv",index=False)

mergedDf = yearly_avg.merge(popDf[['State','Population']],on='State')
mergedDf['HousingPricePerCapita'] = (mergedDf['MedianHousingPrice']*1000)/mergedDf['Population']

print(mergedDf.head())
mergedDf.to_csv("finalData.csv",index=False)

#Index data modification
hpi = pd.read_excel("index_data.xlsx",sheet_name="HPI")
hpi['Year'] = hpi["Date"].dt.year
hpi = hpi.groupby(["Year"])['HPI'].mean().reset_index()
wpi = pd.read_excel("index_data.xlsx",sheet_name="WPI")
wpi['Year'] = wpi["Date"].dt.year
wpi = wpi.groupby(["Year"])['WPI'].mean().reset_index()
cpi = pd.read_excel("index_data.xlsx",sheet_name="CPI")
cpi['Year'] = cpi["Date"].dt.year
cpi = cpi.groupby(["Year"])['CPI'].mean().reset_index()


print(hpi.head())
print(wpi.head())
print(cpi.head())

data_frames = [hpi,wpi,cpi]
mergedDf = reduce(lambda  left,right: pd.merge(left,right,on=['Year'],how='outer'), data_frames)
mergedDf['HPI'] = mergedDf['HPI'].interpolate(method='linear')
print(mergedDf.tail())
mergedDf = pd.melt(mergedDf,id_vars="Year",value_vars=['HPI','WPI','CPI'],var_name="Index")
print(mergedDf.head())
mergedDf.to_csv("IndexData.csv",index=False)

#age vs tenure stuff 
df1 = pd.read_excel("ownershipOverTime.xlsx")
print(df1.head())
numeric_df = df1.select_dtypes(include=[float])

numeric_df_interpolated = numeric_df.interpolate(method='linear', axis=1)
df1 = pd.concat([df1['Tenure type'], numeric_df_interpolated], axis=1)
meltDf = pd.melt(df1,id_vars="Tenure type",var_name="Year",value_name="%")
meltDf.to_csv("TenureOverTime.csv",index=False)

#income used on household_costs
df = pd.read_excel('incomeUsedByHousehold.xlsx')
df.drop([4],inplace=True)

numeric_df = df.select_dtypes(include=[float])

numeric_df_interpolated = numeric_df.interpolate(method='linear', axis=1)
df = pd.concat([df['Date'], numeric_df_interpolated], axis=1)
meltDf = pd.melt(df,id_vars="Date",var_name="Year",value_name="%")
meltDf.to_csv("incomeUsedByHousehold.csv",index=False)
