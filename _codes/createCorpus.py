import pandas as pd
import re
import MeCab


def getCorpus(csv_data):
    df = pd.read_csv(csv_data, lineterminator='\n')
    txt_list = list(df['text'])

    corpus = ''
    for txt in txt_list:
        if type(txt) == float: # NaN soll nicht reinkommen
            continue
        else:
            txt = re.sub(r'\s','', txt)
            # Fullwidth-Space werden gelöscht
            txt = re.sub(r'　','', txt)
            wakati = MeCab.Tagger('-F"%f[6] "  -U"%m " -E" " -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd') 
            new_txt = wakati.parse(txt)
            
            corpus += str(new_txt)
    
    with open('./corpus.txt', mode='w') as f:
                f.write(corpus)



if __name__ == "__main__":
    path_to_data = './tweetsdata/'
    data_name = 'tweetsdata_202102.csv'
    data = path_to_data + data_name
    getCorpus(data)
    