import pandas as pd
import json
stateNames = {
    "NSW": "New South Wales",
    "Vic.":"Victoria",
    "Qld.":"Queensland",
    "WA": "Western Australia",
    "Tas.": "Tasmania",
    "NT": "Northern Territory",
    "SA":"South Australia"

}

# Load the data
df = pd.read_excel("median_house_prices.xlsx", sheet_name="Data1")

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
yearly_avg['UniqueKey'] = [x for x in range(len(yearly_avg["Year"]))]
print(yearly_avg.head())

yearly_avg.to_csv("MedianHousePricesByState.csv",index=False)
