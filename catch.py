import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os
import copy



class Catch:
    def __init__(self,config_file):
        self.config_file=config_file
        self.sources_data=config_file.Sources.tophub
        self.url='https://tophub.today'
        self.html = self.get_html(self.url)
        self.data = self.get_data(self.html)
        self.now=time.strftime('%Y-%m-%d %H-%M',time.localtime(time.time()))
        self.last_data=pd.DataFrame()
        self.res=pd.DataFrame()

    def get_html(self, url):
        """获取网页HTML内容"""
        headers={
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; \
             Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"

        }
        resp=requests.get(url,headers=headers)
        return resp.text

    def get_data(self, html):
        """从HTML中提取数据节点"""
        soup=BeautifulSoup(html,'html.parser')
        nodes=soup.find_all('div',class_='cc-cd')
        return nodes

    def get_node_data(self, df, nodes,sources_data,now):
        """处理节点数据并保存到CSV文件"""
        if not os.path.exists(f"data/{now}"):
            os.makedirs(f"data/{now}")
        for node in nodes:
            datas=[]
            #df清空所有行
            df=df.drop(df.index)
            source = node.find('div', class_='cc-cd-lb').text.strip()
            messages = node.find('div', class_='cc-cd-cb-l nano-content')
            if source not in sources_data: 
                continue
            else:
                #移除sources_data中source，避免微博重复问题
                sources_data.remove(source)
                print(f"移除{source}数据")
            if messages:
                messages=messages.find_all('a')
            else:
                continue
            
            for message in messages:
                content = message.find('span', class_='t').text.strip() 
                
                data = {
                        'content': [content],
                        'url': [message['href']],
                        'source': [source],
                        'catch_time': [now],

                    }
                datas.append(data)
            df=pd.DataFrame(datas)
            
            print(df)
            #保存数据
            df.to_csv(f"data/{now}/{source}.csv", index=True)
        return df
    
    def save_data(self):
        """保存数据的主方法"""
        # 使用深拷贝避免修改原始数据
        remove_sources_data = copy.deepcopy(self.sources_data)
        self.res = self.get_node_data(self.res, self.data, remove_sources_data, self.now)
    def merge_data(self):
        """合并数据"""
        for source in self.sources_data:
            # 读取CSV时忽略第一列作为索引，避免读取到行标
            df = pd.read_csv(f"data/{self.now}/{source}.csv", index_col=0)
            self.last_data = pd.concat([self.last_data, df], ignore_index=True)
        # 保存时不包含行标
        self.last_data.to_csv(f"data/{self.now}/last.csv", index=False)
    def get_last_data(self):
        """处理数据"""
        #读取last_data的content列
        content_list=self.last_data['content'].tolist()
        #使用正则表达式提取content中的链接
        url_list=self.last_data["url"].tolist()
        source_list=self.last_data["source"].tolist()
        catch_time_list=self.last_data["catch_time"].tolist()
        return content_list,url_list,source_list,catch_time_list
        
        




