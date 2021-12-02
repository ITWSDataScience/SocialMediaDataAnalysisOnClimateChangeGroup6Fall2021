import csv
import twitter
import os
from dotenv import load_dotenv
import sys
import dateutil.parser

if __name__ == '__main__':

    # Load CSVs
    csv_input_file = open("output.csv", "r", encoding="utf8")
    csv_reader = csv.DictReader(csv_input_file, delimiter=',')

    # Set up the output file
    fieldnames = ["tweetid", "message", "created_at", "favorite_count", "retweet_count", "source",
                  "geo_coordinates_latitude", "geo_coordinates_longitude", "place_id", "place_full_name", "place_type"]
    csv_output_file = open("output2.csv", "w", encoding="utf8", newline='')
    csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames, delimiter=',')
    csv_writer.writeheader()

    for row in csv_reader:
        # Finally, write tweet to the output file
        output = {"tweetid": row["tweetid"],
                  "message": row["message"],
                  "created_at": dateutil.parser.parse(row["created_at"]).isoformat(),
                  "favorite_count": row["favorite_count"],
                  "retweet_count": row["retweet_count"],
                  "source": row["source"],
                  "geo_coordinates_latitude": row["geo_coordinates_latitude"],
                  "geo_coordinates_longitude": row["geo_coordinates_longitude"],
                  "place_id": row["place_id"],
                  "place_full_name": row["place_full_name"],
                  "place_type": row["place_type"]}

        csv_writer.writerow(output)
