import json
import hmac

import streamlit as st

from backend.tmdb import TMDB
from backend.json_boilerplate import json_converter, extract_keywords
from backend.utils import display_movies

MAX_RESULTS = [20]

MOVIE_PARAMS = {
    "include_adult": "false",
    "include_video": "false",
    "language": "en-US",
    "sort_by": "popularity.desc",
    "watch_region": "US",
}

WATCH_PROVIDERS = {
    "Netflix": 8,
    "Amazon Prime Video": 119,
    "Disney+": 337,
    "HBO Max": 384,
    "Apple TV": 2,
    "YouTube": 192,
}


def sidebar():
    st.sidebar.title("Filters")
    year_opts = ["Any"] + [str(i) for i in range(2024, 1969, -1)]
    year = st.sidebar.selectbox("Year", year_opts)
    min_runtime = st.sidebar.selectbox(
        "Minimum runtime", ["Any", "90 min", "120 min", "150 min"]
    )
    max_runtime = st.sidebar.selectbox(
        "Maximum runtime", ["Any", "90 min", "120 min", "150 min"]
    )
    with_watch_providers = st.sidebar.multiselect(
        "Streaming Platforms",
        sorted(WATCH_PROVIDERS.keys()),
    )
    MOVIE_PARAMS["vote_average.gte"] = st.sidebar.slider(
        "Minimum rating", 0.0, 10.0, 4.3
    )
    MAX_RESULTS[0] = st.sidebar.slider("Max results", 20, 100, 20)

    if year != "Any":
        MOVIE_PARAMS["primary_release_year"] = str(year)
    if min_runtime != "Any":
        MOVIE_PARAMS["with_runtime.gte"] = str(min_runtime)
    if max_runtime != "Any":
        MOVIE_PARAMS["with_runtime.lte"] = str(max_runtime)
    if with_watch_providers:
        MOVIE_PARAMS["with_watch_providers"] = "|".join(
            [str(WATCH_PROVIDERS[wp]) for wp in with_watch_providers]
        )


def get_prompt_params(input_prompt, tmdb: TMDB) -> tuple:
    with open("./backend/assets/genres.json") as f:
        genres = json.load(f)
    llm_params = json_converter(input_prompt, genres.keys())
    parsed_params = {}
    # st.write(movie_params)
    if llm_params is None:
        st.error("We could not generate keywords for your input. Please try again.")
        return (None, None)
    parsed_params["with_genres"] = "|".join(
        [
            str(genres[genre.strip()])
            for genre in llm_params["genres"]
            if genre.strip() in genres
        ]
    )
    sep = "," if llm_params["all_actors"] else "|"
    parsed_params["with_cast"] = sep.join(
        [tmdb.get_actor_id(actor.strip()) for actor in llm_params["actors"]]
    )
    keywords = extract_keywords(
        input_prompt,
        [tmdb.search_keyword(keyword) for keyword in llm_params["keywords"]],
    )
    if keywords is None:
        st.error("We could not extract keywords for your input. Please try again.")
        return (None, None)
    parsed_params["with_keywords"] = "|".join(
        [str(id) for id in keywords.values() if id]
    )
    return parsed_params, llm_params


def validate_params():
    if "with_runtime.gte" in MOVIE_PARAMS and "with_runtime.lte" in MOVIE_PARAMS:
        if int(MOVIE_PARAMS["with_runtime.gte"]) > int(
            MOVIE_PARAMS["with_runtime.lte"]
        ):
            st.error("Minimum runtime must be less than maximum runtime")
            return False
    return True


def header():
    # cols = st.columns(8)
    # mid = cols[3]
    # with mid:
    st.title(" FlickFinder")


def run():
    st.set_page_config(layout="wide", page_icon="./public/flickfinder.png")
    sidebar()
    header()

    st.header("Discover something new!")
    with st.form(key="my_form"):
        input_prompt = st.text_input(
            "Provide a description of what you want to watch:", ""
        )
        submit_button = st.form_submit_button(
            "Search", type="primary", use_container_width=True
        )

    if "movies" in st.session_state:
        if not submit_button:
            tmdb = TMDB(st.secrets["TMDB_API_KEY"])
            display_movies(st.session_state.movies, cols=6, tmdb=tmdb)

    if submit_button and validate_params():
        with st.spinner("Generating movie recommendations..."):
            tmdb = TMDB(st.secrets["TMDB_API_KEY"])
            prompt_params, llm_params = get_prompt_params(input_prompt, tmdb)
            MOVIE_PARAMS.update(prompt_params if prompt_params else {})

            movies = (
                tmdb.discover_movies(MOVIE_PARAMS, num_movies=MAX_RESULTS[0])
                if submit_button
                else st.session_state.movies
            )
            if len(movies) < 5:
                MOVIE_PARAMS.pop("with_keywords")
                movies = tmdb.discover_movies(MOVIE_PARAMS, num_movies=MAX_RESULTS[0])
            display_movies(movies, cols=6, tmdb=tmdb)
            st.session_state.movies = movies

            with st.expander("Attributes", expanded=False):
                st.write("Params returned from LLM:")
                st.write(llm_params)
                st.write("Params sent to TMDB API:")
                st.write(MOVIE_PARAMS)


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


run()
