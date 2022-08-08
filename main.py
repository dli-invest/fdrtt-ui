import requests
import databutton as db
import pandas as pd
import streamlit as st


@db.apps.streamlit("/hackernews-data", name="Data from hackernews")
def show_hackernews_data():
    st.title("Hackernews data")
    st.dataframe(db.storage.dataframes.get("hackernews-data"))



# Every 30 seconds
@db.jobs.repeat_every(seconds=30, name="Check hackernews")
def fetch_hackernews_data():
    # Fetch newest post ids from HN
    response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
    ids = response.json()

    # Get the actual posts
    posts = [
        requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json?print=pretty"
        ).json()
        # Only get data for the latest 3
        for post_id in ids[:3]
    ]

    # Get the current list of posts
    # dataframes.get(key) will return an empty dataframe if the key does not exist
    # If you want to handle this as an exception (FileNotFoundError), pass ignore_not_found=False
    current = db.storage.dataframes.get("hackernews-data")
    if len(current) == 0:
        new_posts = posts
    else:
        new_posts = [
            post for post in posts if len(current.loc[current["id"] == post["id"]]) == 0
        ]
    df = pd.DataFrame.from_records(new_posts)

    # Add the new posts
    new_df = pd.concat([current, df], ignore_index=True)

    # Store the data
    db.storage.dataframes.put(new_df, "hackernews-data")
    print(f"Created {len(new_posts)} records")