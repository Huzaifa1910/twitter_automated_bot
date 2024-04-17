#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 1.0.0 or higher.
import os
import pandas as pd
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()


# Read the Excel file
df = pd.read_excel("techcrunch_articles.xlsx")

client = AzureOpenAI(
  azure_endpoint = "https://hazdorhasan.openai.azure.com/", 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2024-02-15-preview"
)

num_rows = df.shape[0]
print(num_rows)

for index, row in df.iterrows():
    # if df.at[i, "summary"] == "nan" or df.at[i, "summary"] == None:
    if pd.isnull(row['summary']) or row['summary'] == "":
      print("NEW-------------------------------------------")

      message_text = [{"role":"system","content":"Providing you a blog i want you to write its summary for the post of twitter. Use easy and understandable english. Must keep it under 250 characters including Hashtags and cover the complete context."}]


      blog = {"role":"user","content":row["Desciption"]}
      # Get the description column of the first row

      # Update the corresponding cell in the DataFrame with the processed value

      message_text.append(blog)

      completion = client.chat.completions.create(
      model="gpt-4", # model = "deployment_name"
      messages = message_text,
      temperature=0.7,
      max_tokens=500,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
      )
      response = completion.choices[0].message.content
      df.at[index, 'summary'] = response

      # Write the updated DataFrame back to the Excel file
      df.to_excel("techcrunch_articles.xlsx", index=False)
      print(response)
      print("NEW-------------------------------------------")
    else:
       print("Already Summary")
       print(row["summary"])
      #  input("enter")