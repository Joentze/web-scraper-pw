# from google.cloud import pubsub_v1
from pw_scrape import run_scraper
from concurrent.futures import TimeoutError
from threading import Thread
import ast
import os
# import json
import base64
from flask import Flask, request

app = Flask(__name__)

PORT = int(os.environ["PORT"])


@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()

    def scraper(configs):
        run_scraper(configs)

    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        string_obj = base64.b64decode(
            pubsub_message["data"]).decode("utf-8").strip()

    data_configs = ast.literal_eval(string_obj)

    if data_configs and "configs" in data_configs:
        thread = Thread(target=scraper, kwargs={
                        "configs": data_configs["configs"]})
        thread.start()
        thread.join()
    else:
        return ("", 400)

    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
