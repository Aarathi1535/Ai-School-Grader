import json
from typing import Dict, Any, List, Tuple

from student_answers_schema import StudentScript, StudentAnswer
from utils_text import normalize_text, equals_loose, contains_keywords

def load_answer_key(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    key_by_id = {q["id"]: q for q in data["questions"]}
    return {"meta": data["meta"], "questions_by_id": key_by_id}
def grade_mcq(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, q.get("feedback_incorrect", "No answer provided.")

    # Normalize
    ans_norm = normalize_text(ans)
    options = q["options"]
    correct_idx = q["correct_option_index"]
    correct_text_norm = normalize_text(options[correct_idx])

    # 1) Try strict text match
    if ans_norm == correct_text_norm:
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")

    # 2) If student wrote only the key phrase, accept if it is contained
    # e.g. "they lack interndecular spaces" vs "they lack intermolecular spaces"
    if ans_norm in correct_text_norm or correct_text_norm in ans_norm:
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")

    # 3) Keyword match: require at least one key word from correct option
    correct_words = [w for w in correct_text_norm.split() if len(w) > 3]
    if all(w in ans_norm for w in correct_words[:2]):  # first two content words
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")

    return 0.0, q.get("feedback_incorrect", "Incorrect option.")


def grade_true_false(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    correct = q["correct_value"]
    if equals_loose(ans, correct):
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    return 0.0, q.get("feedback_incorrect", "Incorrect.")

def grade_fill(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    if equals_loose(ans, q["correct_value"]):
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    for v in q.get("accepted_values", []):
        if equals_loose(ans, v):
            return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    return 0.0, q.get("feedback_incorrect", "Incorrect.")

def grade_short_direct(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    correct = q.get("correct_value")
    accepted = q.get("accepted_values", [])
    if correct and equals_loose(ans, correct):
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    if any(equals_loose(ans, v) for v in accepted):
        return float(q["max_marks"]), q.get("feedback_correct", "Correct.")
    return 0.0, q.get("feedback_incorrect", "Incorrect.")

def grade_classify(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    return grade_short_direct(q, ans)

def grade_short_def(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans or not ans.strip():
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    return float(q["max_marks"]), q.get("feedback_correct", "Correct definition.")

def grade_reason(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    if not ans or not ans.strip():
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    return float(q["max_marks"]), q.get("feedback_correct", "Correct reason.")

def grade_differentiate(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    special = q.get("special_rubric")
    if not ans or not ans.strip():
        return 0.0, q.get("feedback_incorrect", "No answer provided.")
    max_m = float(q["max_marks"])
    if special == "partial_as_meridian":
        has_left = any(w in normalize_text(ans) for w in ["element", "pure"])
        has_right = any(w in normalize_text(ans) for w in ["compound", "ratio", "combined", "mixtures", "mixture"])
        if has_left and has_right:
            return max_m / 2.0, q.get("feedback_partial", "Partially correct.")
        return 0.0, q.get("feedback_incorrect", "Incorrect differentiation.")
    if ";" in ans or "-" in ans or " vs " in ans.lower():
        return max_m, q.get("feedback_correct", "Correct differentiation.")
    return max_m, q.get("feedback_correct", "Correct differentiation.")

def grade_question(q: Dict[str, Any], ans: str) -> Tuple[float, str]:
    t = q["type"]
    if t == "mcq": return grade_mcq(q, ans)
    if t == "true_false": return grade_true_false(q, ans)
    if t == "fill": return grade_fill(q, ans)
    if t in ("short_direct", "symbol", "flowchart"): return grade_short_direct(q, ans)
    if t == "classify": return grade_classify(q, ans)
    if t == "short_def": return grade_short_def(q, ans)
    if t == "reason": return grade_reason(q, ans)
    if t == "differentiate": return grade_differentiate(q, ans)
    return 0.0, "Question type not handled."

def compute_grade_from_percentage(p: float) -> str:
    if p >= 90: return "A"
    if p >= 80: return "B"
    if p >= 70: return "C"
    if p >= 60: return "D"
    return "E"

def grade_script(answer_key: Dict[str, Any], script: StudentScript) -> Dict[str, Any]:
    key_by_id = answer_key["questions_by_id"]
    results: List[Dict[str, Any]] = []
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
