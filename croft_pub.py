from google.cloud import pubsub_v1
import os

configs = [
    {"url": "https://www.shafaq.com/en/All-News",        "items": [{"tag": "p",                "class_name": "mobile-title-breaking-news line-clamp-1 ltr-title dark:text-[#ABABAB]", },],
        "wait_for_selector": "body > main > div.space-y-10.rounded-md.py-4 >div.grid.grid-cols-1.gap-5.md\:grid-cols-2.lg\:grid-cols-3"}

]

attributes = {
    "configs": configs
}

# credentials_path = "/Users/tanjoen/Documents/web-scraper-pw/credentials/croft_pubsub_key.json"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

topic_path = "projects/croft-pubsub/topics/croft-worker-scrape"

publisher = pubsub_v1.PublisherClient()

name = str(attributes)

name = name.encode("utf-8")

future = publisher.publish(topic_path, name)

print(future.result())
