import pandas as pd

def forLogstash(csv_data):
    df = pd.read_csv(csv_data, lineterminator='\n')
    new_df = df.drop(df.columns[[0]], axis=1)
    new_df.to_csv('tweetsdata.csv', index = False, float_format='%.0f')

if __name__ == "__main__":
    path_to_data = './tweetsdata/'
    data_name = 'tweetsdata_202103.csv'
    data = path_to_data + data_name
    forLogstash(data)
    