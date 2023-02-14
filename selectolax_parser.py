from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from pprint import pprint
test_data = {
    "url": "https://books.toscrape.com",
    "wait_for_selector": "article.product_pod",
    "items_to_scrape": [
        {
            "css_selector": "div.image_container",
            "get_attributes": []

        }
    ]

}


@dataclass
class ParseItemConfig:
    css_selector: str
    get_attributes: list[str] | None


@dataclass
class ParseConfig:
    url: str
    items_to_scrape: list[ParseItemConfig]
    wait_for_selector: str | None


def scrape_items(html: str, config: ParseConfig):
    if "wait_for_selector" in config:
        config = ParseConfig(url=config["url"], items_to_scrape=config["items_to_scrape"],
                             wait_for_selector=config["wait_for_selector"])
    else:
        config = ParseConfig(url=config["url"], items_to_scrape=config["items_to_scrape"],
                             wait_for_selector=None)
    tree = HTMLParser(html)
    for item in config.items_to_scrape:
        pprint([[{"text": x.text().strip().replace("\n", ""), **x.attributes} for x in i.traverse()]
                for i in tree.css(item["css_selector"])])


if __name__ == "__main__":
    scrape_items(test_data)
