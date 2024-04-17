import bot
import json
import os
import pandas as pd
import time

twitter = bot.make_token()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token_url = "https://api.twitter.com/2/oauth2/token"

with open("token.json", "r") as token:
    data = json.load(token)
print(data)
df = pd.read_excel("techcrunch_articles.xlsx")

refreshed_token = twitter.refresh_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    refresh_token=data["refresh_token"],
    # headers=haeders
)
print(refreshed_token)
with open("token.json", "w") as file:
        json.dump(refreshed_token, file)
x = df.shape[0]
for i in range(x):
    # time.sleep(120)
    print(df.iloc[i]["summary"])
    post = df.iloc[i]["summary"].split('.')
    link = df.iloc[i]["link"]
    post.append(f"Source: {link}")
    print(post)
    # time.sleep(10)
    if df.iloc[i]["is_posted"] == 0:
        post_ids = []
        for j in range(len(post)):
            if j == 0:
                print(j)
                payload = {"text": "{}".format(post[j])}
                b = bot.post_tweet(payload, refreshed_token)
                data = b.json()
                id = data['data']['id']
                post_ids.append(id)
                time.sleep(10)
                df.at[i, 'is_posted'] = 1
                df.at[i, 'post_id'] = id
            else:
                payload = {"text": "{}".format(post[j]),"reply": {"in_reply_to_tweet_id": id}}
                m = bot.post_tweet(payload, refreshed_token)
                m = m.json()
                id = m['data']['id']
                post_ids.append(id)
                time.sleep(5)


              
    # doggie_fact = bot.parse_dog_fact()
    # payload = df.iloc[i]["summary"]
    # bot.post_tweet(payload, refreshed_token)

    df.to_excel("techcrunch_articles.xlsx", index=False)

    time.sleep(220)
    # if(x==3):
      
