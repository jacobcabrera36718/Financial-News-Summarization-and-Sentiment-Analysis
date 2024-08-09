from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import re
import csv

# Load the Pegasus tokenizer and model for financial summarization
tokenizer = PegasusTokenizer.from_pretrained("human-centered-summarization/financial-summarization-pegasus")
model = PegasusForConditionalGeneration.from_pretrained("human-centered-summarization/financial-summarization-pegasus")

# 'AAPL', 'MSFT', 'WMT', 'JPM', 'NFLX' Other sample tickers to test
monitor_company_tickers = ['TSLA', 'NVDA', 'META', 'AMZN', 'GOOGL']

# https://www.google.com/search?q=yahoo+finance&tbm=nws yahoo finance url test case instead of investing.com
# Generate URLs for news articles for given stock tickers
def stock_news_url(tickers):
    url_search = "https://www.google.com/search?q=investing.com&tbm=nws".format(tickers)
    request = requests.get(url_search)
    soup = BeautifulSoup(request.text, 'html.parser')
    tags = soup.find_all('a')
    href = [link['href'] for link in tags]
    return href

# List to save urls from function above
raw_urls = {ticker:stock_news_url(ticker) for ticker in monitor_company_tickers}

exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support']

# Clean urls so they are not as long
def strip_url(urls, exclude_list):
    val = []
    for url in urls:
        if 'https://' in url and not any(exclude_word in url for exclude_word in exclude_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            val.append(res)
    return list(set(val))

# List to save new cleaned urls
clean_urls = {ticker:strip_url(raw_urls[ticker] , exclude_list) for ticker in monitor_company_tickers} 

# Scrape articles for given cleaned urls
def scrape_url(URLS):
    articles = []
    for url in URLS:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = [paragraph.text for paragraph in paragraphs]
        words = ' '.join(text).split(' ')[:350]
        article = ' '.join(words)
        articles.append(article)
    return articles

# List to save scraped articles
url_articles = {ticker:scrape_url(clean_urls[ticker]) for ticker in monitor_company_tickers} 


def summarize_url_article(url_articles):
    summarized_articles = []
    for article in url_articles:
        id_input = tokenizer.encode(article, return_tensors = 'pt')
        output = model.generate(id_input, max_length = 100, num_beams = 5, early_stopping = True)
        summary = tokenizer.decode(output[0], skip_special_tokens = True)
        summarized_articles.append(summary)
    return summarized_articles

# List to save article summeries
summaries = {ticker:summarize_url_article(url_articles[ticker]) for ticker in monitor_company_tickers}

# Initialize the sentiment analysis pipeline
sentiment = pipeline('sentiment-analysis')

# Analyze sentiment for each summary
sentiments = {ticker:sentiment(summaries[ticker]) for ticker in monitor_company_tickers}

# Create a structured array with summaries and sentiment information
def create_array(summaries, setiments, urls):
    array = []
    for ticker in monitor_company_tickers:
        for counter in range(len(summaries[ticker])):
            output = [
                ticker,
                summaries[ticker][counter],
                setiments[ticker][counter]['label'],
                setiments[ticker][counter]['score'],
                urls[ticker][counter]
            ]
            array.append(output)
    return array

# Create the final output array with headers
final_output = create_array(summaries, sentiments, clean_urls)
final_output.insert(0, ['Ticker', 'Summary', 'Sentiment', 'Confidence', 'URL'])

# Write the final output to a CSV file
with open('summaries2.csv', mode = 'w', newline = '') as f:
    csv_writer = csv.writer(f, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    csv_writer.writerows(final_output)

