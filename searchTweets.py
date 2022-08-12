import requests
import os
import re
from datetime import timezone, timedelta
import datetime
import time
import mojimoji
import pandas as pd

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get('BEARER_TOKEN')

search_url = 'https://api.twitter.com/2/tweets/search/all'


def create_query(nextToken):

    # Zeitangabe in JST
    jst_st = datetime.datetime(2021, 4, 1, 0, 0, 0, 0, datetime.timezone(timedelta(hours=+9)))
    jst_et = datetime.datetime(2021, 5, 1, 0, 0, 0, 0, datetime.timezone(timedelta(hours=+9)))
    # Zeitangabe nach UTC umschreiben
    utc_st = jst_st.astimezone(timezone.utc)
    utc_st = utc_st.isoformat()
    utc_et = jst_et.astimezone(timezone.utc)
    utc_et =utc_et.isoformat()
    

    if not nextToken:
        # Optionale params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        query_params = {'query': '(オリンピック lang:ja -is:retweet) OR (五輪 lang:ja -is:retweet)',
                    'tweet.fields': 'created_at,id,text,public_metrics',
                    'start_time': utc_st,
                    'end_time': utc_et,
                    'max_results': 500}
    else:
        query_params = {'query': '(オリンピック lang:ja -is:retweet) OR (五輪 lang:ja -is:retweet)',
                    'tweet.fields': 'created_at,id,text,public_metrics',
                    'start_time': utc_st,
                    'end_time': utc_et,
                    'max_results': 500,
                    'next_token': nextToken}
    
    return query_params


def create_headers(bearer_token):
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):

    # für 3 sec warten wegen rate limit "App rate limit: 1 request per second"
    time.sleep(3)
    
    response = requests.request('GET', url, headers=headers, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def throw_q(nextToken):
    headers = create_headers(bearer_token)
    query_params = create_query(nextToken)
    json_response = connect_to_endpoint(search_url, headers, query_params)

    if json_response['meta'].get('next_token') is None:
        nextToken = False
    else:
        nextToken = json_response['meta']['next_token']

    tw_daten = json_response['data']
    tw_list = []
    for i in tw_daten:
        # id als Str 
        ident = str(i['id'])
        # user-id, url, hash-tag, Zeilenumbruch und Spatien aus dem Tweets entfernen
        tw_text = re.sub(r'@\w+','', i['text'])
        tw_text = re.sub(r'https://t\.co/[0-9a-zA-Z]+','', tw_text)
        tw_text = re.sub(r'(http|https)://[0-9a-zA-Z\./]+','', tw_text)
        tw_text = re.sub(r'#.+?(\s|$)', '', tw_text)
        tw_text = re.sub(r'\n','', tw_text)
        # tw_text = re.sub(r'\s','', tw_text)
        # Kana soll immer in Fullwidth-Zeichen dargestellt werden
        tw_text = mojimoji.han_to_zen(tw_text, kana=True, digit=False, ascii=False)
        # Digit und Ascii sollen immer in Halfwidth-Zeichen dargestellt werden
        tw_text = mojimoji.zen_to_han(tw_text, kana=False, digit=True, ascii=True)

        # Wenn die Text-Länge kurzer als 3 Zeichen ist, soll das Tweet ignoriert werden
        if len(tw_text) < 3:
            continue

        # Zahl von retweet und like
        retw = i['public_metrics']['retweet_count']
        like_count = i['public_metrics']['like_count']

        tw_list.append([ident, i['created_at'], tw_text, retw, like_count])

    
    return nextToken, tw_list


if __name__ == "__main__":
    start_time = time.time()
    nextToken = ''
    tweets = []
    nt, l = throw_q(nextToken)
    nextToken = nt
    tweets += l

    itr_num = 1
    while nextToken:
        t1 = time.time()
        if itr_num == 1:
            t0 = t1

        # Wenn das ganze Verfahren länger als 2 Stunde dauert, soll das aktuelle nextToken gespeichert werden. while-loop wird auch unterbrochen 
        ft = t1 - start_time
        if ft >= 7200:
            dt_now = datetime.datetime.now()
            dt_now = dt_now.isoformat()
            s = 'Verfahren unterbrochen: ' + dt_now + ' Das aktuelle nextToken: ' + nextToken
            with open('./nextToken.txt', mode='w') as f:
                f.write(s)
            break

        # Query werfen und tweets & nextToken erhalten
        nt, l = throw_q(nextToken)
        nextToken = nt
        tweets += l
        itr_num += 1
        
        # wegen rate limit Pause einlegen "App rate limit: 300 requests per 15-minute window"
        if itr_num == 299:
            t2 = time.time()
            t = 1200 - (t2 - t0)
            if t > 0:
                print('sleep ' + str(t) + ' sec. wegen rate limit')
                time.sleep(t)
            itr_num = 1
        
    
    tweetsDf = pd.DataFrame(tweets, columns=['id', 'time', 'text', 'retweets', 'likes'])
    tweetsDf.to_csv('tweetsdata.csv', encoding='utf_8')


