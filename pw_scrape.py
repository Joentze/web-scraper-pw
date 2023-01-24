import json
from time import time
from threading import Thread
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from config import MAX_NUM_OF_THREADS, PLAYWRIGHT_HEADLESS, PLAYWRIGHT_TIMEOUT, DEFAULT_SELECTOR_TO_WAIT
from bs4_parser import get_full_urls_for_href, parse_tags, parse_tags_by_class, parse_tag_by_id, get_attribute_by_class
# from notion_db_call import get_configs_to_scrape, post_scraped_results
# from config_types import is_valid_conf cig

# configs = get_configs_to_scrape()

configs = [
    {
        "url": "https://www.amazon.com/s?k=toys&s=date-desc-rank&pd_rd_r=198eabfe-75ec-469c-a989-9b43dad80bb2&pd_rd_w=26HV8&pd_rd_wg=Na0p2&pf_rd_p=779cadfb-bc4d-465d-931f-0b68c1ba5cd5&pf_rd_r=CV58886EY1Y28824VRD0&qid=1632870778&ref=pd_gw_unk",
        "items": [
            {
                "tag":"span",
                "class_name":"a-size-base-plus a-color-base a-text-normal"
            }
        ],

    }

]
print(configs)


def segment_content(content: list[object], num_of_threads: int) -> None:
    segments = [[] for i in range(num_of_threads)]
    for i, config in enumerate(content):
        multiplier = i // num_of_threads
        segments[i - num_of_threads*multiplier].append(config)
    return segments


def get_inner_html(config: object) -> object:
    html = ""
    
    # SET DEFAULT WAIT SELECTOR
    if "wait_for_selector" not in config.keys():
        w_sel = "html"
    else:
        w_sel = config["wait_for_selector"]
    # OPENS WEB DRIVER
    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=PLAYWRIGHT_HEADLESS, timeout=PLAYWRIGHT_TIMEOUT)

            page = browser.new_page(
                java_script_enabled=True, user_agent="my-user-agent")

            page.goto(config["url"], wait_until="domcontentloaded")

            if "delay" in config:

                page.wait_for_timeout(config["delay"])

            page.wait_for_selector(w_sel)

            html = page.inner_html(DEFAULT_SELECTOR_TO_WAIT)

            item_contents = get_tags(html, config["items"])

    except Exception as e:

        print(e)
        
        # miss.append(config["url"])

    return {"url": config["url"], "results": item_contents}


def get_tags(html, items)->list[object]:
    item_contents = []    

    for item in items:
        
        keys = item.keys()

        if "class_name" in keys:

            result = parse_tags_by_class(
            item["tag"], item["class_name"], html)

        elif "id" in keys:

            result = parse_tag_by_id(item["tag"], item["id"], html)

        item_contents.append(result)
    
    return item_contents


def get_segment_inner_html(segment: list[object]) -> None:
    for config in segment:
        results = get_inner_html(config)
        try:
            # post_scraped_results(results)
            print(results)
            print([result.text for result in results["results"][0]])
        except Exception as e:
            print(e)


def run_scraper(configs):
    threads = [Thread(target=get_segment_inner_html, args=[x])
               for x in segment_content(configs, MAX_NUM_OF_THREADS)]
    # START THREADS
    for thread in threads:
        thread.start()
    # JOIN THREADS
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start = time()
    run_scraper(configs)
    print(f'\n{"="*5+str(time()-start)+"s"+"="*5}')