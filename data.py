import pandas as pd

data = pd.read_csv('csv/data.csv')

data = data.drop(['page'], axis=1)
data['date'] = pd.to_datetime(data['date'], dayfirst=True)
data = data.sort_values(by='date', ascending=False)
data.to_csv('csv/result.csv', index=False)