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

import streamlit as st

from utils import create_temp_file, validate_input, num_tokens_from_string

from prompts import PROMPT_earnings, PROMPT_short

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.chains.summarize import load_summarize_chain

def chat_with_doc():

    # OpenAI models
    model_names = {
        'gpt-4-1106-preview': '10K context. The latest GPT-4 model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.',
        'gpt-4': '8K context. Snapshot of gpt-4 from June 13th 2023 with improved function calling support.',
        'gpt-3.5-turbo-1106': '16K context. The latest GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.',
        'gpt-3.5-turbo': '4K context. Snapshot of gpt-3.5-turbo from June 13th 2023.',
        'gpt-3.5-turbo-16k': '16K context. Snapshot of gpt-3.5-16k-turbo from June 13th 2023.'
    }
    # Drop-down menu
    selected_model = st.sidebar.selectbox(":blue[Select a model:]", list(model_names.keys()))

    # Display the description of the selected model
    st.sidebar.write("Model Description:")
    st.sidebar.markdown(model_names[selected_model])


st.set_page_config(page_title="Chat with Doc", page_icon="📈")
st.markdown("# Chat with Doc")
st.sidebar.header("Chat with Doc")

