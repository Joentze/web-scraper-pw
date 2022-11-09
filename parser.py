from bs4 import BeautifulSoup

def parse_tags(tag:str,html:str)->list:
    soup = BeautifulSoup(html)
    return soup.find_all(tag)

def parse_tags_by_class(tag:str, class_name:str, html:str)->list:
    soup = BeautifulSoup(html)
    return soup.find_all(tag, {"class":class_name})

def get_attribute_by_class(attribute:str ,tag:str, class_name:str, html:str)->list:
    return [tag[attribute] for tag in parse_tags_by_class(tag,class_name,html)]