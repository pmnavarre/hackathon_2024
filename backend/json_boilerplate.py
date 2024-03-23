import json
import requests
import streamlit as st
import os
from openai import OpenAI


def json_converter(prompt: str) -> json:
    parameters = {
        "region": "",  # string
        "genres": "",
        "ending": "", # open or close 
        "overall mood": "", #sad, happy
    }
    # end_paramters = { 
    #     "with_keywords": "horror genres, resolved ending, sad overall mood"
    # }
    n = len(parameters.keys())

    prompt = f"Use this prompt to return at least {n} key words to use to get movie recommendations, at least one and at most three word for each of these categories: {parameters.keys()}. \
        For genres, reference existing genres in the TMDB API. For ending, return either 'cliffhanger' or 'resolved'. \
        If you are unsure about any of these categories based on the prompt, return None for all categories except genres. \
        Return the response in json." + prompt
    
    data = {'prompt': prompt, 
            'response': 'This is a response based on the prompt'}
    
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    

    client = OpenAI(
        # This is the default and can be omitted
        api_key=st.secrets["OPENAI_API_KEY"] 
    )

    # prompt = f"Given the following movie description: \"{json_file}\", provide the genre, target audience, and suggested rating."

    print("got here")
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
    print("Chat completion: ", chat_completion) 
    return json.loads(chat_completion.choices[0].message.content)

# res = json_converter("Say something funny please! Return the response in json.")
# print(res)