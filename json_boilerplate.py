import json
import requests
import os
from openai import OpenAI


def json_converter(prompt: str) -> json:
    data = {'prompt': prompt, 
            'response': 'This is a response based on the prompt'}
    
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY")
    )



    # prompt = f"Given the following movie description: \"{json_file}\", provide the genre, target audience, and suggested rating."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-0125",
        response_format={"type": "json_object"}
    )
    return json.loads(chat_completion.choices[0].message.content)['response']


res = json_converter("Say something funny please! Return the response in json.")
print(res)