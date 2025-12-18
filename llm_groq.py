# llm_groq.py
import json
import time
from groq import Groq, RateLimitError
from config import GROQ_API_KEY, GROQ_MODEL_EXTRACTION, GROQ_MODEL_GRADING

_client = Groq(api_key=GROQ_API_KEY)

def llm_json(model: str, system_prompt: str, user_prompt: str,
             max_retries: int = 3) -> dict:
    """
    Generic helper: call Groq and get JSON with simple rate-limit backoff.
    """
    for attempt in range(max_retries):
        try:
            resp = _client.chat.completions.create(
                model=model,
                temperature=0.0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return json.loads(resp.choices[0].message.content)
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.5)


# ---------- Marking scheme extraction ----------

SCHEME_SYSTEM_PROMPT = """
You are an expert exam-paper parser for middle school chemistry.

Given the full text of a question paper, build a marking scheme as JSON:

{
  "exam_title": string,
  "total_marks": float,
  "questions": [
    {
      "id": string,              // e.g. "1.1", "2(i).3", "3.2.a"
      "section": string,         // "A" or "B"
      "text": string,            // question text WITHOUT the options
      "type": string,            // one of: ["mcq","true_false","fill","symbol",
                                 //          "short_def","reason","classify",
                                 //          "differentiate","flowchart","short_direct"]
      "options": [string],       // for mcq only
      "correct_option_text": string | null,  // for mcq only: full correct option text
      "correct_value": string | null,        // canonical correct answer for non-mcq
      "model_answer": string,    // short ideal answer / marking scheme text
      "max_marks": float
    }
  ]
}

Rules:
- Use the marks in brackets [] in the paper to set max_marks per question or per sub-question.
- For MCQs:
  - Fill "options" with the four options in order.
  - Infer the correct option using your chemistry knowledge.
  - Set "correct_option_text" to the full text of the correct option.
  - Leave "correct_value" null.
- For non-MCQ:
  - "correct_option_text" must be null.
  - "correct_value" should be a concise canonical answer (e.g., "physical change", "H2O").
  - "model_answer" should be a short marking scheme style sentence (what teacher expects).
- Use unique ids in the same order as they appear in the paper.
- Split multi-part questions into separate entries, e.g.,
  - 2(i).1, 2(i).2 ... for T/F
  - 4.2.a, 4.2.b ... for diagram sub-parts.
"""

def extract_marking_scheme(exam_text: str) -> dict:
    user_prompt = f"EXAM PAPER OCR TEXT:\n\n{exam_text}"
    return llm_json(
        model=GROQ_MODEL_EXTRACTION,
        system_prompt=SCHEME_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )


# ---------- Student answer extraction ----------

ANSWER_EXTRACT_SYSTEM_PROMPT = """
You are an answer-booklet parser.

You receive:
- A list of exam questions (id, text, type).
- The full OCR text of one student's handwritten answer booklet.

Your task:
- Map each question id to the student's answer text.
- Extract the student's name and roll number when present near the top.

Output JSON:
{
  "student_name": string | null,
  "roll_no": string | null,
  "answers": [
    { "question_id": string, "answer": string }
  ]
}

Guidelines:
- Use the questions list (order and wording) to align the answers.
- If a question seems unanswered, omit that question_id from the answers array.
- For sub-parts (like 4.2.a, 4.2.b), store just the relevant portion (e.g., student's text for that sub-part).
"""

def extract_student_answers(exam_scheme: dict, answer_text: str) -> dict:
    questions_min = [
        {"id": q["id"], "text": q["text"], "type": q["type"]}
        for q in exam_scheme.get("questions", [])
    ]
    user_prompt = f"""
QUESTIONS (ID, TEXT, TYPE):
{json.dumps(questions_min, ensure_ascii=False, indent=2)}

STUDENT ANSWER BOOKLET OCR TEXT:
{answer_text}
"""
    return llm_json(
        model=GROQ_MODEL_EXTRACTION,
        system_prompt=ANSWER_EXTRACT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )


# ---------- Lenient subjective grading ----------


def grade_subjective(question: dict, student_answer: str) -> dict:
    """
    Lenient grading for all non-MCQ questions, imitating a human teacher:
    - Full marks whenever the main concept is correct (even if wording is different).
    - Partial marks only when an important point is missing or unclear.
    - Zero marks only when the answer is mostly wrong / off-topic / blank.
    """
    system_prompt = """
You are a middle school chemistry teacher grading written answers.

You are given:
- one question (with type and max_marks)
- a marking scheme / model_answer (what the teacher expects)
- one student's answer

Your grading style must imitate a lenient human teacher, like in real school exams:

- Focus on CONCEPTS, not exact words.
- If the student's answer clearly shows the correct idea, GIVE FULL MARKS,
  even if:
  - capitalization is different
  - grammar is imperfect
  - synonyms or different phrasing are used
- Give PARTIAL marks only when:
  - the student captures some of the idea but misses one or more important points
  - the explanation is very vague but not completely wrong
- Give ZERO or very low marks only when:
  - the answer is mostly or fully incorrect
  - it contradicts the marking scheme
  - it is blank or off-topic

IGNORE:
- capitalization
- small spelling errors
- language level (as long as meaning is clear)

Many questions may have multiple valid phrasings. Use your chemistry knowledge
to accept equivalent answers generously.

Output ONLY valid JSON of the form:
{
  "marks_awarded": float,   // between 0 and max_marks
  "feedback": string        // short, friendly explanation
}
"""

    user_prompt = f"""
Question ID: {question.get("id")}
Type: {question.get("type")}
Max marks: {question.get("max_marks")}

Question text:
{question.get("text", "")}

Marking scheme / model answer (teacher's expected key points):
{question.get("model_answer", "")}

Student answer:
{student_answer}
"""

    resp = _client.chat.completions.create(
        model=GROQ_MODEL_GRADING,
        temperature=0.0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    out = json.loads(resp.choices[0].message.content)
    out.setdefault("marks_awarded", 0.0)
    out.setdefault("feedback", "")
    return out
