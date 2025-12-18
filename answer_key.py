# answer_key.py
from dataclasses import dataclass
from typing import Literal, Optional, Dict, List

QType = Literal[
    "mcq", "true_false", "fill", "symbol",
    "short_def", "reason", "classify",
    "differentiate", "flowchart", "short_direct"
]

@dataclass
class QuestionSpec:
    id: str
    text: str
    q_type: QType
    max_marks: float
    options: Optional[List[str]] = None           # for mcq
    correct_option_text: Optional[str] = None     # for mcq
    correct_value: Optional[str] = None           # for non-mcq
    model_answer: Optional[str] = None            # ideal answer
    notes: Optional[str] = None                   # for partial-mark rules

ANSWER_KEY: Dict[str, QuestionSpec] = {
    # SECTION A – Q1 MCQ (1 mark each)
    "1.1": QuestionSpec(
        id="1.1",
        text="Solids do not diffuse because",
        q_type="mcq", max_marks=1.0,
        options=[
            "They have many free surfaces",
            "They lack intermolecular spaces",
            "They have a high density",
            "All of the above",
        ],
        correct_option_text="They lack intermolecular spaces",
        model_answer="Solids do not diffuse because they lack intermolecular spaces.",
    ),
    "1.2": QuestionSpec(
        id="1.2",
        text="Diffusion is the movement of particles from the region of their",
        q_type="mcq", max_marks=1.0,
        options=[
            "Higher to lower concentration",
            "Lower to higher concentration",
            "Both A and B",
            "None of these",
        ],
        correct_option_text="Higher to lower concentration",
    ),
    "1.3": QuestionSpec(
        id="1.3",
        text="When ice melts, heat is",
        q_type="mcq", max_marks=1.0,
        options=["Given out", "Taken in", "Unchanged", "Deposited"],
        correct_option_text="Taken in",
    ),
    "1.4": QuestionSpec(
        id="1.4",
        text="In water, the molecules pull together into a spherical shape due to the force of",
        q_type="mcq", max_marks=1.0,
        options=["Gravity", "Cohesion", "Adhesion", "Magnetism"],
        correct_option_text="Cohesion",
    ),
    "1.5": QuestionSpec(
        id="1.5",
        text="Which of the following can be described as being fluid?",
        q_type="mcq", max_marks=1.0,
        options=["Solids", "Liquids", "Gases", "Both b and c"],
        correct_option_text="Both b and c",
    ),
    "1.6": QuestionSpec(
        id="1.6",
        text="Growth of a crystal is an example of",
        q_type="mcq", max_marks=1.0,
        options=["Periodic change", "Irreversible change", "Physical change", "Chemical change"],
        correct_option_text="Physical change",
    ),
    "1.7": QuestionSpec(
        id="1.7",
        text="The state through which a substance does not pass during sublimation",
        q_type="mcq", max_marks=1.0,
        options=["solid", "liquid", "gas", "none of the above"],
        correct_option_text="liquid",
    ),
    "1.8": QuestionSpec(
        id="1.8",
        text="The smallest unit of matter is called",
        q_type="mcq", max_marks=1.0,
        options=["molecules", "compounds", "atoms", "mixtures"],
        correct_option_text="atoms",
    ),
    "1.9": QuestionSpec(
        id="1.9",
        text="An example of a photochemical reaction is",
        q_type="mcq", max_marks=1.0,
        options=["Respiration", "Electrolysis", "Photosynthesis", "Galvanisation"],
        correct_option_text="Photosynthesis",
    ),
    "1.10": QuestionSpec(
        id="1.10",
        text="The burning of magnesium is",
        q_type="mcq", max_marks=1.0,
        options=["A fast change", "Slow change", "Periodic change", "Seasonal change"],
        correct_option_text="A fast change",
    ),
    "1.11": QuestionSpec(
        id="1.11",
        text="Which of the following is a liquid metal?",
        q_type="mcq", max_marks=1.0,
        options=["Oxygen", "Carbon dioxide", "Chlorine", "Mercury"],
        correct_option_text="Mercury",
    ),
    "1.12": QuestionSpec(
        id="1.12",
        text="When salt dissolves in water it loses its",
        q_type="mcq", max_marks=1.0,
        options=["Salty taste", "Crystalline shape", "Neither a nor b", "All of these"],
        correct_option_text="Crystalline shape",
    ),
    "1.13": QuestionSpec(
        id="1.13",
        text="Which of the following element is triatomic?",
        q_type="mcq", max_marks=1.0,
        options=["Phosphorus", "Argon", "Ozone", "Chlorine"],
        correct_option_text="Ozone",
    ),
    "1.14": QuestionSpec(
        id="1.14",
        text="Which of the following is NOT a homogeneous mixture?",
        q_type="mcq", max_marks=1.0,
        options=["Alcohol + water", "Gunpowder", "Ammonia + hydrogen", "Sulphur + carbon disulphide"],
        correct_option_text="Gunpowder",
    ),
    "1.15": QuestionSpec(
        id="1.15",
        text="When iron and sulphur are mixed and heated together, the product formed is a",
        q_type="mcq", max_marks=1.0,
        options=["Mixture", "Compound", "Element", "None of these"],
        correct_option_text="Compound",
    ),

    # SECTION A – Q2(i) True/False (1 mark each)
    "2(i).1": QuestionSpec(
        id="2(i).1",
        text="Bromine is a liquid metal.",
        q_type="true_false", max_marks=1.0,
        correct_value="false",
        model_answer="Bromine is a liquid non-metal.",
    ),
    "2(i).2": QuestionSpec(
        id="2(i).2",
        text="The symbol of potassium is P.",
        q_type="true_false", max_marks=1.0,
        correct_value="false",
        model_answer="Symbol of potassium is K.",
    ),
    "2(i).3": QuestionSpec(
        id="2(i).3",
        text="The formation of paneer is an example of a precipitation reaction.",
        q_type="true_false", max_marks=1.0,
        correct_value="true",
    ),
    "2(i).4": QuestionSpec(
        id="2(i).4",
        text="The properties of a compound are same as those of its constituent elements.",
        q_type="true_false", max_marks=1.0,
        correct_value="false",
    ),
    "2(i).5": QuestionSpec(
        id="2(i).5",
        text="Hydrogen gas burns with a 'pop' sound.",
        q_type="true_false", max_marks=1.0,
        correct_value="true",
    ),

    # Q2(ii) Fill (1 mark each)
    "2(ii).1": QuestionSpec(
        id="2(ii).1",
        text="In a ______ change no new substance is formed.",
        q_type="fill", max_marks=1.0,
        correct_value="physical",
    ),
    "2(ii).2": QuestionSpec(
        id="2(ii).2",
        text="For rusting of iron ______ and ______ are required.",
        q_type="fill", max_marks=1.0,
        correct_value="oxygen and water",
    ),
    "2(ii).3": QuestionSpec(
        id="2(ii).3",
        text="Water molecule is made up of ____ atoms.",
        q_type="fill", max_marks=1.0,
        correct_value="3",
    ),
    "2(ii).4": QuestionSpec(
        id="2(ii).4",
        text="Same kind of atoms make up ______.",
        q_type="fill", max_marks=1.0,
        correct_value="elements",
    ),
    "2(ii).5": QuestionSpec(
        id="2(ii).5",
        text="The decomposition of water molecules into hydrogen and oxygen gas is an example of ______.",
        q_type="fill", max_marks=1.0,
        correct_value="electrolysis",
    ),

    # Q2(iii) Symbols (1 mark each)
    "2(iii).1": QuestionSpec(
        id="2(iii).1",
        text="Symbol of Hydrogen",
        q_type="symbol", max_marks=1.0,
        correct_value="h",
    ),
    "2(iii).2": QuestionSpec(
        id="2(iii).2",
        text="Symbol of Chlorine",
        q_type="symbol", max_marks=1.0,
        correct_value="cl",
    ),
    "2(iii).3": QuestionSpec(
        id="2(iii).3",
        text="Symbol of Phosphorus",
        q_type="symbol", max_marks=1.0,
        correct_value="p",
    ),
    "2(iii).4": QuestionSpec(
        id="2(iii).4",
        text="Symbol of Magnesium",
        q_type="symbol", max_marks=1.0,
        correct_value="mg",
    ),
    "2(iii).5": QuestionSpec(
        id="2(iii).5",
        text="Symbol of Iron",
        q_type="symbol", max_marks=1.0,
        correct_value="fe",
    ),

    # Q2(iv) Explain terms (1 mark each) – all full marks for Roman [file:2]
    "2(iv).1": QuestionSpec(
        id="2(iv).1",
        text="Explain: Evaporation",
        q_type="short_def", max_marks=1.0,
        model_answer="Liquid changing to vapour at the surface below boiling point.",
    ),
    "2(iv).2": QuestionSpec(
        id="2(iv).2",
        text="Explain: Endothermic reaction",
        q_type="short_def", max_marks=1.0,
        model_answer="Chemical reaction in which heat is absorbed.",
    ),
    "2(iv).3": QuestionSpec(
        id="2(iv).3",
        text="Explain: Physical change",
        q_type="short_def", max_marks=1.0,
        model_answer="No new substance formed; usually reversible; may involve heating or cooling.",
    ),
    "2(iv).4": QuestionSpec(
        id="2(iv).4",
        text="Explain: Metalloid",
        q_type="short_def", max_marks=1.0,
        model_answer="Element with properties of both metals and non-metals.",
    ),
    "2(iv).5": QuestionSpec(
        id="2(iv).5",
        text="Explain: Homogeneous mixture",
        q_type="short_def", max_marks=1.0,
        model_answer="Mixture whose components are uniformly distributed and cannot be seen separately.",
    ),

    # Q2(v) classify (0.5 each, total 5 marks) [file:2]
    "2(v).1": QuestionSpec(id="2(v).1", text="Aluminium", q_type="classify", max_marks=0.5, correct_value="element"),
    "2(v).2": QuestionSpec(id="2(v).2", text="Copper sulphate", q_type="classify", max_marks=0.5, correct_value="compound"),
    "2(v).3": QuestionSpec(id="2(v).3", text="Saliva", q_type="classify", max_marks=0.5, correct_value="mixture"),
    "2(v).4": QuestionSpec(id="2(v).4", text="Ammonia", q_type="classify", max_marks=0.5, correct_value="compound"),
    "2(v).5": QuestionSpec(id="2(v).5", text="Blood", q_type="classify", max_marks=0.5, correct_value="mixture"),
    "2(v).6": QuestionSpec(id="2(v).6", text="Honey", q_type="classify", max_marks=0.5, correct_value="mixture"),
    "2(v).7": QuestionSpec(id="2(v).7", text="Gold", q_type="classify", max_marks=0.5, correct_value="element"),
    # 2(v).8 duplicate Ammonia accepted as mixture [file:2]
    "2(v).8": QuestionSpec(id="2(v).8", text="Ammonia (duplicate)", q_type="classify", max_marks=0.5, correct_value="mixture"),
    "2(v).9": QuestionSpec(id="2(v).9", text="Glucose", q_type="classify", max_marks=0.5, correct_value="compound"),
    "2(v).10": QuestionSpec(id="2(v).10", text="Bread", q_type="classify", max_marks=0.5, correct_value="mixture"),

    # SECTION B – Q3.1 differentiate (1 mark each, with partials) [file:2]
    "3.1.a": QuestionSpec(
        id="3.1.a",
        text="Differentiate: Solids and liquids [density]",
        q_type="differentiate", max_marks=1.0,
        model_answer="Solids have higher density; liquids have lower density.",
    ),
    "3.1.b": QuestionSpec(
        id="3.1.b",
        text="Differentiate: Elements and compounds [definition]",
        q_type="differentiate", max_marks=1.0,
        model_answer="Element: pure substance made of one kind of atom. Compound: pure substance of two or more elements in fixed ratio.",
        notes="Roman got 0.5 because he called compounds 'pure homogeneous substances'; award 0.5 when element correct and compound nearly correct.",
    ),
    "3.1.c": QuestionSpec(
        id="3.1.c",
        text="Differentiate: Periodic and non-periodic change [example]",
        q_type="differentiate", max_marks=1.0,
        model_answer="Periodic: day and night; Non-periodic: volcanic eruption.",
    ),
    "3.1.d": QuestionSpec(
        id="3.1.d",
        text="Differentiate: Monoatomic and diatomic molecules [No. of atoms]",
        q_type="differentiate", max_marks=1.0,
        model_answer="Monoatomic: 1 atom; diatomic: 2 atoms.",
    ),
    "3.1.e": QuestionSpec(
        id="3.1.e",
        text="Differentiate: Compounds and mixtures [Separation method]",
        q_type="differentiate", max_marks=1.0,
        model_answer="Compounds are separated by chemical means; mixtures by physical methods such as filtration, distillation, etc.",
        notes="Roman got 0.5: gave only 'mixtures - separating funnel', incomplete.",
    ),

    # Q3.2 reasons (all 1 mark, all correct for Roman) [file:2]
    "3.2.a": QuestionSpec(
        id="3.2.a",
        text="Give reason: Pumice stone floats on water",
        q_type="reason", max_marks=1.0,
        model_answer="Because it has air spaces, making it less dense than water.",
    ),
    "3.2.b": QuestionSpec(
        id="3.2.b",
        text="Give reason: Burning is an exothermic reaction",
        q_type="reason", max_marks=1.0,
        model_answer="Because burning gives out heat.",
    ),
    "3.2.c": QuestionSpec(
        id="3.2.c",
        text="Give reason: Solids are generally very rigid",
        q_type="reason", max_marks=1.0,
        model_answer="Because their particles are closely packed.",
    ),
    "3.2.d": QuestionSpec(
        id="3.2.d",
        text="Give reason: Burning of candle wax is both physical and chemical change",
        q_type="reason", max_marks=1.0,
        model_answer="Melting of wax is physical; burning wax to give heat, light and CO2 is chemical.",
    ),
    "3.2.e": QuestionSpec(
        id="3.2.e",
        text="Give reason: Mixture is an impure substance",
        q_type="reason", max_marks=1.0,
        model_answer="Because it contains two or more substances in any ratio.",
    ),

    # Q4.1 separation techniques (1 mark each) [file:2]
    "4.1.a": QuestionSpec(
        id="4.1.a",
        text="Ammonium chloride and common salt",
        q_type="short_direct", max_marks=1.0,
        correct_value="sublimation",
    ),
    "4.1.b": QuestionSpec(
        id="4.1.b",
        text="Water and kerosene oil",
        q_type="short_direct", max_marks=1.0,
        correct_value="separating funnel",
    ),
    "4.1.c": QuestionSpec(
        id="4.1.c",
        text="Chalk and water",
        q_type="short_direct", max_marks=1.0,
        correct_value="filtration",
    ),
    "4.1.d": QuestionSpec(
        id="4.1.d",
        text="Salt and water",
        q_type="short_direct", max_marks=1.0,
        correct_value="evaporation",
    ),
    "4.1.e": QuestionSpec(
        id="4.1.e",
        text="Saw dust and water",
        q_type="short_direct", max_marks=1.0,
        correct_value="filtration",
    ),

    # Q4.2 filtration diagram (2+1+1+1 = 5 marks) [file:2]
    "4.2.a": QuestionSpec(
        id="4.2.a",
        text="Identify A and B in filtration setup",
        q_type="short_direct", max_marks=2.0,
        correct_value="residue and water",
        model_answer="A is residue; B is water (filtrate).",
    ),
    "4.2.b": QuestionSpec(
        id="4.2.b",
        text="Is water an element or a compound?",
        q_type="short_direct", max_marks=1.0,
        correct_value="compound",
    ),
    "4.2.c": QuestionSpec(
        id="4.2.c",
        text="Why is a solution of salt and water not separated by this method?",
        q_type="reason", max_marks=1.0,
        model_answer="Because salt and water form a homogeneous solution which cannot be separated by filtration.",
    ),
    "4.2.d": QuestionSpec(
        id="4.2.d",
        text="Write the chemical formula of water.",
        q_type="short_direct", max_marks=1.0,
        correct_value="h2o",
    ),

    # Q5.1 flow chart (5 marks, 5 blanks) [file:2]
    "5.1.1": QuestionSpec(
        id="5.1.1",
        text="Flowchart blank 1",
        q_type="flowchart", max_marks=1.0,
        correct_value="mixture",
    ),
    "5.1.2": QuestionSpec(
        id="5.1.2",
        text="Flowchart blank 2",
        q_type="flowchart", max_marks=1.0,
        correct_value="compounds",
    ),
    "5.1.3": QuestionSpec(
        id="5.1.3",
        text="Flowchart blank 3",
        q_type="flowchart", max_marks=1.0,
        correct_value="heterogeneous",
    ),
    "5.1.4": QuestionSpec(
        id="5.1.4",
        text="Flowchart blank 4",
        q_type="flowchart", max_marks=1.0,
        correct_value="non-metals",
    ),
    "5.1.5": QuestionSpec(
        id="5.1.5",
        text="Flowchart blank 5",
        q_type="flowchart", max_marks=1.0,
        correct_value="metalloids",
    ),

    # Q5.2 short-direct (1 mark each) [file:2]
    "5.2.a": QuestionSpec(
        id="5.2.a",
        text="The mixture in which particles can be seen easily",
        q_type="short_direct", max_marks=1.0,
        correct_value="heterogeneous mixture",
    ),
    "5.2.b": QuestionSpec(
        id="5.2.b",
        text="A molecule which contains three atoms",
        q_type="short_direct", max_marks=1.0,
        correct_value="triatomic",
    ),
    "5.2.c": QuestionSpec(
        id="5.2.c",
        text="The apparatus used to separate immiscible liquid mixture of different densities",
        q_type="short_direct", max_marks=1.0,
        correct_value="separating funnel",
    ),
    "5.2.d": QuestionSpec(
        id="5.2.d",
        text="The change of matter liquid state to solid state at a fixed temperature",
        q_type="short_direct", max_marks=1.0,
        correct_value="freezing",
    ),
    "5.2.e": QuestionSpec(
        id="5.2.e",
        text="A change which takes place over a long period of time",
        q_type="short_direct", max_marks=1.0,
        correct_value="slow change",
    ),

    # Q6.1 – 3 marks (teacher-added) [file:2]
    "6.1.a": QuestionSpec(
        id="6.1.a",
        text="Nature of mixture of iron and sulphur",
        q_type="short_direct", max_marks=1.0,
        correct_value="solid-solid heterogeneous",
    ),
    "6.1.b": QuestionSpec(
        id="6.1.b",
        text="Which component is attracted by magnet after making compound?",
        q_type="short_direct", max_marks=1.0,
        correct_value="iron",
    ),
    "6.1.c": QuestionSpec(
        id="6.1.c",
        text="Behaviour of iron and sulphur with magnet after forming compound",
        q_type="short_direct", max_marks=1.0,
        correct_value="both iron and sulphur are not attracted to the magnet",
    ),

    # Q6.2 – 6 marks (identify apparatus) [file:2]
    "6.2.a": QuestionSpec(id="6.2.a", text="Identify apparatus a", q_type="short_direct", max_marks=1.0, correct_value="conical flask"),
    "6.2.b": QuestionSpec(id="6.2.b", text="Identify apparatus b", q_type="short_direct", max_marks=1.0, correct_value="funnel"),
    "6.2.c": QuestionSpec(id="6.2.c", text="Identify apparatus c", q_type="short_direct", max_marks=1.0, correct_value="separating funnel"),
    "6.2.d": QuestionSpec(id="6.2.d", text="Identify apparatus d", q_type="short_direct", max_marks=1.0, correct_value="watch glass"),
    "6.2.e": QuestionSpec(id="6.2.e", text="Identify apparatus e", q_type="short_direct", max_marks=1.0, correct_value="round bottomed flask"),
    "6.2.f": QuestionSpec(id="6.2.f", text="Identify apparatus f", q_type="short_direct", max_marks=1.0, correct_value="test tube holder"),
}
