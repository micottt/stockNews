from twilio.rest import Client
import requests

STOCK_API_KEY = "G1C3ZQAROGQ3Q9RP"
STOCK_API_URL = "https://www.alphavantage.co/query"
STOCK_FUNCTION = "TIME_SERIES_WEEKLY"
STOCK_SYMBOL = "TSLA"
COMPANY_NAME = "Tesla Inc"


NEWS_API_KEY = "121ce85f89a64850b5c71362f210f95e"
NEWS_API_URL = "https://newsapi.org/v2/everything"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

STOCK_PARAMETERS = {
    "function": STOCK_FUNCTION,
    "symbol": STOCK_SYMBOL,
    "apikey": STOCK_API_KEY
}
stock_response = requests.get(url=STOCK_API_URL, params=STOCK_PARAMETERS)
stock_response.raise_for_status()
stock_data = stock_response.json()["Weekly Time Series"]
data_list = [value for key, value in stock_data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

price_diff = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
print(price_diff)

diff_percent = price_diff / float(yesterday_closing_price) * 100
print(diff_percent)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

if abs(diff_percent) >= 5:
    NEWS_PARAMETERS = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_API_URL, params=NEWS_PARAMETERS)
    three_articles = news_response.json()["articles"][:3]
    print(three_articles)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

account_sid = "AC27d88c06861f7c149e6893058d4a8b77"
auth_token = "1016a8736b6cea85ab33b4d63c51a169"
client = Client(account_sid, auth_token)
MESSAGE_ON = True
if MESSAGE_ON:
    for article in formatted_articles:
        message = client.messages.create(
                                      body=article,
                                      from_='+18775408141',
                                      to='+19084948491'
                                  )
        print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

