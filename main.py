
from time import time
from threading import Thread
from playwright.sync_api import sync_playwright
from config import MAX_NUM_OF_THREADS, PLAYWRIGHT_HEADLESS, PLAYWRIGHT_TIMEOUT, DEFAULT_SELECTOR_TO_WAIT
from parser import parse_tags, parse_tags_by_class
# from config_types import is_valid_config

configs=[
    {
    "url":"https://www.channelnewsasia.com/singapore/apec-inclusive-growth-digital-economy-3084021",
    "tag":"div",
    "class_name":"text"

},{
    "url":"https://www.channelnewsasia.com/latest-news",
    "tag":"a",
    "class_name":"h6__link list-object__heading-link"
},{
    "url":"https://www.quark.bz",
    "tag":"",
    "class_name":""
},{
    "url":"https://www.channelnewsasia.com/?cid=google_sem_paid_12042022_cnamkt&gclid=CjwKCAjwp9qZBhBkEiwAsYFsb_9Ur0tbWTMgZ4dKxwPckd4rK2vLPs-zjeK1fX0K-31lxDvvAIy3wxoCBywQAvD_BwE",
    "tag":"",
    "class_name":""
},
]

def segment_content(content:list[object],num_of_threads:int)->None:
    segments = []
    segment_size = len(content)//num_of_threads
    for i in range(num_of_threads):
        if i == num_of_threads-1:
            segments+=[content[i*segment_size:-1]]
        else:
            segments+=[content[i*segment_size:i*segment_size+segment_size+1]]
    return segments


def get_inner_html(config:object)->str:
    html=""
    #SET DEFAULT WAIT SELECTOR
    if "wait_for_selector" not in config.keys():
        w_sel = "html"
    else:
        w_sel = config["wait_for_selector"]
    #OPENS WEB DRIVER
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=PLAYWRIGHT_HEADLESS, timeout=PLAYWRIGHT_TIMEOUT)
        page = browser.new_page(java_script_enabled=True)
        page.goto(config["url"])
        page.wait_for_selector(w_sel)
        html = page.inner_html(DEFAULT_SELECTOR_TO_WAIT)
        #//{tag}[@{identifier}='{name}']
        # print([i.get_attribute("href") for i in page.query_selector_all(f"   //a[@class='h6__link list-object__heading-link']")])
        
        print(parse_tags_by_class(config["tag"],config["class_name"],html))
    return html 

def get_segment_inner_html(segment:list[object])->None:
    for config in segment:
        get_inner_html(config)

if __name__ == "__main__":
    start = time()
    
    TOTAL_THREADS = MAX_NUM_OF_THREADS
    # [print(len(x)) for x in segment_content(configs, TOTAL_THREADS)]
    # if len(configs) != len([config for config in configs if is_valid_config(config)]):
    #     raise Exception("configs are not of valid types")

    threads = [Thread(target=get_segment_inner_html,args=[x]) 
                for x in segment_content(configs, TOTAL_THREADS)]
    #START THREADS
    for t in threads:
        t.start()
    #JOIN THREADS
    for t in threads:
        t.join()
    
    print(f'\n{"="*5+str(time()-start)+"s"+"="*5}')
