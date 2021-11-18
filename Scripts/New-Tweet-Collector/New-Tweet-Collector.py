import twitter
import os
from dotenv import load_dotenv
import csv
import sys
import json

if __name__ == '__main__':
    load_dotenv()

    api = twitter.Api(
        consumer_key=os.getenv('API_KEY'),
        consumer_secret=os.getenv('API_KEY_SECRET'),
        access_token_key=os.getenv('ACCESS_TOKEN'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))

    #print(api.VerifyCredentials())
    #print(api.GetStatus("1458743621914705920"))

    # Load output CSV
    fieldnames = ["tweetid", "message", "created_at", "favorite_count", "retweet_count", "source",
                  "geo_coordinates_latitude", "geo_coordinates_longitude", "place_id", "place_full_name", "place_type"]
    csv_output_file = None
    csv_writer = None
    if os.path.exists("output.csv"):
        # Append
        csv_output_file = open("output.csv", "a", encoding="utf8", newline='')
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=',')
    else:
        csv_output_file = open("output.csv", "w", encoding="utf8", newline='')
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()

    # api.GetStreamFilter will return a generator that yields one status
    # message (i.e., Tweet) at a time as a JSON dictionary.
    LOCATIONS = ["-124.848974,24.396308,-66.885444,49.384358"]  # NOTE, works as "OR" with keywords, not AND
    LANGUAGES = ["en"]
    KEYWORDS = ["climate change", "earthquake", "flood"]

    total_tweets = 0
    relevant_tweets = 0
    while True:
        try:
            for tweet in api.GetStreamFilter(track=KEYWORDS, languages=LANGUAGES):
                print()
                print(f"Tweet {total_tweets}: {tweet['id']}, (relevant tweets so far: {relevant_tweets})")
                print(tweet["text"])
                #print(tweet["geo"])
                #print(tweet["place"])
                total_tweets += 1

                # Things to filter based on
                if tweet["lang"] != "en":  # Only English tweets
                    print("Non-English tweet, skipping")
                    continue
                if tweet["place"] is None and tweet["geo"] is None:  # Only geotagged tweets
                    print("Non-Geotagged tweet, skipping")
                    continue

                # Finally, write tweet
                output = {"tweetid": tweet["id"],
                          "message": tweet["text"],
                          "created_at": tweet["created_at"],
                          "favorite_count": tweet["favorite_count"],
                          "retweet_count": tweet["retweet_count"],
                          "source": tweet["source"],
                          "geo_coordinates_latitude": "",
                          "geo_coordinates_longitude": "",
                          "place_id": "",
                          "place_full_name": "",
                          "place_type": ""}

                if tweet["geo"] is not None:
                    output["geo_coordinates_latitude"] = tweet["geo"]["coordinates"][0]
                    output["geo_coordinates_longitude"] = tweet["geo"]["coordinates"][1]
                if tweet["place"] is not None:
                    output["place_id"] = tweet["place"]["id"]
                    output["place_full_name"] = tweet["place"]["full_name"]
                    output["place_type"] = tweet["place"]["place_type"]

                relevant_tweets += 1
                csv_writer.writerow(output)
                csv_output_file.flush()

        except:
            print("Stream died, restarting...")

