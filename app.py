import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import streamlit as st
from frontend.pages import home, recommend, history, compare


def main() -> None:
    st.set_page_config(page_title="AI-Based Multi-Cloud Dashboard", page_icon="☁️", layout="wide")

    st.sidebar.title("Multi-Cloud Platform")
    st.sidebar.write("AI-based recommendation and comparison system")
    st.sidebar.markdown("---")

    pages = {
        "Home": home,
        "Recommend": recommend,
        "History": history,
        "Compare": compare,
    }

    selection = st.sidebar.radio("Navigation", list(pages.keys()))
    st.sidebar.markdown("---")
    st.sidebar.write("Streamlit run app.py")

    page = pages[selection]
    page()


if __name__ == "__main__":
    main()
