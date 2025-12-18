from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class StudentAnswer:
    question_id: str
    answer: str

@dataclass
class StudentScript:
    student_name: str
    roll_no: Optional[str]
    meta: Dict[str, Any]
    answers: List[StudentAnswer]
