import requests
import databutton as db
import pandas as pd
import streamlit as st
import spacy_streamlit
from utils import connect_to_db


DEFAULT_MODEL = "en_core_web_sm"
# DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines**"""


@db.apps.streamlit("/livestream-nlp", name="Data from livestream")
def show_livestream_nlp():
    option = st.selectbox(
     'What livestream do you want to use?',
     ("test", "dp8PhLsUcFE",))
    # TODO for iteration 2 allow user to specific video id
    st.title(f"Livestream nlp for {option}")
    # st link to dp8PhLsUcFE
    st.markdown("https://www.youtube.com/watch?v=dp8PhLsUcFE")
    old_df = db.storage.dataframes.get("livestream-nlp")
    st.dataframe(old_df)
    # spacy_streamlit visulization for last 3 text rows in old_df with column text
    last_3_rows = "\n".join(old_df.head(3)["text"])
    spacy_streamlit.visualize(
        [DEFAULT_MODEL],
        default_model=DEFAULT_MODEL,
        visualizers=["ner"],
        # show_visualizer_select=True,
        # sidebar_description=DESCRIPTION,
        default_text=last_3_rows,
        show_json_doc=False,
        show_meta=False,
        show_config=False,
        # show_logo = False,
    )

# Every 5 minutes


@db.jobs.repeat_every(seconds=5*60, name="Check mysql")
def fetch_sql_data():
    # find all results from dp8PhLsUcFE within the last day
    query = "SELECT * FROM dp8PhLsUcFE WHERE created_at > DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY) ORDER BY created_at DESC"
    # Dont care about previous data
    new_df = pd.read_sql(query, con=connect_to_db())
    # Store the data
    db.storage.dataframes.put(new_df, "livestream-nlp")
