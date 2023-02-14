import os
from requests import post, get
import json
import ast
# NOTION_DB_SCRAPE_ID = os.environ["NOTION_DB_SCRAPE_ID"]
NOTION_DB_RESULTS_ID = os.environ["NOTION_DB_RESULTS_ID"]
NOTION_API_LINK = os.environ["NOTION_API_LINK"]


def get_configs_to_scrape() -> list:
    configs = []
    response = get(F"{NOTION_API_LINK}/db/{NOTION_DB_SCRAPE_ID}").json()
    for result in response["results"]:
        configs.append(result["properties"]["Config"]
                       ["rich_text"][0]["plain_text"])
    return [ast.literal_eval(config) for config in configs]


def post_scraped_results(results: list) -> None:
    response = post(f"{NOTION_API_LINK}/feedback/{NOTION_DB_RESULTS_ID}", json={
        "name": results["url"],
        "email": "-",
        "feedback": str(results)
    })
    print(response)


if __name__ == "__main__":
    print(ast.literal_eval(get_configs_to_scrape()[0].replace("'", '"')))
    # post_scraped_results({
    #   "url":"https://google.com",
    #   "items":[1,2,3]
    # })
    pass
