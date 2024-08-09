# Financial News Summarization and Sentiment Analysis

This project uses the Pegasus model from Hugging Face Transformers for summarizing financial news articles and a sentiment analysis pipeline to evaluate the sentiment of the summaries. It retrieves news articles related to specific stock tickers from the web, summarizes them, and assesses their sentiment.

## Installation

To run this project, you'll need to have Python installed along with the required libraries. You can install the necessary libraries using pip:

```bash
pip install transformers
pip install requests
pip install beautifulsoup4
pip install torch  # Required for Hugging Face Transformers
```

## Usage

The script retrieves and processes news articles for the following stock tickers: **TSLA**, **NVDA**, **META**, **AMZN**, and **GOOGL**.

### Steps

1. **Generate URLs for News Articles**: The script generates URLs for news articles related to the specified stock tickers.

    ```python
    def stock_news_url(tickers):
        url_search = "https://www.google.com/search?q=investing.com&tbm=nws".format(tickers)
        request = requests.get(url_search)
        soup = BeautifulSoup(request.text, 'html.parser')
        tags = soup.find_all('a')
        href = [link['href'] for link in tags]
        return href

    raw_urls = {ticker: stock_news_url(ticker) for ticker in monitor_company_tickers}
    ```

2. **Clean URLs**: It filters and cleans the URLs to exclude unnecessary links.

    ```python
    exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support']

    def strip_url(urls, exclude_list):
        val = []
        for url in urls:
            if 'https://' in url and not any(exclude_word in url for exclude_word in exclude_list):
                res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
                val.append(res)
        return list(set(val))

    clean_urls = {ticker: strip_url(raw_urls[ticker], exclude_list) for ticker in monitor_company_tickers}
    ```

3. **Scrape Articles**: The script scrapes the news articles from the cleaned URLs.

    ```python
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

    url_articles = {ticker: scrape_url(clean_urls[ticker]) for ticker in monitor_company_tickers}
    ```

4. **Summarize Articles**: Using the Pegasus model, the script summarizes each article to provide concise information.

    ```python
    from transformers import PegasusTokenizer, PegasusForConditionalGeneration

    tokenizer = PegasusTokenizer.from_pretrained("human-centered-summarization/financial-summarization-pegasus")
    model = PegasusForConditionalGeneration.from_pretrained("human-centered-summarization/financial-summarization-pegasus")

    def summarize_url_article(url_articles):
        summarized_articles = []
        for article in url_articles:
            id_input = tokenizer.encode(article, return_tensors='pt')
            output = model.generate(id_input, max_length=100, num_beams=5, early_stopping=True)
            summary = tokenizer.decode(output[0], skip_special_tokens=True)
            summarized_articles.append(summary)
        return summarized_articles

    summaries = {ticker: summarize_url_article(url_articles[ticker]) for ticker in monitor_company_tickers}
    ```

5. **Analyze Sentiment**: The sentiment analysis pipeline evaluates the sentiment of each summary.

    ```python
    from transformers import pipeline

    sentiment = pipeline('sentiment-analysis')

    sentiments = {ticker: sentiment(summaries[ticker]) for ticker in monitor_company_tickers}
    ```

6. **Export Results to CSV**: The final summaries and their sentiments are saved to a CSV file named `summaries2.csv`.

    ```python
    import csv

    def create_array(summaries, sentiments, urls):
        array = []
        for ticker in monitor_company_tickers:
            for counter in range(len(summaries[ticker])):
                output = [
                    ticker,
                    summaries[ticker][counter],
                    sentiments[ticker][counter]['label'],
                    sentiments[ticker][counter]['score'],
                    urls[ticker][counter]
                ]
                array.append(output)
        return array

    final_out
