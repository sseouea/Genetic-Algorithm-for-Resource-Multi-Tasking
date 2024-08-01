import pandas as pd
import chardet

path = '.\logs\givenData (ep30, num3)\\0-20240611214205\Best_model.csv'
#path = './jobshop/schedule_LPT_1_chefs.csv'

with open(path, 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']
df = pd.read_csv(path, encoding=encoding)

#df = pd.read_csv(path)

cols = ['sub', 'title', 'index', 'duration', 'parallel','pre-dependency','nxt-dependency','real start','real finish','start','finish']

for col in cols:
    print(col, type(col))