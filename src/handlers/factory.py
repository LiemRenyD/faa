from .multiple_choice import MultipleChoiceHandler
from .fill_in_the_blank import FillBlankHandler
from .true_false import TrueFalseHandler
from src.models.enums import QuestionType

class QuestionHandlerFactory:
    _mapping = {
        QuestionType.SINGLE: MultipleChoiceHandler,
        QuestionType.MULTIPLE: MultipleChoiceHandler,
        QuestionType.FILL: FillBlankHandler,
        QuestionType.JUDGE: TrueFalseHandler
    }

    @classmethod
    def get_handler(cls, q_type):
        return cls._mapping.get(q_type, MultipleChoiceHandler)()