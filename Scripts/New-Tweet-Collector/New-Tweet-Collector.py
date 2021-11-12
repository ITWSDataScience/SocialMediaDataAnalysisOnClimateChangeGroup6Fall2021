import twitter
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    api = twitter.Api(
        consumer_key=os.getenv('API_KEY'),
        consumer_secret=os.getenv('API_KEY_SECRET'),
        access_token_key=os.getenv('ACCESS_TOKEN'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))

    #print(api.VerifyCredentials())
    print(api.GetStatus("1458743621914705920"))
