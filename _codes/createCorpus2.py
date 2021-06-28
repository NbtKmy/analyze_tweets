import pandas as pd
import re
import MeCab


def getCorpus(csv_data):
    df = pd.read_csv(csv_data, lineterminator='\n')
    txt_list = list(df['text'])

    corpus = []
    for txt in txt_list:
        if type(txt) == float: # NaN soll nicht reinkommen
            continue
        else:
            txt = re.sub(r'\s','', txt)
            # Fullwidth-Space werden gelöscht
            txt = re.sub(r'　','', txt)
            tg = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd') 
            new_txt = tg.parseToNode(txt)
            
            while new_txt:
                arr = new_txt.feature.split(",")
                if arr[0] == '名詞':
                    if arr[6] == '*':
                        corpus.append(new_txt.surface)
                    else:
                        corpus.append(arr[6])
                elif arr[0] == '動詞':
                    if arr[6] == '*':
                        corpus.append(new_txt.surface)
                    else:
                        corpus.append(arr[6])
                elif arr[0] == '形容詞':
                    if arr[6] == '*':
                        corpus.append(new_txt.surface)
                    else:
                        corpus.append(arr[6])
                
                new_txt = new_txt.next

    corp = ' '.join(corpus)
    
    with open('./corpus.txt', mode='w') as f:
                f.write(corp)



if __name__ == "__main__":
    path_to_data = './tweetsdata/'
    data_name = 'tweetsdata_202101.csv'
    data = path_to_data + data_name
    getCorpus(data)
    