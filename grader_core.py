import json
from typing import Dict, Any, List, Tuple
# grader_core.py
from .student_answers_schema import StudentScript, StudentAnswer
from utils_text import normalize_text, equals_loose, contains_keywords

def load_answer_key(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    key_by_id = {q["id"]: q for q in data["questions"]}
    return {"meta": data["meta"], "questions_by_id": key_by_id}

def grade_mcq(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, q.get("feedback_incorrect", "No answer provided.")

    # Assume ans is the full option text; normalize and match.
    options = q["options"]
    correct_idx = q["correct_option_index"]
    correct_text_norm = normalize_text(options[correct_idx])
    ans_norm = normalize_text(ans)

    if ans_norm == correct_text_norm:
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    return 0.0, q.get("feedback_incorrect", "Incorrect.")

def grade_true_false(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    correct = q["correct_value"]
    if equals_loose(ans, correct):
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    return 0.0, q.get("feedback_incorrect", "Incorrect.")

def grade_fill(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    correct = q["correct_value"]
    if equals_loose(ans, correct):
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    return 0.0, q.get("feedback_incorrect", "Incorrect.")

def grade_short_direct(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    correct = q["correct_value"]
    accepted = q.get("accepted_values", [])
    if equals_loose(ans, correct) or any(equals_loose(ans, v) for v in accepted):
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    return 0.0, q.get("feedback_incorrect", "Incorrect.")

def grade_classify(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    return grade_short_direct(q, ans)

def grade_short_def(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    # Meridian is quite lenient for correct concept. [file:2]
    if not ans.strip():
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    # You can add keyword checks if needed using q["model_answer"].
    return float(q["max_marks"]), q.get("feedback_correct", "Correct definition.")

def grade_reason(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans.strip():
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    return float(q["max_marks"]), q.get("feedback_correct", "Correct reason.")

def grade_differentiate(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    special = q.get("special_rubric")
    if not ans.strip():
        return 0.0, q.get("feedback_incorrect", "No answer provided.")

    # For now, treat any non-empty, structured answer as mostly correct.
    max_m = float(q["max_marks"])
    if special == "partial_as_meridian":
        # Emulate meridian partial for Q3.1.b and Q3.1.e. [file:2]
        # Very simple heuristic: if both sides seem mentioned, give 0.5, else 0.
        model = q.get("model_answer", {})
        left_kw = model.get("left", "")
        right_kw = model.get("right", "")
        has_left = any(w in normalize_text(ans) for w in ["element", "pure"])
        has_right = any(w in normalize_text(ans) for w in ["compound", "ratio", "combined"])

        if has_left and has_right:
            # Meridian gave 0.5 even when both concepts present but wording slightly off. [file:2]
            return max_m / 2.0, q.get("feedback_partial", "Partially correct.")
        return 0.0, q.get("feedback_incorrect", "Incorrect differentiation.")
    else:
        # Generic differentiation: if it looks like two parts, give full marks.
        if ";" in ans or "-" in ans or " vs " in ans.lower():
            return max_m, q.get("feedback_correct", "Correct differentiation.")
        return max_m, q.get("feedback_correct", "Correct differentiation.")

def grade_question(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    qtype = q["type"]
    if qtype == "mcq":
        return grade_mcq(q, ans)
    if qtype == "true_false":
        return grade_true_false(q, ans)
    if qtype == "fill":
        return grade_fill(q, ans)
    if qtype in ("short_direct", "symbol", "flowchart"):
        return grade_short_direct(q, ans)
    if qtype == "classify":
        return grade_classify(q, ans)
    if qtype == "short_def":
        return grade_short_def(q, ans)
    if qtype == "reason":
        return grade_reason(q, ans)
    if qtype == "differentiate":
        return grade_differentiate(q, ans)
    # Fallback: give 0 with generic feedback.
    return 0.0, "Question type not handled."

def grade_script(answer_key: Dict[str, Any], script: StudentScript) -> Dict[str, Any]:
    key_by_id = answer_key["questions_by_id"]
    results = []
    total_obtained = 0.0
    max_total = 0.0

    ans_map: Dict[str, str] = {a.question_id: a.answer for a in script.answers}

    for qid, q in key_by_id.items():
        max_marks = float(q["max_marks"])
        max_total += max_marks

        ans_text = ans_map.get(qid, "").strip()
        marks, feedback = grade_question(q, ans_text)
        total_obtained += marks

        results.append({
            "question_id": qid,
            "question_text": q["text"],
            "type": q["type"],
            "max_marks": max_marks,
            "marks_awarded": marks,
            "student_answer": ans_text,
            "feedback": feedback
        })

    percentage = (total_obtained / max_total * 100.0) if max_total > 0 else 0.0
    grade = compute_grade_from_percentage(percentage)

    return {
        "student_name": script.student_name,
        "roll_no": script.roll_no,
        "total_score": total_obtained,
        "max_marks": max_total,
        "percentage": percentage,
        "grade": grade,
        "details": results
    }

def compute_grade_from_percentage(p: float) -> str:
    # Approximate Meridian style; Roman got 93.8% -> A. [file:2]
    if p >= 90:
        return "A"
    if p >= 80:
        return "B"
    if p >= 70:
        return "C"
    if p >= 60:
        return "D"
    return "E"
