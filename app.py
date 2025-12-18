import streamlit as st
import json
from ocr_azure import ocr_pdf_bytes
from llm_groq import extract_marking_scheme, extract_student_answers
from grade import grade_script

st.set_page_config(page_title="AI School Grader", layout="wide")
st.title("AI School Grader")

qp_file = st.file_uploader("Question paper PDF", type=["pdf"], key="qp")
ans_file = st.file_uploader("Answer sheet PDF", type=["pdf"], key="ans")

if st.button("Evaluate Answer Sheet"):
    if not qp_file or not ans_file:
        st.error("Please upload both PDFs.")
    else:
        # 1. Build marking scheme from QP (OR load from cached JSON)
        qp_text = ocr_pdf_bytes(qp_file.read())
        scheme = extract_marking_scheme(qp_text)   # <- this defines `scheme`

        # 2. OCR answer sheet + extract answers
        ans_text = ocr_pdf_bytes(ans_file.read())
        student_answers_obj = extract_student_answers(scheme, ans_text)  # <- this defines `student_answers_obj`

        # 3. Grade using scheme + extracted answers
        report = grade_script(scheme, student_answers_obj)

        st.subheader("Overall Result")
        st.metric("Score", f"{report['total']} / {report['max_total']}")
        st.metric("Percentage", f"{report['percentage']:.1f}%")
        st.metric("Grade", report['grade'])
