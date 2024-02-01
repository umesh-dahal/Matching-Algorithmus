import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap

# Path to Data
file_path = r'C:\correlation measure.csv'

# Read CSV
data = pd.read_csv(file_path)

# Combine both occurrences of pairs once from x- and y- axis
combined_data = pd.concat([data, data.rename(columns={'First column name': 'Second column name', 'Second column name': 'First column name'})])

# Define correlation value ranges for creating different figure
ranges = [(0.6, 0.8), (0.4, 0.6), (0.2, 0.4), (0.0, 0.2)]

# Create subplots for each range with different sizes
fig, axes = plt.subplots(2, 2, figsize=[24, 20], gridspec_kw={'width_ratios': [1, 1.2]})

fig.suptitle('Korrelations-Heatmaps', fontsize=16)

for i, (lower, upper) in enumerate(ranges):
    # Filter data for the current range
    filtered_data = combined_data[(combined_data['Correlation value'] >= lower) & (combined_data['Correlation value'] < upper)]
    
    # Check if there are any correlations in the range
    if not filtered_data.empty:
        # Get unique attributes in the range
        unique_attributes = set(filtered_data['First column name'].unique()) | set(filtered_data['Second column name'].unique())
        
        # Create a subplot for each range
        ax = axes[i // 2, i % 2]
        
        # Customize color map to start from red
        cmap = sns.color_palette("Reds", as_cmap=True)
        
        # Map colors based on conditions
        color_map = sns.heatmap(filtered_data.pivot(index='First column name', columns='Second column name', values='Correlation value'),
                                annot=True, cmap=cmap, fmt=".2f", linewidths=.5,
                                vmin=filtered_data['Correlation value'].min(), vmax=filtered_data['Correlation value'].max(), 
                                cbar_kws={'label': 'Correlation'}, ax=ax)
        
        # Adjust x-axis and y-axis label font size
        ax.tick_params(axis='both', labelsize=8)
        
        # Wrap labels after every 10 characters
        ax.set_xticklabels([textwrap.fill(label.get_text(), 20) for label in ax.get_xticklabels()])
        ax.set_yticklabels([textwrap.fill(label.get_text(), 20) for label in ax.get_yticklabels()])
        
        ax.set_title(f'Correlation Range: {lower}-{upper}')

        # Remove attributes not present in the current range
        combined_data = combined_data[combined_data['First column name'].isin(unique_attributes) | combined_data['Second column name'].isin(unique_attributes)]

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the plot
plt.show()
