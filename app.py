import streamlit as st

# st.write("""
# # My first app
# Hello *world!*
# """)

# Title of the main page
st.title("My Streamlit App")

# Sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    if st.button("Main Page"):
        st.session_state["page"] = "Main Page"
    if st.button("Other Page"):
        st.session_state["page"] = "Other Page"

page = st.session_state.get("page", "Main Page")

# Main page layout
if page == "Main Page":
    st.header("Welcome to the Main Page")
    input_prompt = st.text_input("Enter something:", "")
    submit_button = st.button("Submit")

    if submit_button:
        st.write(f"You submitted: {input_prompt}")

# Placeholder for other page functionality
elif page == "Other Page":
    st.write(
        "This is another page. You can add different widgets or functionalities here."
    )
