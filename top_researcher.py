import os
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Create 'output' folder if it doesn't exist
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Load the author dataset
authors_path = "data/relevant_authors_with_field.csv"
authors_df = pd.read_csv(authors_path)

# Ensure necessary columns exist
required_columns = ["PMID", "Field", "AuthorForename", "AuthorLastname"]
if not all(col in authors_df.columns for col in required_columns):
    raise KeyError(f"Missing one or more required columns: {required_columns}")

# Create a full name column for authors
authors_df["FullName"] = authors_df["AuthorForename"] + " " + authors_df["AuthorLastname"]

# Build the co-authorship network
G = nx.Graph()

# Group by fields and construct networks
for pmid, group in authors_df.groupby("PMID"):
    authors = group["FullName"].tolist()
    for i, author1 in enumerate(authors):
        for author2 in authors[i + 1:]:
            if G.has_edge(author1, author2):
                G[author1][author2]["weight"] += 1
            else:
                G.add_edge(author1, author2, weight=1)

# Calculate centrality metrics
betweenness_centrality = nx.betweenness_centrality(G, weight="weight", endpoints=True)
degree_centrality = nx.degree_centrality(G)

# Save centrality metrics as a CSV file
metrics_df = pd.DataFrame({
    "Author": list(degree_centrality.keys()),
    "Degree Centrality": list(degree_centrality.values()),
    "Betweenness Centrality": list(betweenness_centrality.values())
})
metrics_output_path = os.path.join(output_folder, "author_centrality_metrics.csv")
metrics_df.to_csv(metrics_output_path, index=False)
print(f"Centrality metrics saved to: {metrics_output_path}")

# Prepare data for visualization
pos = nx.spring_layout(G, k=0.15, seed=42)
node_x = []
node_y = []
node_size = []
node_color = []
node_text = []
edge_x = []
edge_y = []

for node in G.nodes:
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_size.append(degree_centrality[node] * 1000)  # Scale for visibility
    node_color.append(betweenness_centrality[node])
    node_text.append(f"{node}<br>Degree Centrality: {degree_centrality[node]:.4f}<br>"
                     f"Betweenness Centrality: {betweenness_centrality[node]:.4f}")

for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_y.append(y0)
    edge_x.append(x1)
    edge_y.append(y1)
    edge_x.append(None)  # Line breaks for edges

# Create the Plotly visualization
edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color="gray"),
    hoverinfo="none",
    mode="lines"
)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    hoverinfo="text",
    marker=dict(
        showscale=True,
        colorscale="Viridis",
        color=node_color,
        size=node_size,
        colorbar=dict(
            thickness=15,
            title="Betweenness Centrality",
            xanchor="left",
            titleside="right"
        )
    ),
    text=node_text
)

# Create layout and display the graph
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="Interactive Author Activity Network",
                    titlefont_size=16,
                    showlegend=False,
                    hovermode="closest",
                    margin=dict(b=0, l=0, r=0, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)
                ))

# Save the interactive visualization as an HTML file
visualization_output_path = os.path.join(output_folder, "author_network_visualization.html")
fig.write_html(visualization_output_path)
print(f"Interactive visualization saved to: {visualization_output_path}")