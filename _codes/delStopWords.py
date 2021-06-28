import re

def delStopWords():
    with open('./corpus/corpus_202101.txt') as f:
        tex = f.read()
        stopwords = ['やる', 'ん', 'なる', 'する', 'それ', 'こと', 'ある', 'てる', 'なん', 'の', 'もん', 'そう', 'これ', 'そこ', 'いる', 'れる', 'よう', '気', 'ため', 'ない', 'つもり', 'ちゃう', 'しまう', 'つもり', '感じ', 'ほしい', 'いう', ' 言う', 'みたい', '思う', '事', '何', '方', '中']

        unify_exp = [['よい', '良い'], ['いい', '良い'], ['出来る', 'できる']]

        for s in stopwords:
            tex = re.sub(r'\s%s\s' % s,' ', tex)
        
        for t in unify_exp:
            tex = re.sub(r'\s%s\s' % t[0], t[1], tex)
        
        with open('corpus_202101.txt', mode='w') as f:
            f.write(tex)

if __name__ == "__main__":
    delStopWords()

