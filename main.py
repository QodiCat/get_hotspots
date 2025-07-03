from utils.utils import read_yaml
from catch import Catch
from agent.ac_relation_agent import AcRelationContent


config_file=read_yaml('config.yaml')
catch=Catch(config_file)
catch.save_data()
catch.merge_data()

content_list,url_list,source_list,catch_time_list=catch.get_last_data()


ac=AcRelationContent(content_list,url_list,source_list,catch_time_list)
response=ac.action(content_list)
print(response)