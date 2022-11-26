from google.cloud import pubsub_v1
import os

configs=[
    {
    "url":"https://shafaq.com/en/all-news",
    "tag":"a",
    "class_name":"overflow-hidden rounded-sm",
    "wait_for_selector":"body > main > div > div.grid.grid-cols-1.gap-5.md\:grid-cols-2.lg\:grid-cols-3 > article:nth-child(1) > a"
    }

]

attributes = {
    "configs": configs
}

credentials_path = "/Users/tanjoen/Documents/web-scraper-pw/credentials/croft_pubsub_key.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

topic_path = "projects/croft-pubsub/topics/croft-worker-scrape"

publisher = pubsub_v1.PublisherClient()

name = str(attributes)

name = name.encode("utf-8")

future = publisher.publish(topic_path, name)

print(future.result())