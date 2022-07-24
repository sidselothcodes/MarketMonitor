import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
STOCK_API_KEY = os.environ.get("api_key")
NEWS_API_KEY = "e0c1b2e3c12c4da88cf5c6ba7806b23a"
ACCOUNT_SID = "AC4d8a205269c0fa3e0c64c1ed411d5a4e"
AUTH_TOKEN = os.environ.get("token")
TWILIO_NUMBER = os.environ.get("twilio_number")
MY_NUMBER = os.environ.get("number")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(day_before_yesterday_closing_price) - float(yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price))) * 100
print(diff_percent)

if abs(diff_percent) > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for article in three_articles:
        message = Client.messages.create(
            body='This is the ship that made the Kessel Run in fourteen parsecs?',
            from_= TWILIO_NUMBER,
            to= MY_NUMBER
        )

        print(message.status)

