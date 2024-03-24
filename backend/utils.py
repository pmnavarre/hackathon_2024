import streamlit as st


def display_movies(movies, cols=6, width=150, tmdb=None):
    for i in range(0, len(movies), cols):
        for col, movie in zip(st.columns(cols), movies[i : i + cols]):
            with col:
                image_domain = "https://image.tmdb.org/t/p/w200"
                image_url = (
                    f"{image_domain}/{movie['poster_path']}"
                    if movie["poster_path"]
                    else "./public/blank.png"
                )
                st.image(image_url, width=width, caption=movie["title"])
                if tmdb and col.button(
                    "Add to Watchlist",
                    key=f"{'-'.join(movie['title'])}-{str(i)}",
                    help="Click to add to watchlist",
                ):
                    tmdb.add_to_watchlist(movie["id"])
                    st.toast("Added to watchlist!", icon="🎥")
                    # st.write(movie)
                    # st.write(f"Rating: {movie['vote_average']}")
