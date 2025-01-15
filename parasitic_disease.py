import pandas as pd
import numpy as np
import re

articles_path = 'data/articles.schistosomiasis.csv'
authors_path = 'data/authors.schistosomiasis.csv'

articles = pd.read_csv(articles_path)
authors = pd.read_csv(authors_path)

def normalize_text(text):
    """Normalize text by removing brackets, special characters, and trimming whitespace."""
    if pd.isnull(text):  # Handle missing data
        return ""
    # Remove brackets, special characters, and strip whitespace
    return re.sub(r'[\[\](){}]', '', text).strip().lower()

def contains_keywords(text, keywords):
    """Check if any keyword is present in the given text as a whole word."""
    text_normalized = normalize_text(text)
    # Use regex to ensure keywords are matched as whole words
    return any(re.search(rf'\b{re.escape(keyword)}\b', text_normalized) for keyword in keywords)

def filter_articles(articles_df, keywords, sample_size=5):
    """
    Filter articles based on keywords in titles and abstracts.
    Randomly sample non-relevant articles for manual review.

    Args:
        articles_df (pd.DataFrame): DataFrame containing article metadata.
        keywords (list): List of keywords to check for relevance.
        sample_size (int): Number of non-relevant articles to sample.

    Returns:
        relevant_articles (pd.DataFrame): Articles marked as relevant.
        non_relevant_sample (pd.DataFrame): Random sample of non-relevant articles.
        discarded_articles (pd.DataFrame): All non-relevant articles in original format.
    """
    # Apply keyword detection to Title and Abstract fields
    articles_df['Relevant'] = articles_df['Title'].apply(lambda x: contains_keywords(x, keywords)) | \
                              articles_df['Abstract'].apply(lambda x: contains_keywords(x, keywords))

    # Separate relevant and non-relevant articles
    relevant_articles = articles_df[articles_df['Relevant']]
    non_relevant_articles = articles_df[~articles_df['Relevant']]

    # Randomly sample non-relevant articles for manual review
    non_relevant_sample = non_relevant_articles.sample(n=min(sample_size, len(non_relevant_articles)), random_state=42)

    return relevant_articles, non_relevant_sample, non_relevant_articles

# Define relevant keywords
keywords = ["schistosomiasis", "schistosoma", "parasitic disease", "schistosomal",
    "japonicum", "oncomelania", "cercariae", "molluscicide", "bilharzia", "schistosome", "antischistosomal", "schistosomes", "molluscicidal", "snail control"]

# Filter articles and sample non-relevant ones
relevant_articles, non_relevant_sample, discarded_articles = filter_articles(articles, keywords, sample_size=5)

# Save the relevant articles and discarded articles
relevant_articles.to_csv('data/relevant_articles.csv', index=False)
discarded_articles.to_csv('data/discarded_articles.csv', index=False)

# Print sample of non-relevant articles for manual review
print("Sample of non-relevant articles for manual review:")
print(non_relevant_sample[['PMID', 'Abstract']])
