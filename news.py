import requests

import pandas as pd


def create_excel_from_json(data, output_file):
    # Create DataFrame from new JSON data
    new_df = pd.DataFrame(data["articles"])

    try:
        # Try to read the existing Excel file
        existing_df = pd.read_excel(output_file)
        
        # Concatenate existing and new DataFrames and drop duplicates based on title and timestamp
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=["title", "timestamp"], keep="last")
    except FileNotFoundError:
        # If the Excel file doesn't exist, use only the new data
        combined_df = new_df

    # Reset index of combined DataFrame
    combined_df.reset_index(drop=True, inplace=True)

    # Write combined DataFrame to Excel file
    combined_df.to_excel(output_file, index=False)

def get_techcrunch_articles(tag_name):
    # Endpoint URL
    url = f"https://techcrunch.vercel.app/articles?tag={tag_name}"

    try:
        # Send GET request
        response = requests.get(url)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            return data
        else:
            # Print error message if request failed
            print(f"Failed to fetch articles: {response.text}")
            return None
    except Exception as e:
        # Print error message if an exception occurs
        print(f"An error occurred: {e}")
        return None

# Example usage:
topics = ["blockchain","serverless","ai","Data Science","Startup","fintech","LLM"]
for i in topics:
    tag_name = i
    articles = get_techcrunch_articles(tag_name)

    # Output file name
    output_file = "techcrunch_articles.xlsx"

    # Create Excel file from JSON data
    create_excel_from_json(articles, output_file)

print(f"Data has been saved to {output_file}")

# if articles:
#     print(articles['articles'][0]['description'])
    # print(articles)
