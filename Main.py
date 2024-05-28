import requests
from bs4 import BeautifulSoup
import schedule
import time

def scrape_twitter_page(url, ticker):
   
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tweets = soup.find_all('div', {'data-testid': 'tweet'})
        
        mentions = 0
        for tweet in tweets:
            if ticker in tweet.text:
                mentions += 1
                
        return mentions
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return 0

def scrape_all_accounts(accounts, ticker, interval):

    total_mentions = 0
    for account in accounts:
        mentions = scrape_twitter_page(account, ticker)
        total_mentions += mentions
        print(f"{ticker} was mentioned {mentions} times on {account}.")
    
    print(f"'{ticker}' was mentioned '{total_mentions}' times in the last '{interval}' minutes.")

# Define the Twitter accounts and ticker symbols to scrape
twitter_accounts = [
    "https://twitter.com/Mr_Derivatives",
    "https://twitter.com/warrior_0719",
    "https://twitter.com/ChartingProdigy",
    "https://twitter.com/allstarcharts",
    "https://twitter.com/yuriymatso",
    "https://twitter.com/TriggerTrades",
    "https://twitter.com/AdamMancini4",
    "https://twitter.com/CordovaTrades",
    "https://twitter.com/Barchart",
    "https://twitter.com/RoyLMattox"
]

# Example usage
ticker_symbol = '$TSLA'
scrape_interval = 1  # in minutes

# Schedule the scraping function
schedule.every(scrape_interval).minutes.do(scrape_all_accounts, twitter_accounts, ticker_symbol, scrape_interval)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
