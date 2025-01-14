

# Load datasets
import pandas as pd
articles_data = pd.read_csv("data/articles.schistosomiasis.csv")
# Added encoding='latin-1' to handle the different file encoding
authors_data = pd.read_csv("data/authors.schistosomiasis.csv")
paper_counts = pd.read_csv("data/paper_counts.csv")

articles_data

# Check for missing values
print(articles_data.isnull().sum())

# Define keywords for the biological target
keywords = ['parasitic disease', 'schistosomiasis']

# Filter papers where title or abstract mentions the biological target
filtered_articles = articles_data[
    articles_data['Title'].str.contains('|'.join(keywords), case=False, na=False) |
    articles_data['Abstract'].str.contains('|'.join(keywords), case=False, na=False)
]
filtered_articles

authors_data

# Check for missing values
print(authors_data.isnull().sum())

# Filter authors based on selected PMIDs
relevant_authors = authors_data[authors_data['PMID'].isin(filtered_articles['PMID'])]
relevant_authors.to_csv('filtered_authors.csv', index=False)

filtered_authors = pd.read_csv("/content/filtered_authors.csv")
filtered_authors

paper_counts

# Check for missing values
print(paper_counts.isnull().sum())