
import streamlit as st
from resume_parser import extract_text
from question_generator import generate_questions
from feedback_generator import evaluate_answer

st.set_page_config(
    page_title="ZPrep AI",
    layout="wide"
)

st.title("ZPrep AI")
st.subheader("AI Powered Interview Preparation")

st.markdown("---")

st.write("""
Upload your resume and get personalized:

- HR Questions
- Technical Questions
- Project Questions
""")

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = None

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Generate Questions"):

        with st.spinner("Analyzing Resume..."):

            resume_text = extract_text("temp_resume.pdf")

            questions = generate_questions(resume_text)

            st.session_state.questions = questions

        st.success("Questions Generated!")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["HR", "Technical", "Projects", "Mock Interview"]
)

# HR TAB
with tab1:

    st.header("HR Questions")

    if st.session_state.questions:

        for q in st.session_state.questions["hr"]:
            st.info(q)

    else:
        st.info("Generate questions first.")

# TECHNICAL TAB
with tab2:

    st.header("Technical Questions")

    if st.session_state.questions:

        for q in st.session_state.questions["technical"]:
            st.info(q)

    else:
        st.info("Generate questions first.")

# PROJECT TAB
with tab3:

    st.header("Project Questions")

    if st.session_state.questions:

        for q in st.session_state.questions["projects"]:
            st.info(q)

    else:
        st.info("Generate questions first.")

# MOCK INTERVIEW TAB
with tab4:

    st.header("Mock Interview")

    if st.session_state.questions:

        all_questions = (
            st.session_state.questions["hr"]
            + st.session_state.questions["technical"]
            + st.session_state.questions["projects"]
        )

        selected_question = st.selectbox(
            "Choose a Question",
            all_questions
        )

        answer = st.text_area(
            "Your Answer"
        )

        if st.button("Evaluate Answer"):

            if answer:

                with st.spinner("Evaluating Answer..."):

                    feedback = evaluate_answer(
                        selected_question,
                        answer
                    )

                st.success("Evaluation Complete")

                st.markdown(feedback)

            else:
                st.warning("Please enter an answer.")

    else:
        st.info("Generate questions first.")
