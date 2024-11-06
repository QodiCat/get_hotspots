import os
from openai import OpenAI


#
file_dir="data"
#查找列出文件夹下所有文件，获取最新的文件
def list_dir(file_dir):
    list = os.listdir(file_dir)
    list.sort(key=lambda fn: os.path.getmtime(file_dir + "/" + fn))
    file_path = os.path.join(file_dir, list[-1])
    return file_path
file_path=list_dir(file_dir)
print(file_path)

#将excel文件转换为csv文件
import pandas as pd
with open(file_path, 'r') as f:
    df = pd.read_excel(f,engine='openpyxl')
    df.to_csv('data/data.csv', index=False)
    print(df)

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
completion = client.chat.completions.create(
    model="qwen-turbo", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': '你是善于洞察优秀AI热点和资讯的AI，我会给你很多的热点，你需要判断这些热点是否和AI相关，如果相关给出对应热点的前面的序号，如果没有任何热点和AI相关，请回复“没有”'},
        {'role': 'user', 'content': '你喜欢什么？'}],
    )
    
print(completion.choices[0].message.content)

