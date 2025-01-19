import pandas as pd
from collections import defaultdict
import string

# Load the data from a CSV file
file_path = 'data/relevant_articles.csv'
articles_df = pd.read_csv(file_path)

# Check and correct column names
print("Columns in DataFrame:", articles_df.columns)

# Rename columns to remove extra spaces and standardize
articles_df.rename(columns=lambda x: x.strip(), inplace=True)

# Ensure the required columns exist
if "Title" not in articles_df.columns or "Abstract" not in articles_df.columns:
    raise KeyError("The DataFrame must contain 'Title' and 'Abstract' columns.")

# Define academic fields and associated keywords
fields_keywords = {
    "Medical Sciences": ["infection", "hospitalised", "hospitalized", "circulating", "treatment", "disease"],
    "Epidemiology and Public Health": ["epidemiology", "public health", "population", "spread", "incidence", "prevalence"],
    "Parasitology and Tropical Medicine": ["schistosoma", "parasite", "parasitology", "tropical medicine"],
    "Immunology": ["antigen", "immune", "immunology", "immune response", "antigenic"],
    "Biological and Biomedical Research": ["nitric oxide", "biomedical", "biology", "cellular", "biochemistry"]
}

# Stopwords list (can be extended as needed)
stopwords = set(["and", "or", "the", "of", "in", "to", "a", "with", "on", "for", "is", "as", "by", "at", "an"])

# Function to extract unique keywords from text
def extract_keywords(text):
    # Remove punctuation, tokenize, and filter stopwords
    if pd.isnull(text):
        return set()
    words = text.translate(str.maketrans("", "", string.punctuation)).lower().split()
    return set(word for word in words if word not in stopwords)

# Extract unique keywords from all titles and abstracts
all_keywords = set()
for _, row in articles_df.iterrows():
    all_keywords.update(extract_keywords(row["Title"]))
    all_keywords.update(extract_keywords(row["Abstract"]))

# Map unique keywords to fields
keyword_field_mapping = defaultdict(list)
for keyword in all_keywords:
    for field, keywords in fields_keywords.items():
        if keyword in keywords:
            keyword_field_mapping[keyword].append(field)

# Resolve overlaps by selecting the first field or marking ambiguous keywords
resolved_keyword_mapping = {}
for keyword, fields in keyword_field_mapping.items():
    if len(fields) == 1:
        resolved_keyword_mapping[keyword] = fields[0]
    else:
        resolved_keyword_mapping[keyword] = "Ambiguous"  # Mark ambiguous keywords for review

# Save the non-repetitive keyword library to a CSV file
keyword_library_df = pd.DataFrame(list(resolved_keyword_mapping.items()), columns=["Keyword", "Field"])
keyword_library_output_path = 'data/articles_field.csv'
keyword_library_df.to_csv(keyword_library_output_path, index=False)

# Function to classify articles based on keyword frequency
def classify_article_by_frequency(title, abstract):
    combined_text = f"{title} {abstract}".lower() if not pd.isnull(title) and not pd.isnull(abstract) else ""
    field_counts = defaultdict(int)
    
    for field, keywords in fields_keywords.items():
        for keyword in keywords:
            field_counts[field] += combined_text.count(keyword.lower())
    
    # Return the field with the highest count, or "Other" if all counts are zero
    if field_counts:
        return max(field_counts, key=field_counts.get)
    return "Other"

# Apply classification to each article
articles_df["Field"] = articles_df.apply(lambda row: classify_article_by_frequency(row["Title"], row["Abstract"]), axis=1)

# Count the number of articles in each field
field_counts = articles_df["Field"].value_counts()

# Print the field counts
print("\nNumber of articles in each field:")
for field, count in field_counts.items():
    print(f"- {field}: {count} articles")

# Save the classified articles to a new CSV file
classified_articles_output_path = 'data/relevant_articles_with_field.csv'
articles_df.to_csv(classified_articles_output_path, index=False)

print(f"\nNon-repetitive keyword library saved to: {keyword_library_output_path}")
print(f"Classified articles saved to: {classified_articles_output_path}")