import json
import requests
import os
from openai import OpenAI


def json_converter(prompt: str) -> json:
    prompt = " Use this prompt to return 3 key words, one for each of these categories\
        : genre, region, and year. If you are unsure about any of these categories based on the prompt, return None for the category. Return the response in json." + prompt
    data = {'prompt': prompt, 
            'response': 'This is a response based on the prompt'}
    
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY")
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
    return json.loads(chat_completion.choices[0].message.content)['response']


# res = json_converter("Say something funny please! Return the response in json.")
# print(res)