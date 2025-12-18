# generate_scheme.py
import json
from ocr_azure import ocr_pdf_bytes
from llm_groq import extract_marking_scheme

def build_marking_scheme_from_pdf(exam_pdf_path: str,
                                  out_json_path: str = "data/marking_scheme.json") -> dict:
    with open(exam_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    exam_text = ocr_pdf_bytes(pdf_bytes)
    scheme = extract_marking_scheme(exam_text)
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(scheme, f, ensure_ascii=False, indent=2)
    return scheme

if __name__ == "__main__":
    scheme = build_marking_scheme_from_pdf("Exam-paper.pdf", "data/marking_scheme.json")
    print("Marking scheme saved to data/marking_scheme.json")
