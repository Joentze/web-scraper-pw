import json
from time import time
from threading import Thread
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from config import MAX_NUM_OF_THREADS, PLAYWRIGHT_HEADLESS, PLAYWRIGHT_TIMEOUT, DEFAULT_SELECTOR_TO_WAIT
from bs4_parser import BS4Parse
from notion_db_call import post_scraped_results
# from config_types import is_valid_conf cig

# configs = get_configs_to_scrape()

configs = [
    {"url": "https://www.shafaq.com/en/All-News",        "items": [{"tag": "p",                "class_name": "mobile-title-breaking-news line-clamp-1 ltr-title dark:text-[#ABABAB]", },],
        "wait_for_selector": "body > main > div.space-y-10.rounded-md.py-4 >div.grid.grid-cols-1.gap-5.md\:grid-cols-2.lg\:grid-cols-3"}

]


def segment_content(content: list, num_of_threads: int) -> None:
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
            item_contents = []
            browser = p.chromium.launch(
                headless=PLAYWRIGHT_HEADLESS, timeout=PLAYWRIGHT_TIMEOUT)

            page = browser.new_page(
                java_script_enabled=True, user_agent="my-user-agent")

            page.goto(config["url"], wait_until="domcontentloaded")

            if "delay" in config:

                page.wait_for_timeout(config["delay"])

            page.wait_for_selector(w_sel)

            html = page.inner_html(DEFAULT_SELECTOR_TO_WAIT)

            ParseObject = BS4Parse(
                {"url": config["url"], "html": html, "items": config["items"]})

            item_contents = get_tags(ParseObject, config["items"])

            post_scraped_results(
                {"url": config["url"], "results": item_contents[0]})

    except Exception as e:

        print("error", e)

        # miss.append(config["url"])

    return {"url": config["url"], "results": item_contents}


def get_tags(BS4Parse, items) -> list:
    item_contents = []
    # print(BS4Parse)
    for item in items:

        keys = item.keys()

        if "class_name" in keys:

            result = BS4Parse.parse_tags_by_class(
                item["tag"], item["class_name"])

        elif "id" in keys:

            result = BS4Parse.parse_tag_by_id(item["tag"], item["id"])

        item_contents.append(result)

    return item_contents


def get_segment_inner_html(segment: list) -> None:
    for config in segment:
        try:
            get_inner_html(config)
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
