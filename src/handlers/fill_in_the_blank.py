from .base import BaseHandler
from src.config import settings

class FillBlankHandler(BaseHandler):
    def execute(self, page, question):
        # 处理答案：将逗号分隔的字符串转换为列表
        if isinstance(question.answer, str):
            # 按逗号分割，并去除每个答案的前后空格
            answers = [ans.strip() for ans in question.answer.split(',')]
        elif isinstance(question.answer, list):
            answers = question.answer
        else:
            answers = [str(question.answer)] if question.answer else []
        
        inputs = page.locator(".blank-item input").all()
        
        for i, ipt in enumerate(inputs):
            val = str(answers[i]) if i < len(answers) and answers[i] else " "
            ipt.fill(val)
            page.wait_for_timeout(settings.answer_interval)
            
        page.wait_for_timeout(1500)
        submit = page.locator("#mult-submit")
        if submit.is_visible(): submit.click()