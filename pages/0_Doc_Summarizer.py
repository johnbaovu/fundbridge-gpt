import streamlit as st

import utils
from utils import create_temp_file, num_tokens_from_string, select_prompt

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.chains.summarize import load_summarize_chain

st.set_page_config(page_title="Doc Summarizer", page_icon="📹")
st.markdown("# :green[Doc Summarizer]")
st.write(
    """This app allows you to upload pdf's or txt files and summarizes them using Chat-GPT."""
)
st.write(
    """Upload the document below, input your OpenAI key and select the OpenAI model to do the summary.  Each model will have different capabilities and costs."""
)

class DocSummarizer:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = utils.select_openai_model()        
    
    def main(self):
        uploaded_file = st.file_uploader(":blue[Upload a document to summarize]", type=['txt', 'pdf'])
        max_tokens = {
            'gpt-4-1106-preview': 7500,
            'gpt-4': 6000,
            'gpt-3.5-turbo-1106': 12000,
            'gpt-3.5-turbo': 2500,
            'gpt-3.5-turbo-16k': 12000   
        }
        st.write (max_tokens[self.openai_model])
        prompt = select_prompt()

        if st.button(":green[Summarize (click once and wait)] :coffee:"):
            with st.spinner("Summarizing... please wait..."):
                temp_filepath = create_temp_file (uploaded_file)
                if uploaded_file.type == 'application/pdf':
                    st.write ("File is a PDF!")
                    loader = PyPDFLoader(temp_filepath)
                    transcript = loader.load()
                else:
                    st.write ("File is a text!")
                    loader = TextLoader(temp_filepath, encoding = 'UTF-8')
                    transcript = loader.load()
                token_count = num_tokens_from_string(transcript[0].page_content,encoding_name='cl100k_base')
                st.write (f"This document contains {token_count} TOKENS!")

                if token_count < max_tokens[self.openai_model]:
                    llm = ChatOpenAI(model_name=self.openai_model)
                    chain = load_summarize_chain(llm, chain_type='stuff', prompt=prompt)
                    output_summary = chain.run(transcript)
                    st.text_area(label='SUMMARY', value=output_summary, height=800)
                else:
                    st.write ("Document is too large for selected model!  Choose another model.")

if __name__ == "__main__":
    obj = DocSummarizer()
    obj.main()

