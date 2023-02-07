# from google.cloud import pubsub_v1
from pw_scrape import run_scraper
from concurrent.futures import TimeoutError
# import ast
# import os
import json

from flask import Flask, request

app = Flask(__name__)

PORT = int(os.environ["PORT"])

# credentials_path = "/Users/tanjoen/Documents/web-scraper-pw/credentials/croft_pubsub_key.json"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

subscriber_path = "projects/croft-pubsub/subscriptions/croft-worker-scrape-sub"

subscriber = pubsub_v1.SubscriberClient()

def callback(message):
    print("Receiving a new message!")

    configs = message.data.decode("utf-8")

    configs = json.loads(configs.replace("'",'"'))

    if configs and "configs" in configs:
        run_scraper(configs["configs"])
    message.ack()
        
streaming_pull_futures = subscriber.subscribe(subscriber_path, callback)
            
while subscriber:
    try:
        streaming_pull_futures.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_futures.result()

print(future.result())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)