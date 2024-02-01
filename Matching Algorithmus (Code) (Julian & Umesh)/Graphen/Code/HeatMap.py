import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap

# path to data
file_path = r'C:\correlation measure.csv'

# Read csv
data = pd.read_csv(file_path)

# Identify symmetric pairs and double the rows for them so that it can plot value in both pair.
symmetric_pairs = data[data['First column name'] != data['Second column name']].copy()
symmetric_pairs[['First column name', 'Second column name']] = symmetric_pairs[['Second column name', 'First column name']]
data_doubled = pd.concat([data, symmetric_pairs], ignore_index=True)

# Heatmap erstellen
plt.figure(figsize=(12, 10))

# Customize color map to start from red
cmap = sns.color_palette("Reds", as_cmap=True)

# Wrap labels after 10 characters
data_doubled['First column name'] = data_doubled['First column name'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=20)))
data_doubled['Second column name'] = data_doubled['Second column name'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=20)))

# Map colors based on conditions
color_map = sns.heatmap(data_doubled.pivot(index='First column name', columns='Second column name', values='Correlation value'),
                        annot=True, cmap=cmap, fmt=".2f", linewidths=.5,
                        vmin=0.4, vmax=0.7, cbar_kws={'label': 'Correlation'})

plt.title('Korrelations-Heatmap')
plt.show()
