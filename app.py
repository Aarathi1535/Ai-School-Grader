import json
import streamlit as st

from grader_core import load_answer_key, grade_script
from student_answers_schema import StudentScript, StudentAnswer

st.title("AI School Grader")

# Load answer key once
ANSWER_KEY = load_answer_key("answer_key.json")

# For now, hard-code Roman's answers from OCR (you can replace with Azure OCR mapping) [file:3]
def build_roman_script() -> StudentScript:
    answers = [
        StudentAnswer("1.1", "They lack intermolecular spaces"),
        StudentAnswer("1.2", "Higher to lower concentration"),
        StudentAnswer("1.3", "Taken in"),
        StudentAnswer("1.4", "Cohesion"),
        StudentAnswer("1.5", "Both (b) and (c)"),
        StudentAnswer("1.6", "Physical change"),
        StudentAnswer("1.7", "liquids"),
        StudentAnswer("1.8", "atoms"),
        StudentAnswer("1.9", "Photosynthesis"),
        StudentAnswer("1.10", "A fast change"),
        StudentAnswer("1.11", "Mercury"),
        StudentAnswer("1.12", "Crystalline shape"),
        StudentAnswer("1.13", "Ozone"),
        StudentAnswer("1.14", "Gunpowder"),
        StudentAnswer("1.15", "Compound"),
        StudentAnswer("2.i.1", "True"),
        StudentAnswer("2.i.2", "False"),
        StudentAnswer("2.i.3", "False"),
        StudentAnswer("2.i.4", "True"),
        StudentAnswer("2.i.5", "True"),
        StudentAnswer("2.ii.1", "Physical"),
        StudentAnswer("2.ii.2", "Oxygen and Water"),
        StudentAnswer("2.ii.3", "3"),
        StudentAnswer("2.ii.4", "Elements"),
        StudentAnswer("2.ii.5", "Electrolysis"),
        StudentAnswer("2.iii.1", "H"),
        StudentAnswer("2.iii.2", "Cl"),
        StudentAnswer("2.iii.3", "P"),
        StudentAnswer("2.iii.4", "Mg"),
        StudentAnswer("2.iii.5", "Fe"),
        StudentAnswer("2.iv.1", "The process in which liquid state changes into gaseous state is called as Evaporation."),
        StudentAnswer("2.iv.2", "The chemical reaction in which the heat is absorbed."),
        StudentAnswer("2.iv.3", "No new substances are formed. It is usually reversible and some changes involve heating or cooling."),
        StudentAnswer("2.iv.4", "A group of elements which has both properties of metals and non-metals."),
        StudentAnswer("2.iv.5", "The substances which mix with other mixture completely is called Homogeneous mixture."),
        StudentAnswer("2.v.1", "Elements"),
        StudentAnswer("2.v.2", "Compound"),
        StudentAnswer("2.v.3", "Mixture"),
        StudentAnswer("2.v.4", "Compound"),
        StudentAnswer("2.v.5", "Mixture"),
        StudentAnswer("2.v.6", "Mixture"),
        StudentAnswer("2.v.7", "Element"),
        StudentAnswer("2.v.8", "Mixture"),
        StudentAnswer("2.v.9", "Compound"),
        StudentAnswer("2.v.10", "Mixture"),
        StudentAnswer("3.1.a", "Solids have more density. Liquid have less density compared to solids."),
        StudentAnswer("3.1.b", "Elements- Pure substances consists of only one type of atoms. Compounds- Pure homogeneous substances which are made up of two or more elements in fixed ratio."),
        StudentAnswer("3.1.c", "Day and Night - Periodic change. Eruption of Volcano - Non-Periodic change."),
        StudentAnswer("3.1.d", "Monoatomic - 1. Diatomic - 2."),
        StudentAnswer("3.1.e", "Compounds - It is separated by chemical means. Mixtures - It is separated by Separating Funnel"),
        StudentAnswer("3.2.a", "Air space that makes it light."),
        StudentAnswer("3.2.b", "Because burning gives out the heat."),
        StudentAnswer("3.2.c", "They are closely packed together."),
        StudentAnswer("3.2.d", "Because if we burn the candle we get the wax. And with that same wax we can burn the wax again so it is physical change. It is a chemical change because it gives out heat, light and Carbon dioxide."),
        StudentAnswer("3.2.e", "Because it is mixed with two or more elements, elements or compound or two or more compounds in any ratio."),
        StudentAnswer("4.1.a", "Sublimation"),
        StudentAnswer("4.1.b", "Separating funnel"),
        StudentAnswer("4.1.c", "Filtration"),
        StudentAnswer("4.1.d", "Evaporation"),
        StudentAnswer("4.1.e", "Filtration"),
        StudentAnswer("4.2.a", "A- Residue B- Water"),
        StudentAnswer("4.2.b", "It is a compound"),
        StudentAnswer("4.2.c", "Because salt and water form homogeneous mixture which cannot be separated by this method"),
        StudentAnswer("4.2.d", "H2O"),
        StudentAnswer("5.1", "1- Mixture, 2- Compounds, 3- Heterogeneous, 4- Non-Metals, 5- Metalloids"),
        StudentAnswer("5.2.a", "Heterogeneous mixture"),
        StudentAnswer("5.2.b", "Triatomic"),
        StudentAnswer("5.2.c", "Separating Funnel"),
        StudentAnswer("5.2.d", "Setting Freezing"),
        StudentAnswer("5.2.e", "Slow change"),
        StudentAnswer("6.1", "a. solid-solid heterogeneous b. Iron c. Both iron and sulphur are not attracted to the magnet"),
        StudentAnswer("6.2", "a. Conical flask b. Funnel c. Separating funnel d. Watch glass e. Round bottomed flask glass f. Test tube holder")
    ]
    return StudentScript(
        student_name="Roman Manuel",
        roll_no="33",
        meta={"exam_id": "chem-2025-term1"},
        answers=answers
    )

if st.button("Grade Roman's Script"):
    script = build_roman_script()
    report = grade_script(ANSWER_KEY, script)
    st.subheader("Total")
    st.write(f"{report['total_score']} / {report['max_marks']}  ({report['percentage']:.1f}%)  Grade: {report['grade']}")
    st.subheader("Details")
    st.json(report)
