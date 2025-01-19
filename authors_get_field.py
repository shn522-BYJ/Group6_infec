import pandas as pd

# Load the classified articles and relevant authors
articles_with_field_path = 'data/relevant_articles_with_field.csv'
relevant_authors_path = 'data/relevant_authors.csv'

articles_df = pd.read_csv(articles_with_field_path)
authors_df = pd.read_csv(relevant_authors_path)

# Ensure columns exist
if "PMID" not in articles_df.columns or "Field" not in articles_df.columns:
    raise KeyError("The 'relevant_articles_with_field.csv' must contain 'PMID' and 'Field' columns.")
if "PMID" not in authors_df.columns or "AuthorForename" not in authors_df.columns or "AuthorLastname" not in authors_df.columns:
    raise KeyError("The 'relevant_authors.csv' must contain 'PMID', 'AuthorForename', and 'AuthorLastname' columns.")

# Merge authors with article fields using PMID
authors_with_field_df = pd.merge(authors_df, articles_df[['PMID', 'Field']], on='PMID', how='left')

# Save the resulting DataFrame to a new CSV file
output_path = 'data/relevant_authors_with_field.csv'
authors_with_field_df.to_csv(output_path, index=False)

# Inform the user
print(f"Relevant authors with fields saved to: {output_path}")
