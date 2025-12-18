# grade.py
from typing import Dict, Any, List
from llm_groq import grade_subjective

def norm(s: str) -> str:
    return " ".join((s or "").lower().strip().split())

def grade_one_question(q: Dict[str, Any], student_answer: str) -> Dict[str, Any]:
    """
    - MCQ: strict text-based check on full correct option text; fallback to Groq if key missing.
    - Non-MCQ: lenient Groq grading using model_answer and max_marks.
    """
    q_type = q.get("type")
    max_marks = float(q.get("max_marks", 0))
    student_answer = student_answer or ""
    s_norm = norm(student_answer)

    # MCQ grading (old logic)
    if q_type == "mcq":
        correct_text = norm(q.get("correct_option_text") or "")

        # If scheme lacks correct_text, fallback to Groq
        if not correct_text:
            graded = grade_subjective(q, student_answer)
            marks = float(graded.get("marks_awarded", 0.0))
            marks = max(0.0, min(marks, max_marks))
            return {"score": marks, "feedback": graded.get("feedback", "")}

        # Student may write the whole option or a slightly longer/shorter phrase.
        if correct_text and (correct_text in s_norm or s_norm in correct_text):
            return {"score": max_marks, "feedback": "Correct option chosen."}

        if student_answer:
            return {
                "score": 0.0,
                "feedback": f"Incorrect. Correct option: {q.get('correct_option_text', '')}."
            }

        return {"score": 0.0, "feedback": "No answer."}

    # Non-MCQ: lenient Groq grading
    graded = grade_subjective(q, student_answer)
    marks = float(graded.get("marks_awarded", 0.0))
    if marks < 0:
        marks = 0.0
    if marks > max_marks:
        marks = max_marks

    return {
        "score": marks,
        "feedback": graded.get("feedback", ""),
    }

def grade_script(scheme: Dict[str, Any],
                 student_answers_obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    scheme: marking_scheme.json as dict
    student_answers_obj: output from extract_student_answers()
    """
    ans_by_id = {
        a["question_id"]: a["answer"]
        for a in student_answers_obj.get("answers", [])
    }

    results: List[Dict[str, Any]] = []
    total = 0.0

    # Use real max_total from scheme; you had hard-coded 80 before.
    max_total = 0.0

    for q in scheme.get("questions", []):
        qid = q["id"]
        ans = ans_by_id.get(qid, "")
        graded = grade_one_question(q, ans)
        max_marks = float(q.get("max_marks", 0))

        results.append({
            "id": qid,
            "text": q["text"],
            "student_answer": ans,
            "score": graded["score"],
            "max_marks": max_marks,
            "feedback": graded["feedback"],
        })

        total += graded["score"]
        max_total += max_marks

    percentage = (total / max_total) * 100 if max_total else 0.0
    grade_letter = (
        "A+" if percentage >= 90 else
        "A" if percentage >= 80 else
        "B" if percentage >= 70 else
        "C"
    )

    return {
        "student_name": student_answers_obj.get("student_name"),
        "roll_no": student_answers_obj.get("roll_no"),
        "questions": results,
        "total": total,
        "max_total": max_total,
        "percentage": percentage,
        "grade": grade_letter,
    }
