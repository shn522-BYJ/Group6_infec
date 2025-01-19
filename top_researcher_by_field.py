import pandas as pd
import networkx as nx
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load data
authors_with_field_path = 'data/relevant_authors_with_field.csv'
authors_df = pd.read_csv(authors_with_field_path)

# Ensure necessary columns exist
required_columns = ["PMID", "Field", "AuthorForename", "AuthorLastname"]
if not all(col in authors_df.columns for col in required_columns):
    raise KeyError(f"Missing one or more required columns: {required_columns}")

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Group articles by fields
fields = authors_df["Field"].unique()

# Initialize a dictionary to store metrics for each field
field_scholar_metrics = {}

# Process each field
for field in fields:
    # Filter authors for the current field
    field_authors = authors_df[authors_df["Field"] == field]

    # Build a co-authorship network
    G = nx.Graph()
    for pmid, group in field_authors.groupby("PMID"):
        authors = group["AuthorForename"] + " " + group["AuthorLastname"]
        authors = authors.tolist()
        for i, author1 in enumerate(authors):
            for author2 in authors[i + 1:]:
                if G.has_edge(author1, author2):
                    G[author1][author2]["weight"] += 1
                else:
                    G.add_edge(author1, author2, weight=1)

    # Calculate centrality metrics
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    # Store metrics in a DataFrame
    metrics_df = pd.DataFrame({
        "Author": list(degree_centrality.keys()),
        "Degree Centrality": list(degree_centrality.values()),
        "Betweenness Centrality": list(betweenness_centrality.values())
    })

    # Rank scholars by degree centrality
    metrics_df.sort_values(by="Degree Centrality", ascending=False, inplace=True)

    # Save the metrics for the current field
    metrics_output_path = os.path.join(output_dir, f"{field.replace(' ', '_').lower()}_scholar_metrics.csv")
    metrics_df.to_csv(metrics_output_path, index=False)
    print(f"Metrics for {field} saved to: {metrics_output_path}")

    # Store for tabular summary
    field_scholar_metrics[field] = metrics_df

    # Visualize the top 10 scholars in this field
    top_authors = metrics_df.head(10)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Formatter to display percentages
    percent_formatter = FuncFormatter(lambda x, _: f"{x * 100:.1f}%")

    # Bar chart for Degree Centrality
    ax1.bar(top_authors["Author"], top_authors["Degree Centrality"], color="blue", alpha=0.6, label="Degree Centrality")
    ax1.set_xlabel("Author", fontsize=12)
    ax1.set_ylabel("Degree Centrality", color="blue", fontsize=12)
    ax1.tick_params(axis="x", rotation=45, labelsize=10)
    ax1.tick_params(axis="y", labelcolor="blue", labelsize=10)
    ax1.yaxis.set_major_formatter(percent_formatter)  # Format y-axis as percentages

    # Line chart for Betweenness Centrality
    ax2 = ax1.twinx()
    ax2.plot(top_authors["Author"], top_authors["Betweenness Centrality"], color="red", marker="o", label="Betweenness Centrality")
    ax2.set_ylabel("Betweenness Centrality", color="red", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="red", labelsize=10)
    ax2.yaxis.set_major_formatter(percent_formatter)  # Format y-axis as percentages

    # Title and legend
    plt.title(f"Top 10 Scholars in {field} by Centrality Metrics", fontsize=14)
    fig.tight_layout()
    plt.legend(loc="upper left")

    # Save visualization
    visualization_output_path = os.path.join(output_dir, f"{field.replace(' ', '_').lower()}_centrality_chart.png")
    plt.savefig(visualization_output_path, dpi=300)
    plt.close()
    print(f"Visualization for {field} saved to: {visualization_output_path}")

# Combine summaries for all fields
summary_df = pd.concat(field_scholar_metrics, names=["Field"])
summary_output_path = os.path.join(output_dir, "scholar_summary_by_field.csv")
summary_df.to_csv(summary_output_path, index=False)

print(f"Summary of top scholars by field saved to: {summary_output_path}")