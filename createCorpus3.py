import pandas as pd
import re
import MeCab
import pickle


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

            txt_list = txt.split('。')
            for sentence in txt_list:
                word_list = []
                tg = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd') 
                new_txt = tg.parseToNode(sentence)
            
                while new_txt:
                    arr = new_txt.feature.split(",")
                    if arr[0] == '名詞':
                        if arr[6] == '*':
                            word_list.append(new_txt.surface)
                        else:
                            word_list.append(arr[6])
                    elif arr[0] == '動詞':
                        if arr[6] == '*':
                            word_list.append(new_txt.surface)
                        else:
                            word_list.append(arr[6])
                    elif arr[0] == '形容詞':
                        if arr[6] == '*':
                            word_list.append(new_txt.surface)
                        else:
                            word_list.append(arr[6])
                
                    new_txt = new_txt.next
                
                #print (word_list)
                # stopwords eliminieren
                stopwords = ['やる', 'ん', 'なる', 'する', 'それ', 'こと', 'ある', 'てる', 'なん', 'の', 'もん', 'そう', 'これ', 'そこ', 'いる', 'れる', 'よう', '気', 'ため', 'ない', 'つもり', 'ちゃう', 'しまう', 'つもり', '感じ', 'ほしい', 'いう', ' 言う', 'みたい', '思う', '事', '何', '方', '中']
                for stw in stopwords:
                    word_list = [w for w in word_list if w != stw]

                #print (word_list)
                unify_exp = [['よい', '良い'], ['いい', '良い'], ['出来る', 'できる']]
                for uex in unify_exp:
                    word_list = [uex[1] if uex[0] == x else x for x in word_list]
                # print (word_list)

                if len(word_list) != 0:
                    corpus.append(word_list)
            
    with open('corpus_202103.pickle', mode='wb') as f:
        pickle.dump(corpus, f)



if __name__ == "__main__":
    path_to_data = './tweetsdata/'
    data_name = 'tweetsdata_202103.csv'
    data = path_to_data + data_name
    getCorpus(data)
    