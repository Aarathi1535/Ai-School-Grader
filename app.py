# app.py
import streamlit as st
from ocr_azure import ocr_pdf_bytes
from parser import parse_answers_from_text
from grade import grade_script

st.set_page_config(page_title="AI School Grader", layout="wide")
st.title("AI School Grader – Chemistry (Class 7)")

st.write("Upload the **question paper** and **student answer sheet** to evaluate using the fixed answer key.")

col1, col2 = st.columns(2)
with col1:
    qp_file = st.file_uploader("Question paper PDF", type=["pdf"], key="qp")
with col2:
    ans_file = st.file_uploader("Answer sheet PDF", type=["pdf"], key="ans")

if st.button("Evaluate Answer Sheet"):
    if not qp_file or not ans_file:
        st.error("Please upload both PDFs.")
    else:
        # 1. OCR question paper (for reference only)
        qp_text = ocr_pdf_bytes(qp_file.read())
        with st.expander("Question Paper OCR (reference)"):
            st.text(qp_text)

        # 2. OCR answer sheet
        ans_text = ocr_pdf_bytes(ans_file.read())
        with st.expander("Answer Sheet OCR (raw)"):
            st.text(ans_text)

        # 3. Parse answers -> {question_id: answer}
        student_answers = parse_answers_from_text(ans_text)
        with st.expander("Parsed Answers (by question ID)"):
            st.json(student_answers)

        # 4. Grade deterministically from answer_key
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
