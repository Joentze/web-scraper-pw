
from time import time
from threading import Thread
from playwright.sync_api import sync_playwright
from config import MAX_NUM_OF_THREADS, PLAYWRIGHT_HEADLESS, PLAYWRIGHT_TIMEOUT, DEFAULT_SELECTOR_TO_WAIT
from parser import parse_tags, parse_tags_by_class
# from config_types import is_valid_config

configs=[
    {
    "url":"https://www.reuters.com/world/us/how-biden-white-house-scrambled-after-poland-missile-blast-2022-11-18/",
    "tag":"p",
    "class_name":"text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__large__nEccO body__full_width__ekUdw body__large_body__FV5_X article-body__element__2p5pI",
    "wait_for_selector":"#main-content > article > div > div.article__main__33WV2 > div:nth-child(3) > div > div.article-body__content__17Yit.paywall-article"
    }
,{
    "url":"https://www.reuters.com/world/us/hakeem-jeffries-launches-bid-lead-us-house-democrats-2022-11-18/",
    "tag":"p",
    "class_name":"text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__large__nEccO body__full_width__ekUdw body__large_body__FV5_X article-body__element__2p5pI",
    "wait_for_selector":"#main-content > article > div > div.article__main__33WV2 > div:nth-child(3) > div > div.article-body__content__17Yit.paywall-article"
    },{
    "url":"https://www.reuters.com/world/us/democrat-frisch-concedes-republican-incumbent-boebert-us-house-election-colorado-2022-11-18/",
    "tag":"p",
    "class_name":"text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__large__nEccO body__full_width__ekUdw body__large_body__FV5_X article-body__element__2p5pI",
    "wait_for_selector":"#main-content > article > div > div.article__main__33WV2 > div:nth-child(3) > div > div.article-body__content__17Yit.paywall-article"
    },{
    "url":"https://www.reuters.com/legal/us-urges-jury-convict-oath-keepers-plotting-block-peaceful-transfer-power-2022-11-18/",
    "tag":"p",
    "class_name":"text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__large__nEccO body__full_width__ekUdw body__large_body__FV5_X article-body__element__2p5pI",
    "wait_for_selector":"#main-content > article > div > div.article__main__33WV2 > div:nth-child(3) > div > div.article-body__content__17Yit.paywall-article"
    },{
    "url":"https://duckduckgo.com/?q=apples&kp=1&t=h_&iax=images&ia=images",
    "tag":"img",
    "class_name":"tile--img__img js-lazyload",
    "wait_for_selector":"#zci-images > div > div.tile-wrap > div > div:nth-child(3) > div.tile--img__media > span > img"
    },{
    "url":"https://duckduckgo.com/?q=apples&kp=1&t=h_&iax=images&ia=images",
    "tag":"img",
    "class_name":"tile--img__img js-lazyload",
    "wait_for_selector":"#zci-images > div > div.tile-wrap > div > div:nth-child(3) > div.tile--img__media > span > img"
    }
]
def segment_content(content:list[object],num_of_threads:int)->None:
    segments = [[] for i in range(num_of_threads)]
    print(segments)
    for i, config in enumerate(content):
        multiplier = i // num_of_threads
        segments[i - num_of_threads*multiplier].append(config)
    print(segments)
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
        page.goto(config["url"],wait_until="domcontentloaded")
        page.wait_for_selector(w_sel)
        html = page.inner_html(DEFAULT_SELECTOR_TO_WAIT)
        #//{tag}[@{identifier}='{name}']
        # print([i.get_attribute("href") for i in page.query_selector_all(f"   //a[@class='h6__link list-object__heading-link']")])
        print(config["url"])
        # print(parse_tags_by_class(config["tag"],config["class_name"],html))
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
