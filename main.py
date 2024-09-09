import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def app(llm: Chain, portfolio):
    st.title('Generate Cold Email Using AI')
    url = st.text_input(label="Enter the link to career page...", label_visibility="visible")
    submit_button = st.button("Submit")
    if submit_button:
        try:
            loader = WebBaseLoader([url])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.get_query(str(skills))
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.write(e)

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    app(chain, portfolio)