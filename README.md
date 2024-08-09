# Financial News Summarization and Sentiment Analysis

This project uses the Pegasus model from Hugging Face Transformers for summarizing financial news articles and a sentiment analysis pipeline to evaluate the sentiment of the summaries. It retrieves news articles related to specific stock tickers from the web, summarizes them, and assesses their sentiment.

## Installation

To run this project, you'll need to have Python installed along with the required libraries. You can install the necessary libraries using pip:

```bash
pip install transformers
pip install requests
pip install beautifulsoup4
pip install torch  # Required for Hugging Face Transformers
