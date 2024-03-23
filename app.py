import streamlit as st
import backend.tmdb
from backend.json_boilerplate import json_converter

MOVIE_PARAMS = {
    "include_adult": "false",
    "include_video": "false",
    "language": "en-US",
    "page": "1",
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
    MOVIE_PARAMS["vote_average.gte"] = st.sidebar.slider(
        "Minimum rating", 0.0, 10.0, 7.5
    )
    with_watch_providers = st.sidebar.multiselect(
        "Streaming Platforms",
        sorted(["Netflix", "Amazon Video", "Disney+", "Hulu", "Apple TV"]),
    )

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


def validate_params():
    if "with_runtime.gte" in MOVIE_PARAMS and "with_runtime.lte" in MOVIE_PARAMS:
        if int(MOVIE_PARAMS["with_runtime.gte"]) > int(
            MOVIE_PARAMS["with_runtime.lte"]
        ):
            st.error("Minimum runtime must be less than maximum runtime")
            return False
    return True


def run():
    st.set_page_config(layout="wide")
    st.title("Movie Recommendation System")
    # page = st.session_state.get("page", "Main Page")

    sidebar()

    st.header("Discover something new!")
    with st.form(key="my_form"):
        input_prompt = st.text_input(
            "Provide a description of what you want to watch:", ""
        )
        submit_button = st.form_submit_button("Submit")

    if submit_button and validate_params():
        st.write(
            f"Generating keywords for movie recommendations based on: {input_prompt}"
        )
        movie_params = json_converter(input_prompt)
        st.write(movie_params)

        tmdb = backend.tmdb.TMDB(st.secrets["TMDB_API_KEY"])
        # movie_params["primary_release_year"] = input_prompt.split(" ")[0]

        # with st.spinner("Finding movies..."):
        movies = tmdb.discover_movies(MOVIE_PARAMS, num_movies=50)
        # movies = tmdb.discover_movies(movie_params, num_movies=50)
        display_movies(movies, cols=6)
        st.toast("We found some movies for you!", icon="😍")
        # st.write(f"You submitted: {input_prompt}")


def display_movies(movies, cols=4, width=150):
    for i in range(0, len(movies), cols):
        for col, movie in zip(st.columns(cols), movies[i : i + cols]):
            with col:
                image_domain = "https://image.tmdb.org/t/p/w200"
                image_url = f"{image_domain}/{movie['poster_path']}"
                st.image(image_url, width=width, caption=movie["title"])
            # if col.button(
            #     "![Image]",
            #     key="-".join(movie["title"]),
            #     help="Click to show info for Image 2",
            # ):
            #     pass


if __name__ == "__main__":
    run()
