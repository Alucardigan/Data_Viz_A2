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

pivotDf = pd.melt(df,id_vars=['Date'],var_name='State',value_name='Median Housing Price')
pivotDf.to_csv("MedianHousePricesByState.csv",index=False)
print(pivotDf)
with open('AustralianMapWithBorders.json','r') as file:
    data = json.load(file)
    print(data["objects"]["ne_50m_admin_1_states_provinces"]["geometries"][0]['properties'])