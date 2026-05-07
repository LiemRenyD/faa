from pydantic import BaseModel
from typing import List, Optional, Union
from .enums import QuestionType

class Question(BaseModel):
    id: str
    content: str
    type: QuestionType
    options: List[str] = []
    answer: Optional[Union[str, List[str]]] = None
    blanks_count: int = 0