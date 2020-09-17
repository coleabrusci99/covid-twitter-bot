from bs4 import BeautifulSoup as bs
import tweepy
import requests
from datetime import date, timedelta
import time
import schedule

# Get covid statistics and save them to dictionary
def get_statistics():
    # Grabs data from the nytimes covid tracker
    req = requests.get(
        "https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html")
    soup = bs(req.text, 'html.parser')

    data_tags = soup.find_all("span", class_="svelte-8rsupl")
    data_dict = {"cases": {}, "deaths": {}}

    # Saving the data to the data_dict dictionary based on css class names
    for data in data_tags:
        class_name = data.parent["class"]
        table_class = data.parent.parent["class"]
        if "cases" in table_class:
            if "totals" in class_name:
                data_dict["cases"]["total"] = data.text
            elif "yesterday" in class_name:
                data_dict["cases"]["new"] = data.text
        elif "deaths" in table_class:
            if "totals" in class_name:
                data_dict["deaths"]["total"] = data.text
            elif "yesterday" in class_name:
                data_dict["deaths"]["new"] = data.text

    return data_dict

# Format string to tweet
def format_tweet():
    data = get_statistics()
    yesterday = date.today() - timedelta(days=1)
    tweet = f"{yesterday}\n\nCases:\nTotal Cases = {data['cases']['total']}, with {data['cases']['new']} new cases being reported\n\nDeaths:\nTotal Deaths = {data['deaths']['total']}, with {data['deaths']['new']} new deaths being reported"
    return tweet

# Set up tweepy authorization and access
def send_tweet(message):
    api_key = "6AvHRxUALGoeOp4xMjtuDGxSK"
    api_secret = "wBeqr7i0LhFplip7UME3qAtn7N0bJAg0K2iopKFBm3iF36Bc85"
    access_token = "1306295025983082496-uu1e8aPBkkPURmdtwYZI9KOtpNC3Xm"
    access_secret = "yQHNMhPpT59e7edgK7Q6bgyfQsnvUL6acUzVpFx4YVxZf"

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    api.update_status(message)

# Function that is called from the scheduler
def full_task():
    tweet = format_tweet()
    send_tweet(tweet)


if __name__ == "__main__":
    # Sets the program to run at 09:00 every day (while the script is running)
    schedule.every().day.at("09:00").do(full_task)
    while True:
        schedule.run_pending()
        time.sleep(60)
