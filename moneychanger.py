from typing import Tuple, Dict
import os
from dotenv import load_dotenv
import json
import requests
import streamlit as st
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

load_dotenv()
EXCHANGERATE_API_KEY=os.getenv('EXCHANGERATE_API_KEY')



def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url=f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    response = json.loads(requests.get(url).text)

    return (base,target,amount,f'{response["conversion_result"]:.2f}')


def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
            #tools=tools,
        )
    
    except Exception as e:
        print(f"Exception {e} for {text}")
    else:
        return response.choices[0].message.content

def run_pipeline():
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    if True: #tool_calls
        # Update this
        st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}')

    elif True: #tools not used
        # Update this
        st.write(f"(Function calling not used) and response from the model")
    else:
        st.write("NotImplemented")

# Set the title of the app
st.title('Multilingual Money Changer')

# Create a text input box
user_input = st.text_input("Enter your amount of currency:")

# Create a submit button
if st.button('Submit'):
    # Print the contents of the text box below the text box
    st.write(call_llm(user_input))