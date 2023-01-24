from bs4 import BeautifulSoup
from urllib.parse import urljoin


class BS4Parse:
    def __init__(self, result_obj):
        self.url = result_obj["url"]
        self.items = result_obj["items"]
        self.soup = BeautifulSoup(result_obj["html"])
    
    def parse_tags(self, tag:str)->list:
        return self.soup.find_all(tag)

    def parse_tags_by_class(self, tag:str, class_name:str)->list:
        return self.soup.find_all(tag, {"class":class_name})

    def parse_tag_by_id(self, tag:str, id:str)->list:
        return self.soup.find(tag, {"id":id})

    def get_attribute_by_class(self, attribute:str ,tag:str, class_name:str, html:str)->list:
        return [tag[attribute] for tag in parse_tags_by_class(tag,class_name,html)]

    def get_full_urls_for_href(self, config:object, tags:list[str], attr:str)->list[str]:
        return [urljoin(config["url"], tag[attr]) for tag in tags]
        