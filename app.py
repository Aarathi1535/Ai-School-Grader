# app.py
import streamlit as st
import json
from ocr_azure import ocr_pdf_bytes
from llm_groq import extract_marking_scheme, extract_student_answers
from grade import grade_script

st.set_page_config(page_title="AI Answer Sheet Evaluator", layout="wide")
st.title("AI Answer Sheet Evaluator (Azure OCR + Groq)")

tab_exam, tab_grade = st.tabs(["1. Build Marking Scheme", "2. Grade Answer Sheet"])

with tab_exam:
    st.subheader("Upload Exam Question Paper (PDF)")
    qp_file = st.file_uploader("Question paper PDF", type=["pdf"], key="qp")
    if st.button("Generate Marking Scheme") and qp_file:
        exam_text = ocr_pdf_bytes(qp_file.read())
        scheme = extract_marking_scheme(exam_text)
        st.success("Marking scheme generated.")

        st.download_button(
            "Download marking_scheme.json",
            data=json.dumps(scheme, ensure_ascii=False, indent=2),
            file_name="marking_scheme.json",
            mime="application/json"
        )
        st.json(scheme)

with tab_grade:
    st.subheader("Grade a Student Answer Sheet")
    scheme_file = st.file_uploader("Upload marking_scheme.json", type=["json"])
    answer_pdf = st.file_uploader("Upload student's answer sheet (PDF)", type=["pdf"])

    if st.button("Evaluate Answer Sheet") and scheme_file and answer_pdf:
        scheme = json.load(scheme_file)
        ans_text = ocr_pdf_bytes(answer_pdf.read())
        student_answers_obj = extract_student_answers(scheme, ans_text)
        report = grade_script(scheme, student_answers_obj)

        st.markdown(
            f"**Student:** {report.get('student_name') or 'Unknown'} "
            f"(Roll: {report.get('roll_no') or 'N/A'})"
        )
        st.metric("Score", f"{report['total']} / {report['max_total']}")
        st.metric("Percentage", f"{report['percentage']:.1f}%")
        st.metric("Grade", report["grade"])

        st.subheader("Detailed Evaluation")
        for q in report["questions"]:
            with st.expander(f"Q {q['id']} – {q['score']}/{q['max_marks']}"):
                st.write(f"**Question:** {q['text']}")
                st.write(f"**Student Answer:** {q['student_answer']}")
                st.write(f"**Feedback:** {q['feedback']}")
