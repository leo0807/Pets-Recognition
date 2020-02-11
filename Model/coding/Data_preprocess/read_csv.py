import glob

import pandas as pd

csv1Path = 'prep_images_rotated.csv'
csv2Path = 'result.csv'

inputfile = "*.csv"
outputfile = "dog_training.csv"
csv_list = glob.glob(inputfile)

filepath = csv_list[0]
df = pd.read_csv(filepath)
df = df.to_csv(outputfile, index=False)

for i in range(1, len(csv_list)):
    filepath = csv_list[i]
    df = pd.read_csv(filepath)
    df = df.to_csv(outputfile, index=False, header=False, mode='a+')
