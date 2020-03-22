import pandas as pd
FILE_LOCATION = 'C:/Users/sefx5/Downloads/CAPI_test.csv'
df = pd.read_csv(FILE_LOCATION,encoding='utf-8',dtype = {'layer_2' : str})
df['question_logic'] = df['question_logic'].fillna('')
df['question'] = df['layer_1'].astype(str) + df['layer_2'] + df['layer_3'].fillna('')
df.drop(df[df['question_logic'] == ''].index,axis = 0,inplace=True)

condition = {}

for num,logic in zip(df['question'],df['question_logic']):
    condition[num] = logic

TOTAL_PAGE_QUESTION = df['page'].iloc[-1]

hello 
