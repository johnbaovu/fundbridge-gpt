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

from typing import Any

import os
import streamlit as st
import tempfile
import shutil

from utils import create_temp_file, validate_input, num_tokens_from_string

from prompts import PROMPT_earnings

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.chains.summarize import load_summarize_chain

def doc_summarizer() -> None:

    # OpenAI models
    model_names = {
        'gpt-4-1106-preview': '10K context. The latest GPT-4 model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.',
        'gpt-4': '8K context. Snapshot of gpt-4 from June 13th 2023 with improved function calling support.',
        'gpt-3.5-turbo-1106': '16K context. The latest GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.',
        'gpt-3.5-turbo': '4K context. Snapshot of gpt-3.5-turbo from June 13th 2023.',
        'gpt-3.5-turbo-16k': '16K context. Snapshot of gpt-3.5-16k-turbo from June 13th 2023.'
    }
    # Drop-down menu
    selected_model = st.sidebar.selectbox('Select a model:', list(model_names.keys()))

    # Display the description of the selected model
    st.sidebar.write('Model Description:')
    st.sidebar.markdown(model_names[selected_model])

    uploaded_file = st.file_uploader("Upload a document to summarize", type=['txt', 'pdf'])
    api_key = st.text_input("Enter API key here")

    if st.button('Summarize (click once and wait)'):
        process_summarize_button(uploaded_file, api_key, selected_model)


def process_summarize_button(file, api_key, openai_model):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid

    :param file_or_transcript: The file uploaded by the user

    :param api_key: The API key entered by the user

    :param openai_model: The model selected by the user

    :return: None
    """
    if not validate_input(file, api_key):
        return
    
    temp_filepath = create_temp_file (file)

    with st.spinner("Summarizing... please wait..."):
        if file.type == 'application/pdf':
            st.markdown ("File is a PDF!")
            loader = PyPDFLoader(temp_filepath)
            transcript = loader.load_and_split()
        else:
            st.markdown ("File is a text!")
            loader = TextLoader(temp_filepath, encoding = 'UTF-8')
            transcript = loader.load()
        token_count = num_tokens_from_string(transcript,encoding_name='cl100k_base')
        st.markdown(f"{token_count} TOKENS!")

        llm = ChatOpenAI(openai_api_key=api_key, model_name=openai_model)
        chain = load_summarize_chain(llm, 
                             chain_type="stuff", 
                             prompt=PROMPT_earnings)
        
        output_summary = chain.run(transcript)
        st.markdown(output_summary)

st.set_page_config(page_title="Doc Summarizer", page_icon="📹")
st.markdown("# Animation Demo")
st.sidebar.header("Doc Summarizer")
st.write(
    """This app allows you to upload pdf's or txt files and summarizes them using Chat-GPT."""
)

st.write(
    """Upload the document below and select the OpenAI model to do the summary.  Each model will have different capabilities and costs."""
)

doc_summarizer()

