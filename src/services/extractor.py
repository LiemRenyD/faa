from src.models.question import Question
from src.models.enums import QuestionType

class APIQuestionParser:
    @staticmethod
    def parse(raw_data: dict) -> Question:
        type_map = {1: QuestionType.MULTIPLE, 2: QuestionType.FILL, 7: QuestionType.JUDGE}
        q_type = type_map.get(raw_data.get("type"), QuestionType.SINGLE)
        
        options = []
        for k in ["optionA", "optionB", "optionC", "optionD"]:
            if raw_data.get(k): options.append(raw_data[k])
            
        return Question(
            id=str(raw_data.get("questionId")),
            content=raw_data.get("topic", ""),
            type=q_type,
            options=options,
            blanks_count=raw_data.get("answerNum", 0)
        )