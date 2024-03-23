import streamlit as st
import backend.tmdb
import time

# Title of the main page
st.set_page_config(layout="wide")
st.title("Movie Recommendation System")


images = [
    "https://image.tmdb.org/t/p/w200/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg" for _ in range(10)
]


def display_movies(movies, cols=4, width=150):
    for i in range(0, len(movies), cols):
        for col, movie in zip(st.columns(cols), movies[i : i + cols]):
            with col:
                image_domain = "https://image.tmdb.org/t/p/w200"
                image_url = f"{image_domain}/{movie['poster_path']}"
                st.image(image_url, width=width, caption=movie["title"])
            if col.button(
                "![Image]",
                key="-".join(movie["title"]),
                help="Click to show info for Image 2",
            ):
                pass


# # Sidebar for navigation
# with st.sidebar:
#     st.title("Navigation")
#     if st.button("Main Page"):
#         st.session_state["page"] = "Main Page"
#     if st.button("Other Page"):
#         st.session_state["page"] = "Other Page"

page = st.session_state.get("page", "Main Page")

movie_params = {
    "include_adult": "false",
    "include_video": "false",
    "language": "en-US",
    "page": "1",
    "sort_by": "popularity.desc",
}


# def char_generator(input_str):
#     """A generator function that yields each character of the input string."""
#     for char in input_str:
#         yield char
#         time.sleep(0.1)
#
#
if page == "Main Page":
    st.header("Welcome to the Main Page")
    # st.write_stream(char_generator("Discover something new!"))
    with st.form(key="my_form"):
        input_prompt = st.text_input("Enter something:", "")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        tmdb = backend.tmdb.TMDB(st.secrets["TMDB_API_KEY"])
        movie_params["primary_release_year"] = input_prompt.split(" ")[0]
        movies = tmdb.discover_movies(movie_params)
        display_movies(movies["results"], cols=6)
        st.write(f"You submitted: {input_prompt}")

elif page == "Other Page":
    st.write(
        "This is another page. You can add different widgets or functionalities here."
    )
