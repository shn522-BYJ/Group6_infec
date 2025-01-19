import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Load relevant authors data
relevant_authors_path = "data/relevant_authors.csv"
relevant_authors = pd.read_csv(relevant_authors_path)

# Build the co-authorship network
G = nx.Graph()

# Group by PMID and create edges for co-authors
for pmid, group in relevant_authors.groupby('PMID'):
    authors = group['AuthorForename'] + " " + group['AuthorLastname']
    authors = authors.tolist()
    for i, author1 in enumerate(authors):
        for author2 in authors[i + 1:]:
            if G.has_edge(author1, author2):
                G[author1][author2]['weight'] += 1
            else:
                G.add_edge(author1, author2, weight=1)

# Calculate degree centrality
degree_centrality = nx.degree_centrality(G)

# Create the visualization
pos = nx.spring_layout(G, k=0.15, seed=42)  # Position nodes with spring layout
node_sizes = [1000 * degree_centrality[node] for node in G.nodes()]
node_colors = [degree_centrality[node] for node in G.nodes()]

# Build Plotly graph
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
node_text = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(f"{node} (Degree: {degree_centrality[node]:.2f})")

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=node_text,
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=node_sizes,
        color=node_colors,
        colorbar=dict(
            thickness=15,
            title='Degree Centrality',
            xanchor='left',
            titleside='right'
        )
    )
)

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Co-authorship Network',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False),
                    paper_bgcolor='white'  # Set white background
                ))

# Save and show the graph
fig.write_html("output/coauthorship_network_interactive.html")
fig.show()

