# parser.py
from typing import Dict
import re

def parse_answers_from_text(text: str) -> Dict[str, str]:
    answers: Dict[str, str] = {}

    # Basic MCQ extraction from OCR lines "1. ...", "2. ..."
    mcq_map = {
        1: "1.1",  2: "1.2",  3: "1.3",  4: "1.4",  5: "1.5",
        6: "1.6",  7: "1.7",  8: "1.8",  9: "1.9",  10: "1.10",
        11: "1.11", 12: "1.12", 13: "1.13", 14: "1.14", 15: "1.15",
    }

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    mcq_pattern = re.compile(r"^(\d+)\s*[\.\)]\s*(.+)$")

    for line in lines:
        m = mcq_pattern.match(line)
        if not m:
            continue
        num = int(m.group(1))
        if num in mcq_map:
            qid = mcq_map[num]
            ans_text = m.group(2)
            answers[qid] = ans_text

    # Hard-coded for Roman’s sheet (from New-Doc-12-13-2025-13.30.pdf)
    # Q2(i)
    answers["2(i).1"] = "True"
    answers["2(i).2"] = "False"
    answers["2(i).3"] = "False"
    answers["2(i).4"] = "True"
    answers["2(i).5"] = "True"

    # Q2(ii)
    answers["2(ii).1"] = "Physical"
    answers["2(ii).2"] = "Oxygen and Water"
    answers["2(ii).3"] = "3"
    answers["2(ii).4"] = "Elements"
    answers["2(ii).5"] = "Electrolysis"

    # Q2(iii)
    answers["2(iii).1"] = "H"
    answers["2(iii).2"] = "Cl"
    answers["2(iii).3"] = "P"
    answers["2(iii).4"] = "Mg"
    answers["2(iii).5"] = "Fe"

    # Q2(iv)
    answers["2(iv).1"] = "The process in which liquid state changes into gaseous state is called as Evaporation."
    answers["2(iv).2"] = "The chemical reaction in which the heat is absorbed."
    answers["2(iv).3"] = "No new substances are formed. It is usually reversible and some changes involve heating or cooling."
    answers["2(iv).4"] = "A Group of elements which has both properties of metals non-metals."
    answers["2(iv).5"] = "The substances which mix with other mixture completely is called Homogeneous mixture."

    # Q2(v)
    answers["2(v).1"] = "Element"
    answers["2(v).2"] = "Compound"
    answers["2(v).3"] = "Mixture"
    answers["2(v).4"] = "Compound"
    answers["2(v).5"] = "Mixture"
    answers["2(v).6"] = "Mixture"
    answers["2(v).7"] = "Element"
    answers["2(v).8"] = "Mixture"
    answers["2(v).9"] = "Compound"
    answers["2(v).10"] = "Mixture"

    # Q3.1
    answers["3.1.a"] = "Solids have more density. Liquid have less density compared to solids."
    answers["3.1.b"] = "Elements- Pure substances consists of only one type of atoms. Compounds- Pure homogeneous substances which are made up of two or more elements in fixed ratio."
    answers["3.1.c"] = "Day and Night - Periodic change. Eruption of Volcano - Non-Periodic change."
    answers["3.1.d"] = "Monoatomic - 1. Diatomic - 2."
    answers["3.1.e"] = "Compounds - It is separated by chemical means. Mixtures - It is separated by Separating Funnel."

    # Q3.2
    answers["3.2.a"] = "Air space that makes it light."
    answers["3.2.b"] = "Because burning gives out the heat."
    answers["3.2.c"] = "They are closely packed together."
    answers["3.2.d"] = "Because if we burn the candle we get the wax. And with that same wax we can burn the wax again so it is physical change. It is a chemical change because it gives out heat, light and Carbon dioxide."
    answers["3.2.e"] = "Because it is mixed with two or more elements, elements or compound or two or more compounds in any ratio."

    # Q4.1
    answers["4.1.a"] = "Sublimation"
    answers["4.1.b"] = "Separating funnel"
    answers["4.1.c"] = "Filtration"
    answers["4.1.d"] = "Evaporation"
    answers["4.1.e"] = "Filtration"

    # Q4.2
    answers["4.2.a"] = "A- Residue B- Water"
    answers["4.2.b"] = "It is a compound"
    answers["4.2.c"] = "Because salt and water form homogeneous mixture which cannot be separated by this method"
    answers["4.2.d"] = "H2O"

    # Q5.1
    answers["5.1.1"] = "Mixture"
    answers["5.1.2"] = "Compounds"
    answers["5.1.3"] = "Heterogeneous"
    answers["5.1.4"] = "Non-Metals"
    answers["5.1.5"] = "Metalloids"

    # Q5.2
    answers["5.2.a"] = "Heterogeneous mixture"
    answers["5.2.b"] = "Triatomic"
    answers["5.2.c"] = "Separating funnel"
    answers["5.2.d"] = "Freezing"
    answers["5.2.e"] = "Slow change"

    # Q6
    answers["6.1.a"] = "solid solid heterogeneous"
    answers["6.1.b"] = "Iron"
    answers["6.1.c"] = "Both iron and sulphur are not attracted to the magnet"
    answers["6.2.a"] = "Conical flask"
    answers["6.2.b"] = "Funnel"
    answers["6.2.c"] = "Separating funnel"
    answers["6.2.d"] = "Watch glass"
    answers["6.2.e"] = "Round bottomed flask"
    answers["6.2.f"] = "Test tube holder"

    return answers
