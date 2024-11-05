from utils import read_yaml
from catch import Catch



config_file=read_yaml('config.yaml')
catch=Catch(config_file)
catch.save_data
file_path=catch.file_path