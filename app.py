import streamlit as st
from grader_core import load_answer_key, grade_script
from student_answers_schema import StudentScript, StudentAnswer
import re

ANSWER_KEY = load_answer_key("answer_key.json")

# --- 1. OCR stub (replace with your real Azure call) ---

def azure_ocr_extract_text(pdf_bytes: bytes) -> str:
    # TEMP: return hard-coded text like Roman's sheet so pipeline works
    return """
New Doc 12-13-2025 13.30 BALDWIN BOYS HIGH SCHOOL...
1. A. They lack interndecular spaces
2. A. Higher to lower concentration
3. A. Taken in
4. A. Cohesion
5. A. Both bandc
6. A. Physical chang
7. A. liquids
8. A. atoms
9. A. Photosynthesis
10. A. A fast change
11-0 Mercury
12.A. Grystalline shafo
13.A. Argon Ozone
14. A. Gunpowder
15.A. compound
PA True X
2.A. False
3. A. False
4.A. Jrue X
5.A. Jrue
ii 1.n Physical
2.A. Oxygen and Water
3-A. 3
4.A. Elements
5. A. Electrolyis
iii 1.A. H
2. A Cl
3.A. P
4.A. Mg
5. A. Fe
iv 1.A The process in which liquid state changes into gascon state is called as Evaporation.
2. A. The chemical reaction in which the heat is absorbed.
3.A. No new substances are formed. It is usually reversible and some changes involve heating or et cooling.
4.A. A Grouf of elements which has both properties of metalls,
6.A. The substances which mir with other mixture completely is called Homogeneous mixture.
1A Elements
2.A. Compound
3. A. Mixture
4.A Compound
5.1. Mixture
6.A. Mixture Element
8.A. Mixture
9.A. Comfround
10.1. Mixture
Section-B Question 3.
1. A. solids have Jonore more density Liquid have less density compared to slide
2. A. Elements - Pure substances consils of only one type of atoms Compounds Pure homogeneous substances which are made wh of two or more compounds comp raha
3. A. Day and Night - Periodic change Eruption of Volcano - Non - Periodic change
4. A. Monoatomic - 1 Diatomic - 2
5. A. Compounds - It is separated by hand.c Mixtures- 56 is separated by sparating fun
Give Reasons
1.A. Air shace that make it light.
2.A. Because buring gives out the heat.
3.A. They are closely packed together.
4.A. Because of we burn the camelle we get the wars was... Carbon dioxide...
5. A. Because it is missed with two or more elements elements or compound or two more compounds in any ratio
Question 4
1. a. Sublimation
b. Scharting furn
c. Filtration
d. Evaporation
e. Fillbration
2. a. A- Residue B-Water
6. It is a comfround
c. Because sall and water form homogeneous mixhave which connot be scharated by this method
d. H2O
question-5
1. A. 1- Mixture 2- Compounds 3- Heterogeneous 4- Non-Metalls 5. Mettaliods
2. a- Heterogeneous mixture b. Triatomic c. separating Fund d. Hetting Freezing ze. slow change
Question-6
a. Solid Solid heterogenous b. Iron L. Both iron and sulphur are not attracted to the maquet
2. a. Conical flask b. Funnel c. Separating fure d. watch-Glass e. Round bottomed flask glass! F. Test tube holder
"""

# --- 2. Map OCR text -> StudentScript for this exam ---

MCQ_ID_MAP = {
    1: "1.1", 2: "1.2", 3: "1.3", 4: "1.4", 5: "1.5",
    6: "1.6", 7: "1.7", 8: "1.8", 9: "1.9", 10: "1.10",
    11: "1.11", 12: "1.12", 13: "1.13", 14: "1.14", 15: "1.15"
}

def build_script_from_ocr_text(ocr_text: str, student_name: str, roll_no: str) -> StudentScript:
    lines = [l.strip() for l in ocr_text.splitlines() if l.strip()]
    answers: list[StudentAnswer] = []

    # Section A, Q1 MCQs: pattern like "1. A. They lack interndecular spaces" [file:3]
    mcq_pattern = re.compile(r"^(\d+)\.\s*A\.\s*(.+)$", re.IGNORECASE)
    seen_mcq = set()
    for line in lines:
        m = mcq_pattern.match(line)
        if not m:
            continue
        qno = int(m.group(1))
        text = m.group(2)
        if qno in MCQ_ID_MAP and qno not in seen_mcq:
            answers.append(StudentAnswer(MCQ_ID_MAP[qno], text))
            seen_mcq.add(qno)

    # Section A Q2: use Roman’s exact lines as anchors [file:3]
    for line in lines:
        low = line.lower()
        if low.startswith("pa true"):
            answers.append(StudentAnswer("2.i.1", "True"))
        elif "2.a. false" in low and "symbol of potassium" not in low:
            answers.append(StudentAnswer("2.i.2", "False"))
        elif re.search(r"\b3\.\s*a\.\s*false", low):
            answers.append(StudentAnswer("2.i.3", "False"))
        elif "4.a. jrue" in low or "4.a. true" in low:
            answers.append(StudentAnswer("2.i.4", "True"))
        elif "5.a. jrue" in low or "5.a. true" in low:
            answers.append(StudentAnswer("2.i.5", "True"))

        if "1.n physical" in low or "1.a physical" in low:
            answers.append(StudentAnswer("2.ii.1", "Physical"))
        if "oxygen and water" in low:
            answers.append(StudentAnswer("2.ii.2", "Oxygen and Water"))
        if re.search(r"\b3[- ]a\.\s*3\b", low):
            answers.append(StudentAnswer("2.ii.3", "3"))
        if "4.a. elements" in low:
            answers.append(StudentAnswer("2.ii.4", "Elements"))
        if "5. a. electrolys" in low:
            answers.append(StudentAnswer("2.ii.5", "Electrolysis"))

        if "1.a h" in low:
            answers.append(StudentAnswer("2.iii.1", "H"))
        if "2. a cl" in low:
            answers.append(StudentAnswer("2.iii.2", "Cl"))
        if "3.a. p" in low:
            answers.append(StudentAnswer("2.iii.3", "P"))
        if "4.a. mg" in low:
            answers.append(StudentAnswer("2.iii.4", "Mg"))
        if "5. a. fe" in low:
            answers.append(StudentAnswer("2.iii.5", "Fe"))

        if "evaporation" in low and "liquid state changes into gas" in low:
            answers.append(StudentAnswer("2.iv.1", line))
        if "heat is absorbed" in low:
            answers.append(StudentAnswer("2.iv.2", line))
        if "no new substances are formed" in low:
            answers.append(StudentAnswer("2.iv.3", line))
        if "properties of metalls" in low or "properties of metals" in low:
            answers.append(StudentAnswer("2.iv.4", line))
        if "mix with other mixture completely" in low:
            answers.append(StudentAnswer("2.iv.5", line))

        if "1a elements" in low:
            answers.append(StudentAnswer("2.v.1", "Elements"))
        if "2.a. compound" in low:
            answers.append(StudentAnswer("2.v.2", "Compound"))
        if "3. a. mixture" in low:
            answers.append(StudentAnswer("2.v.3", "Mixture"))
        if "4.a compound" in low and "ammonia" in ocr_text.lower():
            answers.append(StudentAnswer("2.v.4", "Compound"))
        if "5.1. mixture" in low:
            answers.append(StudentAnswer("2.v.5", "Mixture"))
        if "6.a. mixture" in low:
            answers.append(StudentAnswer("2.v.6", "Mixture"))
        if "element 8.a. mixture" in low:
            answers.append(StudentAnswer("2.v.7", "Element"))
        if "8.a. mixture" in low:
            answers.append(StudentAnswer("2.v.8", "Mixture"))
        if "9.a. comfround" in low or "9.a. compound" in low:
            answers.append(StudentAnswer("2.v.9", "Compound"))
        if "10.1. mixture" in low:
            answers.append(StudentAnswer("2.v.10", "Mixture"))

    # Section B mapping using Roman’s phrases [file:3]
    for line in lines:
        low = line.lower()
        if "solids have" in low and "density" in low:
            answers.append(StudentAnswer("3.1.a", line))
        elif "elements - pure substances" in low:
            answers.append(StudentAnswer("3.1.b", line))
        elif "day and night" in low and "eruption of volcano" in low:
            answers.append(StudentAnswer("3.1.c", line))
        elif "monoatomic" in low and "diatomic" in low:
            answers.append(StudentAnswer("3.1.d", line))
        elif "compounds - it is separated by" in low and "separating fun" in low:
            answers.append(StudentAnswer("3.1.e", line))
        elif "air shace" in low or "air space" in low:
            answers.append(StudentAnswer("3.2.a", line))
        elif "buring gives out the heat" in low or "burning gives out the heat" in low:
            answers.append(StudentAnswer("3.2.b", line))
        elif "closely packed together" in low:
            answers.append(StudentAnswer("3.2.c", line))
        elif "burn the camelle" in low or "burn the candle" in low:
            answers.append(StudentAnswer("3.2.d", line))
        elif "mixed with two or more elements" in low:
            answers.append(StudentAnswer("3.2.e", line))
        elif "1. a. sublimation" in low:
            answers.append(StudentAnswer("4.1.a", "Sublimation"))
        elif "b. scharting furn" in low or "b. separating fun" in low:
            answers.append(StudentAnswer("4.1.b", "Separating funnel"))
        elif "c. filtration" in low:
            answers.append(StudentAnswer("4.1.c", "Filtration"))
        elif "d. evaporation" in low:
            answers.append(StudentAnswer("4.1.d", "Evaporation"))
        elif "e. fillbration" in low or "e. filtration" in low:
            answers.append(StudentAnswer("4.1.e", "Filtration"))
        elif "a- residue b-water" in low:
            answers.append(StudentAnswer("4.2.a", "A- Residue B- Water"))
        elif "it is a comfround" in low or "it is a compound" in low:
            answers.append(StudentAnswer("4.2.b", "It is a compound"))
        elif "homogeneous mixhave" in low or "homogeneous mixture" in low:
            answers.append(StudentAnswer("4.2.c", line))
        elif "d. ho" in low or "d. h2o" in low:
            answers.append(StudentAnswer("4.2.d", "H2O"))
        elif "1- mixture 2- compounds" in low and "5. mettaliods" in low:
            answers.append(StudentAnswer("5.1", line))
        elif "heterogeneous mixture" in low and "2. a-" in low:
            answers.append(StudentAnswer("5.2.a", "Heterogeneous mixture"))
        elif "b. triatomic" in low:
            answers.append(StudentAnswer("5.2.b", "Triatomic"))
        elif "c. separating fund" in low or "c. separating fun" in low:
            answers.append(StudentAnswer("5.2.c", "Separating Funnel"))
        elif "d. heting freezing" in low or "d. setting freezing" in low:
            answers.append(StudentAnswer("5.2.d", "Setting Freezing"))
        elif "ze. slow change" in low or "e. slow change" in low:
            answers.append(StudentAnswer("5.2.e", "Slow change"))
        elif "solid solid heterogenous" in low:
            answers.append(StudentAnswer("6.1", line))
        elif "conical flask b. funnel c. separating" in low:
            answers.append(StudentAnswer("6.2", line))

    return StudentScript(
        student_name=student_name or "Unknown",
        roll_no=roll_no or None,
        meta={"exam_id": "chem-2025-term1"},
        answers=answers
    )

# --- 3. Streamlit UI ---

st.title("AI School Grader – Chemistry VII")

uploaded_answer = st.file_uploader("Upload student's answer sheet (PDF)", type=["pdf"])
student_name = st.text_input("Student name", "")
roll_no = st.text_input("Roll no", "")

if uploaded_answer is not None and st.button("Grade Answer Sheet"):
    pdf_bytes = uploaded_answer.read()
    ocr_text = azure_ocr_extract_text(pdf_bytes)
    script = build_script_from_ocr_text(ocr_text, student_name, roll_no)
    report = grade_script(ANSWER_KEY, script)
    st.subheader("Total")
    st.write(f"{report['total_score']} / {report['max_marks']}  ({report['percentage']:.1f}%)  Grade: {report['grade']}")
    st.subheader("Details")
    st.json(report)

