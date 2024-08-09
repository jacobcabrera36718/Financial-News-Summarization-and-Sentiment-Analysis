# Financial News Summarization and Sentiment Analysis

This project uses the Pegasus model from Hugging Face Transformers for summarizing financial news articles and a sentiment analysis pipeline to evaluate the sentiment of the summaries. It retrieves news articles related to specific stock tickers from the web, summarizes them, and assesses their sentiment.

## Installation

To run this project, you'll need to have Python installed along with the required libraries. You can install the necessary libraries using pip:

```bash
pip install transformers
pip install requests
pip install beautifulsoup4
pip install torch  # Required for Hugging Face Transformers
## Usage

The script retrieves and processes news articles for the following stock tickers: **TSLA**, **NVDA**, **META**, **AMZN**, and **GOOGL**.

### Steps

1. **Generate URLs for News Articles**: The script generates URLs for news articles related to the specified stock tickers.

2. **Clean URLs**: It filters and cleans the URLs to exclude unnecessary links.

3. **Scrape Articles**: The script scrapes the news articles from the cleaned URLs.

4. **Summarize Articles**: Using the Pegasus model, the script summarizes each article to provide concise information.

5. **Analyze Sentiment**: The sentiment analysis pipeline evaluates the sentiment of each summary.

6. **Export Results to CSV**: The final summaries and their sentiments are saved to a CSV file named `summaries2.csv`.

### Running the Script

To run the script, execute the following command:

```bash
python financial_summarization.py
