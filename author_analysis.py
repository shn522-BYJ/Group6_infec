import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# File paths for authors and articles data
authors_path = "data/relevant_authors_with_field.csv"
articles_path = "data/relevant_articles_final.csv"

# Load data
authors_df = pd.read_csv(authors_path)
articles_df = pd.read_csv(articles_path)

# Define the authors
authors_list = [
    {'forename': 'David', 'lastname': 'Rollinson'},
    {'forename': 'Donald P', 'lastname': 'McManus'},
    {'forename': 'Xiao-Nong', 'lastname': 'Zhou'},
    {'forename': 'Jürg', 'lastname': 'Utzinger'}
]

# Define the save path for the plots
save_path = r"F:/python_environment/Group6/results_with_trend_lines"

# Ensure the save directory exists
if not os.path.exists(save_path):
    os.makedirs(save_path)

def plot_author_articles_with_trend(author_forename, author_lastname):
    """
    Generate a scatter plot with a trend line for an author's articles and their SJR over time.
    """
    # Find the author's articles and their SJR
    author_articles = authors_df[
        (authors_df['AuthorForename'] == author_forename) & 
        (authors_df['AuthorLastname'] == author_lastname)
    ][['PMID', 'SJR']]
    
    if author_articles.empty:
        print(f"{author_forename} {author_lastname} not found in the authors data.")
        return
    
    # Get article years
    article_years = articles_df[articles_df['PMID'].isin(author_articles['PMID'])][['PMID', 'Year']]
    
    # Merge years and SJR data
    article_details = pd.merge(author_articles, article_years, on='PMID', how='inner')
    
    # Scatter plot includes all points, even extremes
    plt.figure(figsize=(10, 6))
    plt.scatter(article_details['Year'], article_details['SJR'], color='blue', alpha=0.7, label='Data Points')
    
    # Filter extreme SJR values for trend line calculation (e.g., SJR > 0 and SJR < 10)
    filtered_details = article_details[(article_details['SJR'] > 0) & (article_details['SJR'] < 10)]
    
    if not filtered_details.empty:
        # Calculate and plot trend line
        z = np.polyfit(filtered_details['Year'], filtered_details['SJR'], 1)
        p = np.poly1d(z)
        plt.plot(filtered_details['Year'], p(filtered_details['Year']), color='red', linestyle='--', label='Trend Line')
    
    # Plot formatting
    plt.title(f'{author_forename} {author_lastname} Articles: SJR vs Year')
    plt.xlabel('Year')
    plt.ylabel('SJR')
    plt.grid(True)
    plt.legend()
    
    # Save the plot
    filename = f"{author_forename}_{author_lastname}_articles_with_trend.png"
    save_full_path = os.path.join(save_path, filename)
    plt.savefig(save_full_path)
    plt.close()

def calculate_average_author_rank(author_forename, author_lastname):
    """
    Calculate the average author rank for a given author.
    """
    # Find the author's articles and their ranks
    author_articles = authors_df[
        (authors_df['AuthorForename'] == author_forename) & 
        (authors_df['AuthorLastname'] == author_lastname)
    ]
    
    if author_articles.empty:
        print(f"{author_forename} {author_lastname} not found in the authors data.")
        return None
    
    # Calculate the average rank
    average_rank = author_articles['AuthorN'].mean()
    return average_rank

# Generate scatter plots with trend lines for each author
for author in authors_list:
    plot_author_articles_with_trend(author['forename'], author['lastname'])

# Calculate and print the average author rank for each author
for author in authors_list:
    average_rank = calculate_average_author_rank(author['forename'], author['lastname'])
    if average_rank is not None:
        print(f"Average author rank for {author['forename']} {author['lastname']}: {average_rank:.2f}")