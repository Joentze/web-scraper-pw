
import json
from time import time
from threading import Thread
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from config import MAX_NUM_OF_THREADS, PLAYWRIGHT_HEADLESS, PLAYWRIGHT_TIMEOUT, DEFAULT_SELECTOR_TO_WAIT
from parser import get_full_urls_for_href, parse_tags, parse_tags_by_class
# from config_types import is_valid_conf cig
results = []

miss = []

configs = [
    {
        "url": "",
        "wait_for_selector": "",
        "items": [
            {
                "tag": "h1",
                "class_name": "custom-font product-description-header",

            }, {
                "tag": "div",
                "class_name": "accordion-container accordion-container--product",

            }, {
                "tag": "div",
                "class_name": "description-block__content",

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


def get_inner_html(config: object) -> str:
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

            # item_contents = [[config["url"]]]

            # for item in config["items"]:

            #     item_contents.append(parse_tags_by_class(
            #         item["tag"], item["class_name"], html))

            # results.append(item_contents)
            # results.append(get_full_urls_for_href(config,parse_tags_by_class(config["tag"],config["class_name"],html), "href"))
    except:

        miss.append(config["url"])

    return {"url": config["url"], "items": config["items"], "html": html}


def get_segment_inner_html(segment: list[object]) -> None:
    for config in segment:
        get_inner_html(config)


def run_scraper(configs):
    threads = [Thread(target=get_segment_inner_html, args=[x])
               for x in segment_content(configs, MAX_NUM_OF_THREADS)]
    # START THREADS
    for t in threads:
        t.start()
    # JOIN THREADS
    for t in threads:
        t.join()


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
    print(results)

    print(len(configs), "===", len(results))
    print(f'\n{"="*5+str(time()-start)+"s"+"="*5}')
