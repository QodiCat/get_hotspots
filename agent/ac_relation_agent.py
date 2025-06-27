from utils.ai import DeepSeekAPI
import os
from utils.read_json import read_json_file

class AcRelationContent:
    def __init__(self,content_list,url_list,source_list,catch_time_list):
        self.content_list=content_list
        self.url_list=url_list
        self.system_prompt=read_json_file("agent_prompt/ac_relation_content/ac_relation.json")
        self.source_list=source_list
        self.catch_time_list=catch_time_list
        self.deepseek=DeepSeekAPI(os.getenv("DEEPSEEK_API_KEY"),self.system_prompt)

    def action(self):
        pass