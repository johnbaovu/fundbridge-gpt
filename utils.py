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

import tempfile
import shutil
import streamlit as st
import tiktoken

from langchain.chat_models import ChatOpenAI

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