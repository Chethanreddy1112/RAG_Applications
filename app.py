import streamlit as st

from rag_api import ask

st.title("Bank of America Credit Card RAG")

question=st.text_input("Ask")

if st.button("Search"):

    answer,docs=ask(question)

    st.write(answer)

    st.subheader("Sources")

    for d in docs:
        st.write("Card:", d.metadata.get("card_name"))
        st.write("Category:", d.metadata.get("category"))
        st.write("Source:", d.metadata.get("source"))
        st.write("---")