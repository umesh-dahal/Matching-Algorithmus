
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#Lese die Daten aus der CSV-Datei
file_path = r'C:\correlation_measure.csv'
data = pd.read_csv(file_path)

#Filtere die Daten basierend auf einer Korrelationsschwelle
threshold = 0.6
filtered_data = data[data['Correlation value'] > threshold]

#Erstelle ein leeres Netzwerk
G = nx.Graph()

#Füge Knoten (Variablen) hinzu
for index, row in filtered_data.iterrows():
    G.add_node(row['First column name'])
    G.add_node(row['Second column name'])

#Füge Kanten (Beziehungen) hinzu
for index, row in filtered_data.iterrows():
    correlation_value = row['Correlation value']
    if correlation_value > 0.6:
        color = 'green'
    elif correlation_value > 0.5:
        color = 'red'
    else:
        color = 'gray'
    G.add_edge(row['First column name'], row['Second column name'], weight=correlation_value, color=color)

#Zeige das Netzwerkdiagramm
pos = nx.spring_layout(G)  # Spring-Layout für die Positionierung der Knoten
edge_colors = [G[e[0]][e[1]]['color'] for e in G.edges()]
nx.draw(G, pos, with_labels=True, font_size=8, font_color='black', node_size=700, node_color='skyblue', font_weight='bold', edge_color=edge_colors, width=1, alpha=0.7)

#Füge Kantengewicht hinzu
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

plt.title("Korrelationsnetzwerk (Korrelation > 0.4, Rote Linien: Korrelation > 0.5, Grüne Linien: Korrelation > 0.6)")
plt.show()