import pandas as pd

csv1Path = 'result.csv'
data = pd.read_csv(csv1Path)
for index, rows in data.iterrows():
    print(len(rows['pixel']))

