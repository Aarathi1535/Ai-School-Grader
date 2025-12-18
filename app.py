import json
from grader_core import load_answer_key, grade_script
from student_answers_schema import StudentScript, StudentAnswer

def build_student_script_from_ocr(ocr_json_path: str) -> StudentScript:
    # Here you call your existing Azure OCR + mapping logic and finally
    # create a StudentScript object. For demo, hard-code Roman’s few answers.
    # [file:2]

    answers = [
        StudentAnswer(question_id="1.1", answer="They lack intermolecular spaces"),
        StudentAnswer(question_id="1.2", answer="Higher to lower concentration"),
        StudentAnswer(question_id="2.i.1", answer="True"),  # intentionally wrong
        StudentAnswer(question_id="2.ii.1", answer="Physical"),
        StudentAnswer(question_id="2.iii.1", answer="H"),
        StudentAnswer(question_id="2.iv.1", answer="The process in which liquid state changes into gaseous state is called as Evaporation."),
        StudentAnswer(question_id="2.v.1", answer="Elements"),
        StudentAnswer(question_id="3.1.a", answer="Solids have more density. Liquid have less density compared to solids."),
        StudentAnswer(question_id="3.1.b", answer="Elements- Pure substances consists of only one type of atoms. Compounds- Pure homogeneous substances which are made up of two or more elements in fixed ratio."),
        StudentAnswer(question_id="3.2.a", answer="Air space that makes it light."),
        StudentAnswer(question_id="4.1.a", answer="Sublimation")
    ]

    script = StudentScript(
        student_name="Roman Manuel",
        roll_no="33",
        meta={"exam_id": "chem-2025-term1"},
        answers=answers
    )
    return script

def main():
    answer_key = load_answer_key("answer_key.json")
    script = build_student_script_from_ocr("roman_ocr.json")
    report = grade_script(answer_key, script)

    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
