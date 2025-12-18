# app.py
import streamlit as st
import json

from ocr_azure import ocr_pdf_bytes
from answer_key import ANSWER_KEY
from grade import grade_script

# You need to implement this for your answer sheet format:
# from parser import parse_answers_from_text

def parse_answers_from_text(ocr_text: str) -> dict:
    """
    TEMP: stub that you must implement to map OCR text
    to {question_id: answer_text}, e.g.:
      {"1.1": "They lack intermolecular spaces", ...}
    For now, you can reuse whatever parsing logic you already built.
    """
    # TODO: replace with your real parser
    return {}


st.set_page_config(page_title="AI School Grader", layout="wide")
st.title("AI School Grader (Chemistry – Class 7)")

st.write("Upload the **question paper** and a **student answer sheet** to evaluate.")

col1, col2 = st.columns(2)
with col1:
    qp_file = st.file_uploader("Question paper PDF", type=["pdf"], key="qp")
with col2:
    ans_file = st.file_uploader("Answer sheet PDF", type=["pdf"], key="ans")

if st.button("Evaluate Answer Sheet"):
    if not qp_file or not ans_file:
        st.error("Please upload both the question paper and the answer sheet.")
    else:
        # 1. OCR question paper (optional – shown only for reference)
        qp_text = ocr_pdf_bytes(qp_file.read())

        with st.expander("Question paper OCR (for reference)"):
            st.text(qp_text)

        # 2. OCR answer sheet
        ans_text = ocr_pdf_bytes(ans_file.read())

        with st.expander("Answer sheet OCR (raw)"):
            st.text(ans_text)

        # 3. Parse student's answers into {question_id: answer}
        student_answers = parse_answers_from_text(ans_text)

        with st.expander("Parsed answers by question ID"):
            st.json(student_answers)

        # 4. Grade using fixed answer_key + grade.py
        report = grade_script(student_answers)

        st.subheader("Overall Result")
        st.metric("Score", f"{report['total']} / {report['max_total']}")
        st.metric("Percentage", f"{report['percentage']:.1f}%")
        st.metric("Grade", report["grade"])

        st.subheader("Detailed Evaluation")
        for q in report["questions"]:
            with st.expander(f"Q {q['id']} – {q['score']}/{q['max_marks']}"):
                st.write(f"**Question:** {q['text']}")
                st.write(f"**Student Answer:** {q['student_answer']}")
                st.write(f"**Feedback:** {q['feedback']}")
