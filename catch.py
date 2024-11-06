import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os



class Catch:
    def __init__(self,config_file):
        self.config_file=config_file
        self.sources_data=config_file.Sources.tophub
        self.url='https://tophub.today'
        self.html = get_html(self.url)
        self.data = get_data(self.html)
        self.now=time.strftime('%Y-%m-%d %H时%M分',time.localtime(time.time()))
        self.file_path = f"data/{self.now}.csv"
        if os.path.exists(self.file_path):
            self.res = pd.read_csv(self.file_path)
        else:
            self.res = pd.DataFrame(columns=['content', 'url', 'source', 'catch_time'])

    def save_data(self):
        self.res = get_node_data(self.res, self.data, self.sources_data, self.now)
        self.res.to_csv(self.file_path, index=True)
        


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

def get_node_data(df, nodes,sources_data,now):
     for node in nodes:
         source = node.find('div', class_='cc-cd-lb').text.strip()
         messages = node.find('div', class_='cc-cd-cb-l nano-content').find_all('a')
         for message in messages:
            if source in sources_data:
                content = message.find('span', class_='t').text.strip() 
                
                data = {
                        'content': [content],
                        'url': [message['href']],
                        'source': [source],
                        'catch_time': [now],
   
                    }
    
                item = pd.DataFrame(data)
                df = pd.concat([df, item], ignore_index=True)
    
    
     return df




