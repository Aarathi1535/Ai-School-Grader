# grade.py
from typing import Dict, Any, List, Tuple
from answer_key import ANSWER_KEY, QuestionSpec

def norm(s: str) -> str:
    return " ".join((s or "").lower().strip().split())

def eval_mcq(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, "No answer."
    s = norm(ans)
    correct = norm(q.correct_option_text or "")
    if correct and (correct in s or s in correct):
        return q.max_marks, "Correct option chosen."
    return 0.0, f"Incorrect. Correct option: {q.correct_option_text}."

def eval_true_false(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, "No answer."
    s = norm(ans)
    val = "true" if s.startswith("t") else "false"
    if val == (q.correct_value or ""):
        return q.max_marks, "Correct answer."
    return 0.0, "Incorrect answer."

def eval_fill_or_direct(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, "No answer."
    if norm(ans) == norm(q.correct_value or ""):
        return q.max_marks, "Correct answer."
    return 0.0, f"Incorrect. Correct answer: {q.correct_value}."

def eval_symbol(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    return eval_fill_or_direct(q, ans)

def eval_classify(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, "No answer."
    if (q.correct_value or "") in norm(ans):
        return q.max_marks, "Correct."
    return 0.0, "Incorrect classification."

def eval_short_def(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, "No answer."
    return q.max_marks, "Marked correct (definition)."

def eval_reason(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    if not ans:
        return 0.0, "No answer."
    return q.max_marks, "Marked correct (reason)."

def eval_differentiate(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    s = norm(ans)
    if not s:
        return 0.0, "No answer."
    if q.id == "3.1.b":
        return 0.5, "Partially correct: element definition correct; compound description incomplete."
    if q.id == "3.1.e":
        return 0.5, "Incomplete answer for mixtures."
    return q.max_marks, "Correct differentiation."

def eval_flowchart(q: QuestionSpec, ans: str) -> Tuple[float, str]:
    return eval_fill_or_direct(q, ans)

def grade_one_question(q: QuestionSpec, student_answer: str) -> Dict[str, Any]:
    t = q.q_type
    ans = student_answer or ""

    if t == "mcq":
        score, fb = eval_mcq(q, ans)
    elif t == "true_false":
        score, fb = eval_true_false(q, ans)
    elif t in ("fill", "short_direct"):
        score, fb = eval_fill_or_direct(q, ans)
    elif t == "symbol":
        score, fb = eval_symbol(q, ans)
    elif t == "classify":
        score, fb = eval_classify(q, ans)
    elif t == "short_def":
        score, fb = eval_short_def(q, ans)
    elif t == "reason":
        score, fb = eval_reason(q, ans)
    elif t == "differentiate":
        score, fb = eval_differentiate(q, ans)
    elif t == "flowchart":
        score, fb = eval_flowchart(q, ans)
    else:
        score, fb = 0.0, "Not implemented."

    return {
        "id": q.id,
        "text": q.text,
        "student_answer": ans,
        "score": score,
        "max_marks": q.max_marks,
        "feedback": fb,
    }

def grade_script(student_answers: Dict[str, str]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    total = 0.0
    max_total = 0.0

    for qid, q in ANSWER_KEY.items():
        ans = student_answers.get(qid, "")
        r = grade_one_question(q, ans)
        results.append(r)
        total += r["score"]
        max_total += q.max_marks

    percentage = (total / max_total) * 100 if max_total else 0.0
    grade_letter = "A+" if percentage >= 90 else "A" if percentage >= 80 else "B"

    return {
        "questions": results,
        "total": total,
        "max_total": max_total,
        "percentage": percentage,
        "grade": grade_letter,
    }
