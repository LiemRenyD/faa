from enum import Enum

class QuestionType(Enum):
    SINGLE = "单选题"
    MULTIPLE = "多选题"
    FILL = "填空题"
    JUDGE = "判断题"