import streamlit as st

from utils import create_temp_file, validate_input, num_tokens_from_string

from prompts import PROMPT_earnings, PROMPT_short

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
    selected_model = st.sidebar.selectbox(":blue[Select a model:]", list(model_names.keys()))

    # Display the description of the selected model
    st.sidebar.write("Model Description:")
    st.sidebar.markdown(model_names[selected_model])

    # Prompts with Descriptions
    prompt_description = {
        'short_default': 'Generic summary prompt. 100-150 word summary.',
        'earnings': 'Prompt for Earnings Call Transcripts. Focused on financial metrics.'
    }

    # Drop-down menu
    selected_prompt = st.sidebar.selectbox(":blue[Select a prompt:]", list(prompt_description.keys()))

    # Display the description of the selected model
    st.sidebar.write("Prompt Description:")
    st.sidebar.markdown(prompt_description[selected_prompt])

    # Prompts pointing to prompt object
    prompts = {
        'short_default': PROMPT_short,
        'earnings': PROMPT_earnings
    }

    uploaded_file = st.file_uploader(":blue[Upload a document to summarize]", type=['txt', 'pdf'])
    api_key = st.text_input(":blue[Enter API key here]")

    if st.button(":green[Summarize (click once and wait)] :coffee:"):
        process_summarize_button(uploaded_file, api_key, selected_model, prompts[selected_prompt])


def process_summarize_button(file, api_key, openai_model, prompt):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid

    :param file_or_transcript: The file uploaded by the user

    :param api_key: The API key entered by the user

    :param openai_model: The model selected by the user

    :param prompt: The selected prompt object

    :return: None
    """
    if not validate_input(file, api_key):
        return
    
    temp_filepath = create_temp_file (file)

    max_tokens = {
        'gpt-4-1106-preview': 7500,
        'gpt-4': 6000,
        'gpt-3.5-turbo-1106': 12000,
        'gpt-3.5-turbo': 2500,
        'gpt-3.5-turbo-16k': 12000   
    }

    with st.spinner("Summarizing... please wait..."):
        if file.type == 'application/pdf':
            st.write ("File is a PDF!")
            loader = PyPDFLoader(temp_filepath)
            transcript = loader.load()
        else:
            st.write ("File is a text!")
            loader = TextLoader(temp_filepath, encoding = 'UTF-8')
            transcript = loader.load()
        token_count = num_tokens_from_string(transcript[0].page_content,encoding_name='cl100k_base')
        st.write (f"{token_count} TOKENS!")

        if token_count < max_tokens[openai_model]:

            llm = ChatOpenAI(openai_api_key=api_key, model_name=openai_model)
            chain = load_summarize_chain(llm, 
                                         chain_type='stuff', 
                                         prompt=prompt)
            output_summary = chain.run(transcript)
            st.text_area(label='SUMMARY', value=output_summary, height=800)
        else:
            st.write ("Document is too large for selected model.  Choose another model.")

st.set_page_config(page_title="Doc Summarizer", page_icon="📹")
st.markdown("# :green[Doc Summarizer]")
st.sidebar.header(":green[Doc Summarizer]")

st.write(
    """This app allows you to upload pdf's or txt files and summarizes them using Chat-GPT."""
)

st.write(
    """Upload the document below and select the OpenAI model to do the summary.  Each model will have different capabilities and costs."""
)

doc_summarizer()

