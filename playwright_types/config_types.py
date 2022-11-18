# from typing import Dict

# PageImpressionType = Dict['str','object' or 'str']
config_keys = []

def is_valid_config(config:PageImpressionType)->bool:
    return len([i for i in config.keys if i in config_keys]) == len(config_keys)
