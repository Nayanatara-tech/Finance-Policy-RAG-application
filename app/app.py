
import streamlit as st
from rag_backend import retrieve_finance_context, generate_finance_answer


st.set_page_config(
    page_title="Finance Policy Assistant",
    page_icon="💼"
)

st.title("💼 Finance Policy Assistant")

st.write(
    "Ask questions about finance policies and retrieve "
    "the most relevant policy information."
)

question = st.text_input(
    "Ask a finance policy question",
    placeholder="What are the criteria for recognizing revenue?"
)

if st.button("Ask Finance Policy Assistant"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching policies and generating answer..."):

            try:

                # Step 1: Retrieve relevant policy chunks
                context, sources = retrieve_finance_context(question)

                # Step 2: Generate grounded answer
                answer = generate_finance_answer(
                    question,
                    context
                )

                st.subheader("Answer")
                st.write(answer)

                st.subheader("Source Documents")

                for source in dict.fromkeys(sources):
                    st.write(f"📄 {source}")

            except Exception as e:

                st.error(f"Error: {e}")