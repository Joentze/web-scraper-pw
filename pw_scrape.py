import json
from time import time
from threading import Thread
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from config import MAX_NUM_OF_THREADS, PLAYWRIGHT_HEADLESS, PLAYWRIGHT_TIMEOUT, DEFAULT_SELECTOR_TO_WAIT
from parser import get_full_urls_for_href, parse_tags, parse_tags_by_class
from notion_db_call import get_configs_to_scrape, post_scraped_results
# from config_types import is_valid_conf cig
results = []

miss = []

configs = get_configs_to_scrape()

# configs = [
#     {
#         "url": "https://boundbywine.com/collections/wine-1/products/lagertal-holunder-goldtraminer-2020",
#         "items": [
#             {
#                 "tag": "h1",
#                 "class_name": "custom-font product-description-header",

#             }, {
#                 "tag": "div",
#                 "class_name": "accordion-container accordion-container--product",

#             }, {
#                 "tag": "div",
#                 "class_name": "description-block__content",

#             }
#         ],

#     }

# ]
print(configs)


def segment_content(content: list[object], num_of_threads: int) -> None:
    segments = [[] for i in range(num_of_threads)]
    for i, config in enumerate(content):
        multiplier = i // num_of_threads
        segments[i - num_of_threads*multiplier].append(config)
    return segments


def get_inner_html(config: object) -> str:
    html = ""
    
    item_contents = [[config["url"]]]
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
            print(html)
            for item in config["items"]:
                result = parse_tags_by_class(
                    item["tag"], item["class_name"], html)
                item_contents.append(result)
                print("result: ", result)

    except:
        miss.append(config["url"])

    return {"url": config["url"], "items": item_contents[:2]}


def get_segment_inner_html(segment: list[object]) -> None:
    for config in segment:
        results = get_inner_html(config)
        print(results)
        try:
            post_scraped_results(results)
        except:
            pass


def run_scraper(configs):
    threads = [Thread(target=get_segment_inner_html, args=[x])
               for x in segment_content(configs, MAX_NUM_OF_THREADS)]
    # START THREADS
    for t in threads:
        t.start()
    # JOIN THREADS
    for t in threads:
        t.join()
    # print(results)


if __name__ == "__main__":
    start = time()

    TOTAL_THREADS = MAX_NUM_OF_THREADS
    # [print(len(x)) for x in segment_content(configs, TOTAL_THREADS)]
    # if len(configs) != len([config for config in configs if is_valid_config(config)]):
    #     raise Exception("configs are not of valid types")

    threads = [Thread(target=get_segment_inner_html, args=[x])
               for x in segment_content(configs, TOTAL_THREADS)]
    # START THREADS
    for t in threads:
        t.start()
    # JOIN THREADS
    for t in threads:
        t.join()

    # all_links = []
    # for link_list in results:
    #     all_links+=link_list

    # with open("all_links.txt","w") as file:
    #     write_str = "\n".join(list(set(all_links)))
    #     file.write(write_str)
    # print(results)

    print(len(configs), "===", len(results))
    print(f'\n{"="*5+str(time()-start)+"s"+"="*5}')