import twitter
import os
from dotenv import load_dotenv
import csv
import dateutil.parser

if __name__ == '__main__':

    # Load environment variables and initialize the Twitter API
    load_dotenv()
    api = twitter.Api(
        consumer_key=os.getenv('API_KEY'),
        consumer_secret=os.getenv('API_KEY_SECRET'),
        access_token_key=os.getenv('ACCESS_TOKEN'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))

    # Load output CSV
    fieldnames = ["tweetid", "message", "created_at", "favorite_count", "retweet_count", "source",
                  "geo_coordinates_latitude", "geo_coordinates_longitude", "place_id", "place_full_name", "place_type"]
    csv_output_file = None
    csv_writer = None
    if os.path.exists("output.csv"):
        # Append to the existing file
        csv_output_file = open("output.csv", "a", encoding="utf8", newline='')
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=',')
    else:
        # Create a new file
        csv_output_file = open("output.csv", "w", encoding="utf8", newline='')
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()

    # Filtering criteria
    LANGUAGES = ["en"]
    KEYWORDS = ["climate change", "earthquake", "flood"]

    # Initialize some tallies and start collecting tweets
    total_tweets = 0
    relevant_tweets = 0
    while True:
        # Occasionally, the connection gets interrupted. Having it in a loop here allows for automatic retries
        try:
            # api.GetStreamFilter will return a generator that yields one status
            # message (i.e., Tweet) at a time as a JSON dictionary.
            for tweet in api.GetStreamFilter(track=KEYWORDS, languages=LANGUAGES):
                print()
                print(f"Tweet {total_tweets}: {tweet['id']}, (relevant tweets so far: {relevant_tweets})")
                print(tweet["text"])
                total_tweets += 1

                # Things to filter based on
                if tweet["lang"] != "en":  # Only English tweets
                    print("Non-English tweet, skipping")
                    continue
                if tweet["place"] is None and tweet["geo"] is None:  # Only geotagged tweets
                    print("Non-Geotagged tweet, skipping")
                    continue

                # Finally, write tweet to output file
                output = {"tweetid": tweet["id"],
                          "message": tweet["text"],
                          "created_at": dateutil.parser.parse(tweet["created_at"]).isoformat(),
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

