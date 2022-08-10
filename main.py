import requests
import databutton as db
import pandas as pd
import streamlit as st
# import spacy_streamlit
from utils import connect_to_db


@db.apps.streamlit("/livestream-nlp", name="Data from livestream")
def show_hackernews_data():
    # TODO for iteration 2 allow user to specific video id
    st.title("Livestream nlp from bloomberg video")

    # st link to dp8PhLsUcFE
    st.video("https://www.youtube.com/watch?v=loWxa5szbvU&ab_channel=FREENVESTING")
    old_df = db.storage.dataframes.get("livestream-nlp")
    st.dataframe(old_df)
    # spacy_streamlit visulization for last 3 text rows in old_df with column text
    # last_3_rows = "\n".join(old_df.tail(3)["text"])

    # spacy_streamlit.spacy_streamlit(last_3_rows)

# Every 5 minutes
@db.jobs.repeat_every(seconds=5*60, name="Check logs")
def fetch_hackernews_data():
    # find all results from dp8PhLsUcFE within the last day
    query = "SELECT * FROM dp8PhLsUcFE WHERE created_at > DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)"
    # Dont care about previous data
    new_df = pd.read_sql(query, con=connect_to_db())
    # Store the data
    db.storage.dataframes.put(new_df, "livestream-nlp")