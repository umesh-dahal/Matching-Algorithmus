from linkedin_scraper import actions, Person
from selenium import webdriver
from urllib import request
from bs4 import BeautifulSoup
import csv

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# LinkedIn login credentials
email = "your username"
password = "your password"

# Define the maximum number of login attempts and the login timeout in seconds
max_login_attempts = 1

# Create a list to store all LinkedIn links
all_linkedin_links = []

# Take user input for the "web" part in the query
web_query = input("Enter the 'web' part for the LinkedIn search: ")

# Number of pages to scrape
num_pages = 3

# LinkedIn login (made only once)
try:
    actions.login(driver, email, password)
except Exception as e:
    print(f"Login failed: {e}")
    driver.quit()
    exit()

# Iterate through the pages
for page in range(0, num_pages * 10, 10):
    # Construct the search URL with pagination
    url = f"https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2FAND+%22{web_query}%22AND%22Germany%22&start={page}"

    # Create a request object and add the User-Agent header
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})

    # Use the request object to open the URL
    response = request.urlopen(req)

    # Read the HTML content
    html_content = response.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract and append links containing "linkedin.com/in/" starting with "https" but excluding 'maps.google' and 'translate'
    linkedin_links = [link.get('href') for link in soup.find_all('a') if 'linkedin.com/in/' in str(link.get('href')) and str(link.get('href')).startswith('https') and 'maps.google' not in str(link.get('href')) and 'translate' not in str(link.get('href')) and 'google' not in str(link.get('href'))]

    # Append the links to the list
    all_linkedin_links.extend(linkedin_links)

# Print the array of all LinkedIn links
print(all_linkedin_links)

# LinkedIn login and profile extraction
for linkedin_link in all_linkedin_links:
    try:
        # Visit the LinkedIn profile
        person = Person(linkedin_link, driver=driver, close_on_complete=False)

        # Extract information and save to CSV
        experiences_string = ";".join([f"{exp.institution_name} {exp.position_title} {exp.duration}" for exp in person.experiences])
        educations_string = ";".join([f"{edu.institution_name} {edu.degree}" for edu in person.educations])

        with open("names.csv", mode='a', newline='') as csvfile:
            fieldnames = ["name", "about", "educations", "experiences"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({"name": person.name, "about": person.about, "educations": educations_string, "experiences": experiences_string})

        print(f"Data for {person.name} has been saved to names.csv")
    except Exception as e:
        print(f"Error processing {linkedin_link}: {e}")

# Close the WebDriver
driver.quit()