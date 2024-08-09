#Financial News Summarization and Sentiment Analysis
This project uses the Pegasus model from Hugging Face Transformers for summarizing financial news articles and a sentiment analysis pipeline to evaluate the sentiment of the summaries. It retrieves news articles related to specific stock tickers from the web, summarizes them, and assesses their sentiment.

Installation
To run this project, you'll need to have Python installed along with the required libraries. You can install the necessary libraries using pip:

bash
Copy code
pip install transformers
pip install requests
pip install beautifulsoup4
pip install torch  # Required for Hugging Face Transformers
Usage
The script retrieves and processes news articles for the following stock tickers: TSLA, NVDA, META, AMZN, and GOOGL.

Steps
Generate URLs for News Articles: The script generates URLs for news articles related to the specified stock tickers.

Clean URLs: It filters and cleans the URLs to exclude unnecessary links.

Scrape Articles: The script scrapes the news articles from the cleaned URLs.

Summarize Articles: Using the Pegasus model, the script summarizes each article to provide concise information.

Analyze Sentiment: The sentiment analysis pipeline evaluates the sentiment of each summary.

Export Results to CSV: The final summaries and their sentiments are saved to a CSV file named summaries2.csv.

Running the Script
To run the script, execute the following command:

bash
Copy code
python financial_summarization.py
Ensure that you have an internet connection to allow the script to retrieve news articles and access pre-trained models.

Dependencies
Transformers: For using the Pegasus model for text summarization.
BeautifulSoup4: For web scraping the news articles.
Requests: For making HTTP requests to retrieve web pages.
Torch: Required for running the Hugging Face models.
Output
The output is a CSV file named summaries2.csv containing the following columns:

Ticker: The stock ticker symbol.
Summary: The summarized content of the news article.
Sentiment: The sentiment label (e.g., POSITIVE, NEGATIVE).
Confidence: The confidence score of the sentiment analysis.
URL: The URL of the original news article.
Notes
The script uses Google search to find news articles. Depending on your location and the time of search, the results may vary.
Ensure that you have the necessary permissions to scrape and process the data from the web.
