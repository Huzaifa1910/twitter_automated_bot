import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_and_update_excel(input_file, url_column, description_column):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Get the URL from the specified column
        url = row[url_column]
        print(url)
        # Check if the description cell is empty
        if pd.isnull(row[description_column]) or row[description_column] == "":
            # Send a GET request to the URL
            response = requests.get(url)
            print("empty cell")
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content of the webpage
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the elements containing the data you want to scrape
                # Example: extracting the content of all articles with class 'article-content'
                article_content = soup.find(class_='article-content')

                # Get the description (text content)
                description = article_content.get_text(strip=True) if article_content else ""

                # Update the corresponding cell in the DataFrame
                df.at[index, description_column] = description

            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status_code}")

    # Write the updated DataFrame back to the Excel file
    df.to_excel(input_file, index=False)

# Example usage:
input_file = "techcrunch_articles.xlsx"  # Your input Excel file
url_column = "link"  # Column containing the URLs
description_column = "Desciption"  # Column where descriptions will be stored

# Call the function to scrape each URL and update the Excel file
scrape_and_update_excel(input_file, url_column, description_column)
