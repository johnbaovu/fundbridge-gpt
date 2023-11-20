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

    api_key = st.sidebar.text_input(":blue[Enter API key here]")

    uploaded_file = st.file_uploader(":blue[Upload a document to summarize]", type=['csv', 'txt', 'pdf'])


st.set_page_config(page_title="Chat with Doc", page_icon="📈")
st.markdown("# Chat with Doc")
st.sidebar.header("Chat with Doc")

st.write(
    """This app allows you to upload pdf's, csv, or txt files and allows you to ask questions about them."""
)

st.write(
    """Upload the document below and select the OpenAI model.  Each model will have different capabilities and costs."""
)

chat_with_doc()