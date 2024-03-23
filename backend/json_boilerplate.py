import json
import requests
import streamlit as st
import os
from openai import OpenAI


def json_converter(prompt: str) -> json:
    parameters = {
        "region": "",  # string
        "genres": "",
        "ending": "", 
        "overall mood": ""
        # "with_keywords": ""
    }
    # end_paramters = { 
    #     "with_keywords": "horror genres, resolved ending, sad overall mood"
    # }
    n = len(parameters.keys())

    prompt = f"I want to generate keywords for the given categories of movie-related information into JSON format. \
        Your goal is to a JSON object containing a sentence consists of at least one word for each of these categories: {parameters.keys()}. \
        For example, for genres, return the sentence horror, action. They must be comma separated and referenced from the existing genres in the TMDB API. \
        For overall mood, should be one word response. For ending, return either cliffhanger ending or resolved ending if given a related keyword or none. \
        If you are unsure about any of these categories based on the prompt, return None for all categories except genres.\
        Return the response in json." + prompt
    # For with_keywords, reference existing genres in the TMDB API. \

    data = {'prompt': prompt, 
            'response': 'This is a response based on the prompt'}

    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    

    client = OpenAI(
        # This is the default and can be omitted
        api_key=st.secrets["OPENAI_API_KEY"] 
    )

    # prompt = f"Given the following movie description: \"{json_file}\", provide the genre, target audience, and suggested rating."

    # print("got here")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"}
    )

    json_params = json.loads(chat_completion.choices[0].message.content)
    final_params, with_keywords = {}, ""

    for json_param in json_params.keys(): 
        if json_param not in ['region', 'genres']:
            with_keywords += json_params[json_param] + ", "

        else: 
            final_params[json_param] = json_params[json_param]
    final_params["with_keywords"] = with_keywords[:-2]

    return final_params

# res = json_converter("Say something funny please! Return the response in json.")
# print(res)