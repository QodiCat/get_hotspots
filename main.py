from utils.utils import read_yaml
from catch import Catch
from agent.ac_relation_agent import AcRelationContent
from utils.read_csv import read_csv_columns,read_csv
import re
# config_file=read_yaml('config.yaml')
# catch=Catch(config_file)
# catch.save_data()
# catch.merge_data()

# content_list,url_list,source_list,catch_time_list=catch.get_last_data()
csv_data = read_csv("data/2025-07-03 20-12/last.csv")

csv_list = read_csv_columns("data/2025-07-03 20-12/last.csv")
content_list = csv_list[0]  # 第一列
print(content_list.index("['中国青年大有可为']"))
content_list = content_list[1:]    
url_list = csv_list[1]      # 第二列
url_list = url_list[1:]      
source_list = csv_list[2]   # 第三列
source_list = source_list[1:]  
catch_time_list = csv_list[3]  # 第四列
catch_time_list = catch_time_list[1:]  

# response处理，转换成列表
ac=AcRelationContent(content_list,url_list,source_list,catch_time_list)
response=ac.action(content_list)
pattern = r"\['(.*?)'\]"  
matches = re.findall(pattern, str(response))
print(matches)

#匹配提取对应的url
datas=[]
for item in csv_data:
    content = item.get("content")
    if not content:
        continue  # 跳过没有内容的项
    content = content.strip("[']")
    if content in matches:
        datas.append(item)

print(datas)