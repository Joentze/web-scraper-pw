from google.cloud import pubsub_v1
import os

configs=[
    {
        "url": "https://boundbywine.com/collections/wine-1/products/lagertal-holunder-goldtraminer-2020",
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