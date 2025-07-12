import streamlit as st
from document_utils import extract_text_from_file
from qa_engine import QASystem

st.set_page_config(page_title="Smart Research Assistant", layout="centered")
st.title("📄 Smart Document Assistant")
st.write("Upload a PDF or TXT file to begin.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    with st.spinner("Extracting text..."):
        document_text = extract_text_from_file(uploaded_file)

    if document_text:
        st.session_state.document_text = document_text
        st.subheader("📄 Extracted Text Preview")
        st.text_area("Text from document:", document_text[:1000] + "...", height=300)

        st.subheader("📝 Summary (Preview)")
        st.write("This is a short summary of the uploaded document:")
        st.write(document_text[:150] + "...")

        if "qa_system" not in st.session_state:
            st.session_state.qa_system = QASystem(document_text)

        st.subheader("🤖 Ask Anything")
        question = st.text_input("Ask a question based on the document")

        if question:
            with st.spinner("Searching and answering..."):
                answer, source = st.session_state.qa_system.get_answer(question)
                st.markdown(f"**Answer:** {answer}")
                with st.expander("🔍 View source snippet"):
                    st.write(source)

        st.subheader("🧠 Challenge Me")

        if st.button("Generate Challenge Questions"):
            with st.spinner("Creating questions..."):
                questions = st.session_state.qa_system.generate_questions()
                st.session_state.user_answers = [""] * len(questions)

        if "user_answers" in st.session_state and st.session_state.qa_system.questions:
            for i, question in enumerate(st.session_state.qa_system.questions):
                st.markdown(f"**Q{i+1}: {question}**")
                user_input = st.text_input(f"Your Answer to Q{i+1}", key=f"answer_{i}")
                st.session_state.user_answers[i] = user_input

            if st.button("Submit Answers"):
                st.subheader("📋 Evaluation")
                for i, user_ans in enumerate(st.session_state.user_answers):
                    if user_ans.strip():
                        with st.spinner(f"Evaluating Q{i+1}..."):
                            predicted_ans, justification = st.session_state.qa_system.get_answer(
                                st.session_state.qa_system.questions[i]
                            )
                            st.markdown(f"**Q{i+1} Evaluation:**")
                            st.markdown(f"- **Your Answer:** {user_ans}")
                            st.markdown(f"- **Expected Answer:** {predicted_ans}")
                            st.markdown(f"- **Feedback:** {'✅ Correct-ish' if user_ans.lower() in predicted_ans.lower() else '❌ Needs Review'}")
                            st.markdown(f"- 📚 Justification: {justification}")
    else:
        st.error("Could not extract text from the file.")