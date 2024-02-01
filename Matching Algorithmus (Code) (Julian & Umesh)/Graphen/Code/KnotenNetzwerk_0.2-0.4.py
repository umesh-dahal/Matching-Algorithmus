import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Lese die Daten aus der CSV-Datei
file_path = r'C:\correlation_measure.csv'
data = pd.read_csv(file_path)

# Filtere die Daten basierend auf einer Korrelationsschwelle
lower_threshold = 0.2
upper_threshold = 0.4
filtered_data = data[(data['Correlation value'] >= lower_threshold) & (data['Correlation value'] <= upper_threshold)]

# Erstelle ein leeres Netzwerk
G = nx.Graph()

# Füge Knoten (Variablen) hinzu
for index, row in filtered_data.iterrows():
    G.add_node(row['First column name'])
    G.add_node(row['Second column name'])

# Füge Kanten (Beziehungen) hinzu
for index, row in filtered_data.iterrows():
    correlation_value = round(row['Correlation value'], 2)
    if correlation_value > 0.3:
        color = 'green'
    else:
        color = 'red'
    G.add_edge(row['First column name'], row['Second column name'], weight=correlation_value, color=color)

# Zeige das Netzwerkdiagramm mit breiterem Layout und adjusted parameters
pos = nx.spring_layout(G, k=0.2)  # Adjust the 'k' parameter for wider layout
node_size = 300  # Adjust the node size
font_size = 6  # Adjust the font size
edge_colors = [G[e[0]][e[1]]['color'] for e in G.edges()]

nx.draw(G, pos, with_labels=True, font_size=font_size, font_color='black',
        node_size=node_size, node_color='skyblue', font_weight='bold',
        edge_color=edge_colors, width=1, alpha=0.7)

# Füge Kantengewicht hinzu
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

plt.title("Korrelationsnetzwerk (0.2 <= Korrelation <= 0.4, Grüne Linien: Korrelation > 0.3)")
plt.show()
