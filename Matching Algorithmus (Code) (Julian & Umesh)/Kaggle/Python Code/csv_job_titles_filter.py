import pandas as pd

# Read the CSV file
df = pd.read_csv(r'C:\test.csv')

# Delete rows without "IT" in job title
df = df[df['industry'].str.contains('IT', case=False)]

# Delete text after symbol
df['job title'] = df['job title'].str.replace(r'[-;,/x(.*', '', regex=True)

# Delete the "industry" column
df = df.drop('industry', axis=1)

# Delete duplicate items
df = df.drop_duplicates()

# Write the filtered DataFrame to a new CSV file
df.to_csv('filtered_file.csv', index=False)

# Create a string with every item in "job title" column enclosed in double quotes and separated by a comma
titles_string = ', '.join(f'"{title}"' for title in df['job title'])

# Save the titles string in a text file
with open('titles.txt', 'w') as f:
    f.write(titles_string)
