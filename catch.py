import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os

def get_html(url):
    headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; \
         Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"

    }
    resp=requests.get(url,headers=headers)
    return resp.text


def get_data(html):
    soup=BeautifulSoup(html,'html.parser')
    nodes=soup.find_all('div',class_='cc-cd')
    return nodes

def get_node_data(df, nodes):
     now = int(time.time())
     for node in nodes:
         source = node.find('div', class_='cc-cd-lb').text.strip()
         messages = node.find('div', class_='cc-cd-cb-l nano-content').find_all('a')
         for message in messages:
            if source == '微信':
                content = message.find('span', class_='t').text.strip()

                
                if df.empty or df[df.content == content].empty:
                    data = {
                        'content': [content],
                        'url': [message['href']],
                        'source': [source],
                        'start_time': [now],
                        'end_time': [now]
                    }
    
                    item = pd.DataFrame(data)
                    df = pd.concat([df, item], ignore_index=True)
    
                else:
                    index = df[df.content == content].index[0]
                    df.at[index, 'end_time'] = now
    
     return df

url='https://tophub.today'
html = get_html(url)
data = get_data(html)
# 检查文件是否存在
file_path = 'hot.xlsx'
if os.path.exists(file_path):
    res = pd.read_excel(file_path, engine='openpyxl')
else:
    res = pd.DataFrame(columns=['content', 'url', 'source', 'start_time', 'end_time'])

res = get_node_data(res, data)
res.to_excel(file_path, engine='openpyxl', index=False)



