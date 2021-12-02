import csv
import twitter
import os
from dotenv import load_dotenv
import sys

if __name__ == '__main__':

    # Load environment variables and initialize the Twitter API
    load_dotenv()
    api = twitter.Api(
        consumer_key=os.getenv('API_KEY'),
        consumer_secret=os.getenv('API_KEY_SECRET'),
        access_token_key=os.getenv('ACCESS_TOKEN'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
        sleep_on_rate_limit=True)

    # Make sure we got 2 arguments passed in
    if len(sys.argv) < 3:
        print("Error: 2 arguments required, input csv and output csv files")
        sys.exit(1)

    # Load CSVs
    csv_input_file = open(sys.argv[1], "r", encoding="utf8")
    csv_reader = csv.DictReader(csv_input_file, delimiter=',')

    # Set up the output file
    fieldnames = ["tweetid", "message", "sentiment", "created_at", "favorite_count", "retweet_count", "source",
                  "geo_coordinates_latitude", "geo_coordinates_longitude", "place_id", "place_full_name", "place_type"]
    csv_output_file = open(sys.argv[2], "w", encoding="utf8", newline='')
    csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=',')
    csv_writer.writeheader()

    # Load the IDs from the rows in the input file
    rows = {}
    for row in csv_reader:
        rows[int(row["tweetid"])] = row["sentiment"]

    # Process in batches of 5000 tweets to avoid hitting API limits (as much as possible)
    tweet_data = {}
    i = 0
    while i < len(rows):
        k = i + min(5000, len(rows) - i)
        api_data = api.GetStatuses(list(rows.keys())[i:k], trim_user=True, include_entities=False, map=True)
        tweet_data.update(api_data)
        i = k

    # Now that we've gathered all the tweet data, filter out any data that we don't want
    # This consists of tweets that are no longer available, don't have a geotag or place tag, or aren't in English
    for key in tweet_data.keys():
        api_data = tweet_data.get(key)
        if api_data is None:  # Invalid Tweets, likely deleted, user banned, made private, etc.
            continue

        # Things to filter based on
        if api_data.lang != "en":  # Only English tweets
            print("Non-English tweet, skipping")
            continue
        if api_data.place is None and api_data.geo is None:  # Only geotagged tweets
            print("Non-Geotagged tweet, skipping")
            continue

        # Finally, write tweet to the output file
        output = {"tweetid": api_data.id,
                  "message": api_data.text,
                  "sentiment": rows.get(key),
                  "created_at": api_data.created_at,
                  "favorite_count": api_data.favorite_count,
                  "retweet_count": api_data.retweet_count,
                  "source": api_data.source,
                  "geo_coordinates_latitude": "",
                  "geo_coordinates_longitude": "",
                  "place_id": "",
                  "place_full_name": "",
                  "place_type": ""}

        if api_data.geo is not None:
            output["geo_coordinates_latitude"] = api_data.geo["coordinates"][0]
            output["geo_coordinates_longitude"] = api_data.geo["coordinates"][1]
        if api_data.place is not None:
            output["place_id"] = api_data.place["id"]
            output["place_full_name"] = api_data.place["full_name"]
            output["place_type"] = api_data.place["place_type"]

        csv_writer.writerow(output)
