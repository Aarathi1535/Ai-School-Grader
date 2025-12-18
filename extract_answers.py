# extract_answers.py
import json
from ocr_azure import ocr_pdf_bytes
from llm_groq import extract_student_answers

def extract_answers_for_pdf(answer_pdf_path: str,
                            scheme_json_path: str = "data/marking_scheme.json") -> dict:
    with open(answer_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    answer_text = ocr_pdf_bytes(pdf_bytes)

    with open(scheme_json_path, "r", encoding="utf-8") as f:
        scheme = json.load(f)

    return extract_student_answers(scheme, answer_text)

if __name__ == "__main__":
    obj = extract_answers_for_pdf("New-Doc-12-13-2025-13.30.pdf",
                                  "data/marking_scheme.json")
    print(json.dumps(obj, ensure_ascii=False, indent=2))
