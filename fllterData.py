import pandas as pd
import numpy as np

# declare variable
file_path = "C:\\Users\\Dharmaraj\\Favorites\\Downloads\\SaleData.xlsx"
sheet_name = 'SaleData'



#read the file
df = pd.read_excel(file_path, sheet_name=sheet_name)
orgionaldata = pd.read_excel(file_path, sheet_name=sheet_name)

#Agaiin delcare varibale
new_column_name = 'High Sales'
new_column_value = 'Low Stock'
# condition1 = df = df[df['Units'] < 50]
filter_column='Units'

# df['High Sale'] = 'Below Avg'

# Multiple conditions and corresponding values
conditions = [
    (df['Units'] >= 0) & (df['Units'] <= 50),
    (df['Units'] >= 51) & (df['Units'] <=100),
    (df['Units'] > 100)
]
choices = ['LOW', 'MID', 'HIGH']

df['High Sales'] = np.select(conditions, choices, default='OTHER')

# df.to_excel(file_path, sheet_name=sheet_name, index=False)

df.to_excel('C:\\Users\\Dharmaraj\\Favorites\\Downloads\\output.xlsx', index=False)

# Apply the filter condition and assign the specified value

print(df)