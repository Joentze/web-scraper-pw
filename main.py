
from time import time
from threading import Thread
from playwright.sync_api import sync_playwright

configs=[{
    "url":"https://www.channelnewsasia.com/?cid=google_sem_paid_12042022_cnamkt&gclid=CjwKCAjwp9qZBhBkEiwAsYFsb_9Ur0tbWTMgZ4dKxwPckd4rK2vLPs-zjeK1fX0K-31lxDvvAIy3wxoCBywQAvD_BwE"
},{
    "url":"https://www.channelnewsasia.com/?cid=google_sem_paid_12042022_cnamkt&gclid=CjwKCAjwp9qZBhBkEiwAsYFsb_9Ur0tbWTMgZ4dKxwPckd4rK2vLPs-zjeK1fX0K-31lxDvvAIy3wxoCBywQAvD_BwE"
}]


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
        browser = p.chromium.launch(headless=True, timeout=10000)
        page = browser.new_page(java_script_enabled=True)
        page.goto(config["url"])
        page.wait_for_selector(w_sel)
        html = page.inner_html("html")
    print(html)
    return html 


if __name__ == "__main__":
    start = time()
    
    TOTAL_THREADS = 4
    # [print(len(x)) for x in segment_content(configs, TOTAL_THREADS)]
    threads = [Thread(target=get_inner_html,args=[configs[i]]) for i in range(TOTAL_THREADS)]
    #START THREADS
    for t in threads:
        t.start()
    #JOIN THREADS
    for t in threads:
        t.join()
    
    print(f'\n{"="*5+str(time()-start)+"s"+"="*5}')
