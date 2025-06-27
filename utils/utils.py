

from omegaconf import OmegaConf

def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data=OmegaConf.load(f)
    return data