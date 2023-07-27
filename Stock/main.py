import requests
from twilio.rest import Client
#Twilio Auth
account_sid = 'AC03b6c80197c7d4320f015a5e48c6a8fa'
auth_token = "4d0a6733608ad19f8b996a80107219d8"

STOCK_NAME = "INFY"
COMPANY_NAME = "Infosys"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY = "F6O2CY96AJ6JUKMB"
NEWS_API_KEY = "0ebd130ae60c4c389338f8ffb4b5aa49"
stock_params = {"function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": STOCK_NAME,
                "apikey": API_KEY,
                }

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_data_closing = yesterday_data['4. close']
print(yesterday_data_closing)


day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing = day_before_yesterday_data['4. close']
print(day_before_yesterday_data_closing)

difference = float(day_before_yesterday_data_closing) - float(yesterday_data_closing)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percent = abs(difference) / float(yesterday_data_closing) * 100
print(diff_percent)

if diff_percent > 0.3:
    news_params = {"qInTitle": COMPANY_NAME,
                   "apiKey": NEWS_API_KEY,}
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    articles = news_response.json()["articles"]
    print(articles)
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 


    three_articles = articles[0:3]
    formatted_articles = [f"{STOCK_NAME}:{up_down}{round(abs(diff_percent))}% \nHeadline : {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 


    client = Client(account_sid, auth_token)


    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_='+13158475745',
            to='+919606659950'
        )


