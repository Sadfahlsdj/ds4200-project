import pandas as pd
from sankey_functions import create_sankey


def shorten_type(weight_type):
    if 'Normal' in weight_type:
        return 'Normal_Weight'
    if 'Overweight' in weight_type:
        return 'Overweight'
    if 'Obesity' in weight_type:
        return 'Obesity'
    else:
        return 'Insufficient_Weight'


df = pd.read_csv('ObesityDataSet_raw_and_data_sinthetic.csv')
df['Short_Weight_Type'] = df['NObeyesdad'].apply(shorten_type)
df = df.drop(['NObeyesdad'], axis=1)
df['count'] = [1] * len(df['Age']) # 1 for each row - needed for sankey
print(df.head().to_string())

fig = create_sankey(df, 'Short_Weight_Type', 'MTRANS', 'count', ['CAEC'],
              width=1200, height=800)

fig.write_html('sankey.html')