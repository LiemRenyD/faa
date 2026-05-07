import json
from src.models.question import Question

class AnswerFinder:
    def __init__(self, db_path="data/question_bank.json"):
        self.db_path = db_path
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 将题库转换为以 question_id 为键的字典，提高查找效率
            self.bank = {}
            questions_list = data.get("questions", [])
            for q in questions_list:
                qid = q.get("question_id")
                if qid:
                    self.bank[qid] = q.get("answer")
                # 同时支持通过题干内容查找
                qtext = q.get("question_text")
                if qtext:
                    self.bank[qtext] = q.get("answer")

    def find_answer(self, question: Question) -> Question:
        # 优先通过 ID 查找，其次通过题干内容
        ans = self.bank.get(question.id) or self.bank.get(question.content)
        if ans:
            question.answer = ans
            print(f"✅ 找到答案: {ans}")
        else:
            print(f"❌ 未找到答案 - ID: {question.id}, 内容: {question.content[:50]}...")
        return question