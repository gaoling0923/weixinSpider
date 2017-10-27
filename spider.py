
import urllib

import requests

base_url ='http://weixin.sogou.com/weixin?'
keyword='风景';
headers={
'Cookie':'SUID=03E1EB7C3108990A00000000599D2786; SUV=1503471492766249; ABTEST=8|1503471495|v1; SNUID=F113198EF2F4A597CE830CAAF2CCFA03; weixinIndexVisited=1; sct=3; IPLOC=CN1100; JSESSIONID=aaarWs9LFZQ9EeCf7Oi4v; ppinf=5|1503496975|1504706575|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMzpvaCUyME15JTIwZ29kfGNydDoxMDoxNTAzNDk2OTc1fHJlZm5pY2s6MTM6b2glMjBNeSUyMGdvZHx1c2VyaWQ6NDQ6bzl0Mmx1UGZkM2NvV2JtWWZ3a0Q1RUh6dlNGUUB3ZWl4aW4uc29odS5jb218; pprdig=VRlwi-dqXrbtFsoTRTKkgO9ccHO1g4ouC6m7Lu4drW5IsV6A0fyZM8e-MguLpr1v4H8du-YM5NwChgTRX-FguBj7GXuIZKcEO_rlLKdRC-7hYCs2W-rEw2Ffv971dUR_aC54ydH4008CTJHW7f2jlhZabDsG8jgQPXSnj9AysMs; sgid=09-30248001-AVmdiaw8YicflZ0BnhkFGbgSE; ppmdig=15034969750000009a8514683ef723945f53457e9581fb62',
'Host':'weixin.sogou.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

PROXY_POOL_URL = 'http://localhost:5000/get'
proxy=None;
max_count=5;
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url,count=1):
    print('url',url)

    global proxy ,max_count

    if count>max_count:
        print('tried failed')
        return None
    try:
        if proxy:
            proxies={
                'http':'http://'+proxy
            }
            response = requests.get(url, allow_redirects=False,headers=headers,proxies=proxies);
        else:
            #allow_redirects=False 不允许自动跳转
            response=requests.get(url,allow_redirects=False,headers=headers);
            if response.status_code==200:
                return response.text;
            if response.status_code==302:
                # need proxy
                print('302')
                proxy=get_proxy();
                if proxy:
                    print('using proxy',proxy)
                    #max_count += 1
                    return get_html(url);
                else:
                    print('using proxy failed')
                    return None


    except ConnectionError as e :
#    except ConnectionError :
        print('faile',e.args)
        proxy=get_proxy();
        max_count +=1
        return get_html(url,count);


def get_index(keyword,page):
    data ={
        'query':keyword,
        'type':2,
        'page':page
    }
    queries=urllib.parse.urlencode(data);
    url=base_url+queries;
    html=get_html(url);
    return html
def main():
    count=0;
    for page in range(1,101):
        count=count+1
        html=get_index(keyword,page);
        # print(html)
        print(count)

if __name__=='__main__':
    get_index('一汽奔腾',101)
    # main();
