import os 
from requests import post, get
NOTION_DB_SCRAPE_ID = os.environ["NOTION_DB_SCRAPE_ID"]
NOTION_DB_RESULTS_ID = os.environ["NOTION_DB_RESULTS_ID"]
NOTION_API_LINK = os.environ["NOTION_API_LINK"]

def get_configs_to_scrape()->list[object]:
    configs = []
    response = get(F"{NOTION_API_LINK}/db/{NOTION_DB_SCRAPE_ID}").json()
    for result in response["results"]:
        # print({
        #     "name":result["properties"]["Name"]["title"][0]["plain_text"],
        #     "link":result["properties"]["Link"]["rich_text"][0]["plain_text"],
        #     "config":result["properties"]["Config"]["rich_text"][0]["plain_text"]
        # })
        configs.append(result["properties"]["Config"]["rich_text"][0]["plain_text"])
    return configs

def post_scraped_results(results:list)->None:
    response = post(f"{NOTION_API_LINK}/feedback/{NOTION_DB_RESULTS_ID}", json={
        "name":results["url"],
        "email":"-",
        "feedback":str(results)
    })


if __name__ == "__main__":
    get_configs_to_scrape()
    # post_scraped_results({
    #   "url":"https://google.com",
    #   "items":[1,2,3]
    # })
    pass