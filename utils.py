# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import shutil
import streamlit as st
import tiktoken

from langchain.chat_models import ChatOpenAI

from prompts import PROMPT_earnings, PROMPT_short

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def create_temp_file(uploaded_file):
    """
    Create a temporary file from an uploaded file.

    :param uploaded_file: The uploaded file to create a temporary file from.

    :return: The path to the temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.type.split('/')[1]}") as temp_file:
        # Write the contents of the uploaded file to the temporary file
        shutil.copyfileobj(uploaded_file, temp_file)
    return temp_file.name

def check_key_validity(api_key):
    """
    Check if an OpenAI API key is valid.

    :param api_key: The OpenAI API key to check.

    :return: True if the API key is valid, False otherwise.
    """
    try:
        ChatOpenAI(openai_api_key=api_key).call_as_llm('Hi')
        print('API Key is valid')
        return True
    except Exception as e:
        print('API key is invalid or OpenAI is having issues.')
        print(e)
        return False

def validate_input(file, api_key):
    """
    Validates the user input, and displays warnings if the input is invalid

    :param file: The file uploaded by the user

    :param api_key: The API key entered by the user

    :return: True if the input is valid, False otherwise
    """
    if file == None:
        st.warning("Please upload a file.")
        return False

    if not check_key_validity(api_key):
        st.warning('Key not valid or API is down.')
        return False

    return True

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

#decorator
def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):

        # to clear chat history after switching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_openai_api_key():
    openai_api_key = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        value=st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else '',
        placeholder="sk-..."
        )
    if openai_api_key:
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
        st.error("Please add your OpenAI API key to continue.")
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
        st.stop()
    return openai_api_key

def select_openai_model():
    # OpenAI models
    model_description = {
        'gpt-4-1106-preview': '10K context. The latest GPT-4 model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.',
        'gpt-4': '8K context. Snapshot of gpt-4 from June 13th 2023 with improved function calling support.',
        'gpt-3.5-turbo-1106': '16K context. The latest GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.',
        'gpt-3.5-turbo': '4K context. Snapshot of gpt-3.5-turbo from June 13th 2023.',
        'gpt-3.5-turbo-16k': '16K context. Snapshot of gpt-3.5-16k-turbo from June 13th 2023.'
    }
    # Drop-down menu
    selected_model = st.sidebar.selectbox(":blue[Select a model:]", list(model_description.keys()))

    # Display the description of the selected model
    st.sidebar.write("Model Description:")
    st.sidebar.markdown(model_description[selected_model])
    return selected_model

def select_prompt():    
    prompt_description = {
        'short_default': 'Generic summary prompt. 100-150 word summary.',
        'earnings': 'Prompt for Earnings Call Transcripts. Focused on financial metrics.'
        }
        
    # Drop-down menu
    selected_prompt = st.selectbox(":blue[Select a prompt:]", list(prompt_description.keys()))
    # Display the description of the selected model
    st.markdown(prompt_description[selected_prompt])
    # Prompts pointing to prompt object
    prompts = {
        'short_default': PROMPT_short,
        'earnings': PROMPT_earnings
        }   
    return prompts[selected_prompt]