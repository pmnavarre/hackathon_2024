import json
import streamlit as st
from openai import OpenAI
from typing import Union


def invoke_openai(prompt: str) -> Union[dict, None]:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        # model="gpt-4-0125-preview",
        response_format={"type": "json_object"},
    )

    if chat_completion.choices[0].message.content is None:
        return None
    return json.loads(chat_completion.choices[0].message.content)


def json_converter(input: str, genres: list) -> Union[dict, None]:
    parameters = {
        # "region": "",  # string
        "genres": [],
        # "ending": "",
        # "overall mood": "",
        "keywords": [],
        "actors": [],
        "all_actors": False,
        # "with_keywords": ""
    }

    # 3/ For ending, return either cliffhanger ending or resolved ending if given a related keyword or none.
    prompt = f"""You are a data scientist working on a movie recommendation system. Your task is to generate keywords for movie recommendations based on the given prompt. The keywords should be in JSON format (specifically as {parameters.keys()}). Always return a list for each category, even if it is empty.

    Please make sure you complete the objective above with the following rules:
    1/ For genres, return the relevant genres from the list {genres}. They must be comma separated and capitalized.
    2/ For keywords, this should be a short list of words describing the overall mood. 
    3/ For actors, only return the name of an actor if it specifically mentioned in the prompt. If the prompt requires all of the actors to be in the same movie, set the all_actors flag to True. Otherwise, if the prompt does not require all of the actors to be in the same movie, set the all_actors flag to False.

    If you are unsure about any category based on the prompt, return None for that category. The prompt is:\n\n{input}"""
    return invoke_openai(prompt)


def extract_keywords(input: str, keywords: list) -> Union[dict, None]:
    prompt = f"""You are a data scientist working on a movie recommendation system. Your task is to determine keywords for movie recommendations based on the given prompt. You should return a JSON dictionary of the ids (in the form "keyword": "id") associated with only the relevant keywords to the prompt. Do not include any irrelevant keywords. Only return the top 2-3 keywords if there are more than 3.

    The prompt is: {input}

    The dictionary of keywords and ids is as follows: {keywords}
        """
    return invoke_openai(prompt)
