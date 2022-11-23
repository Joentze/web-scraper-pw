
from time import time
from threading import Thread
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from config import MAX_NUM_OF_THREADS, PLAYWRIGHT_HEADLESS, PLAYWRIGHT_TIMEOUT, DEFAULT_SELECTOR_TO_WAIT
from parser import get_full_urls_for_href, parse_tags, parse_tags_by_class
# from config_types import is_valid_config
test = []
configs=[
    {
    "url":"https://shafaq.com/en/all-news",
    "tag":"a",
    "class_name":"overflow-hidden rounded-sm",
    "wait_for_selector":"body > main > div > div.grid.grid-cols-1.gap-5.md\:grid-cols-2.lg\:grid-cols-3 > article:nth-child(1) > a"
    }

]
def segment_content(content:list[object],num_of_threads:int)->None:
    segments = [[] for i in range(num_of_threads)]
    for i, config in enumerate(content):
        multiplier = i // num_of_threads
        segments[i - num_of_threads*multiplier].append(config)
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
        page = browser.new_page(java_script_enabled=True, user_agent="my-user-agent")
        page.goto(config["url"],wait_until="domcontentloaded")
        if "delay" in config:
            page.wait_for_timeout(config["delay"])
        page.wait_for_selector(w_sel)
        html = page.inner_html(DEFAULT_SELECTOR_TO_WAIT)
        #//{tag}[@{identifier}='{name}']
        # print([i.get_attribute("href") for i in page.query_selector_all(f"   //a[@class='h6__link list-object__heading-link']")])
        print(config["url"])
        print(parse_tags_by_class(config["tag"],config["class_name"],html))
        test.append(parse_tags_by_class(config["tag"],config["class_name"],html))
    return html 

def get_segment_inner_html(segment:list[object])->None:
    for config in segment:
        get_inner_html(config)

def run_scraper(configs):
    threads = [Thread(target=get_segment_inner_html,args=[x]) 
                for x in segment_content(configs, MAX_NUM_OF_THREADS)]
    #START THREADS
    for t in threads:
        t.start()
    #JOIN THREADS
    for t in threads:
        t.join()

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
    print(len(configs), "===",len(test))
    print(f'\n{"="*5+str(time()-start)+"s"+"="*5}')
    
