from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_tags(tag:str,html:str)->list:
    soup = BeautifulSoup(html,"html.parser")
    return soup.find_all(tag)

def parse_tags_by_class(tag:str, class_name:str, html:str)->list:
    soup = BeautifulSoup(html,"html.parser")
    return soup.find_all(tag, {"class":class_name})

def get_attribute_by_class(attribute:str ,tag:str, class_name:str, html:str)->list:
    return [tag[attribute] for tag in parse_tags_by_class(tag,class_name,html)]

def get_full_urls_for_href(config:object, tags:list[str])->list[str]:
    return [urljoin(config["url"], tag["href"]) for tag in tags]