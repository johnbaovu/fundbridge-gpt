import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)   


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to FundBridge-GPT! 👋")

    st.sidebar.success("Select a page above.")

    st.markdown(
        """
        This is the starting page for FundBridge's internal website for using AI within our network.

        **👈 Select a page from the sidebar to start**
    """
    )


if __name__ == "__main__":
    run()
