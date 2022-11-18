from typing import Dict

PageImpressionType = Dict['str','object' or 'str']

CLASS_CONFIG_KEYS = {"url":str, "tag":str, "class_name":str}

def is_valid_config(config:PageImpressionType, config_type:object)->bool:
    return len([i for i in config.keys() if i in config_type and config_type[i] == type(config[i])]) == len(config_type)

test_config_obj = {
    "url":"",
    "tag":"",
    "class_name":""
}

if __name__ == "__main__":
    print(is_valid_config(test_config_obj))

