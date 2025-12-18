# grade.py
from typing import Dict, Any, List
from answer_key import ANSWER_KEY, QuestionSpec

def norm(s: str) -> str:
    return " ".join((s or "").lower().strip().split())

def eval_mcq(q: QuestionSpec, ans: str) -> tuple[float, str]:
    """
    MCQ grading based on FULL option text, not just a/b/c/d.
    Student answer can be:
      - the full option text
      - option letter + text
      - text with minor extra words
    """
    if not ans:
        return 0.0, "No answer."

    s = norm(ans)
    correct = norm(q.correct_option_text or "")

    # If student wrote exactly / contains the correct text, or vice versa, accept.
    if correct and (correct in s or s in correct):
        return q.max_marks, "Correct option chosen."

    return 0.0, f"Incorrect. Correct option: {q.correct_option_text}."

# ... keep all other eval_* functions as before ...

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
