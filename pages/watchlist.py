import streamlit as st
from backend.tmdb import TMDB
from backend.utils import display_movies


def watchlist():
    st.set_page_config(layout="wide")
    st.title("My Watchlist")

    tmdb = TMDB(api_key=st.secrets["TMDB_API_KEY"])
    wlist = tmdb.get_watchlist()
    display_movies(wlist["results"])


watchlist()
