import streamlit as st

import utils
from utils import create_temp_file, num_tokens_from_string, select_prompt

from streaming import StreamHandler

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import faiss
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

st.set_page_config(page_title="Chat with Large Doc", page_icon="📈")
st.markdown("# Chat with ComplianceBot")

st.write(
    """This app allows you to chat with a Large Doc, which is larger than the context window."""
)

st.write(
    """Input your OpenAI key and select the OpenAI model.  Each model will have different capabilities and costs."""
)

class CustomDataChatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = utils.select_openai_model()   

    @st.spinner('Loading knowledge base documents..')
    def setup_qa_chain(self, uploaded_files):
        # Load documents
        docs = []
        for file in uploaded_files:
            file_path = create_temp_file (file)
            if file.type == 'application/pdf':
                st.write ("File is a PDF!")
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
            else:
                st.write ("File is a text!")
                loader = TextLoader(file_path, encoding = 'UTF-8')
                docs.extend(loader.load())
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            separators=["\n", "\n\n", "(?<=\. )", "", " "]
        )
        splits = text_splitter.split_documents(docs)

        # Create embeddings and store in vectordb
        db = faiss.FAISS.from_documents (docs, OpenAIEmbeddings())

        # Define retriever
        retriever = db.as_retriever(
            search_type='mmr',
            search_kwargs={'k':2, 'fetch_k':4}
        )

        # Setup memory for contextual conversation        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )

        # Setup LLM and QA chain
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0, streaming=True)
        qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory, verbose=True)
        return qa_chain

    @utils.enable_chat_history
    def main(self):

        # User Inputs
        uploaded_files = st.file_uploader(label='Upload PDF or text files', type=['pdf','txt'], accept_multiple_files=True)
        if not uploaded_files:
            st.error("Please upload documents to continue!")
            st.stop()

        user_query = st.chat_input(placeholder="Ask me anything!")

        if uploaded_files and user_query:
            qa_chain = self.setup_qa_chain(uploaded_files)

            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                response = qa_chain.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    obj = CustomDataChatbot()
    obj.main()