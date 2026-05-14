# src/services/loop_controller.py
from src.config import settings
from src.services.extractor import APIQuestionParser
from src.storage.finder import AnswerFinder
from src.handlers.factory import QuestionHandlerFactory

class LoopController:  # <--- 确保这一行存在且拼写正确
    def __init__(self, page):
        self.page = page
        self.finder = AnswerFinder()
        self.is_first_question = True

    def run(self):
        total_score = 0
        for i in range(settings.max_rounds):
            print(f"--- 第 {i+1} 轮开始 (当前总分: {total_score}) ---")
            # 获取本轮新增的分数和是否退出的信号
            should_exit, round_score = self._answer_single_round(total_score)
            
            total_score += round_score  # 累加本轮得分
            
            if should_exit:
                print(f"🏁 流程结束，最终得分: {total_score}")
                break
            
            self.is_first_question = True  # 每一轮结束重置标识

    def _answer_single_round(self, current_total_score):
        question_count = 0
        round_score = 0  # 记录本轮新增的分数
        
        while True:
            try:
                # ... existing code ...
                with self.page.expect_response("**/getPracticeQuestion*", timeout=10000) as resp_info:
                    if self.is_first_question:
                        print("🌐 正在进入答题页面...")
                        self.page.goto(settings.question_url)
                        self.is_first_question = False
                    else:
                        pass
                
                resp = resp_info.value
                data = resp.json()
                
                if data.get("result") != 1:
                    print(f"🏁 轮次可能已结束: {data.get('msg')}")
                    break
                    
                raw_data = data.get("data", {})
                question = APIQuestionParser.parse(raw_data)
                
                print(f"📝 正在处理题号: {question.id}")
                
                question = self.finder.find_answer(question)
                
                handler = QuestionHandlerFactory.get_handler(question.type)
                handler.execute(self.page, question)

                # 计算本题得分
                score_increment = 2 if question.type.value in ['填空题'] else 1
                round_score += score_increment  # 只增加本轮分数
                
                # 计算实时总分用于显示和判断
                real_time_score = current_total_score + round_score
                print(f"💰 本题+{score_increment} | 本轮累计: {round_score} | 预计总分: {real_time_score}/{settings.end_score}")
                
                self.page.wait_for_timeout(settings.answer_interval)
                
                question_count += 1
                print(f"📊 本轮已答题数: {question_count}/{settings.questionlimit}")

                # 检查是否达到目标总分
                if real_time_score >= settings.end_score:
                    print(f"🎉 恭喜！总分已达到 {settings.end_score}，提前结束整个流程")
                    self.page.wait_for_timeout(5000)
                    return True, round_score  # 返回本轮得分
                
                # 检查是否达到每轮题目上限
                if question_count >= settings.questionlimit:
                    self.page.wait_for_timeout(5000)
                    print(f"✅ 本轮结束，本轮得分: {round_score}")
                    return False, round_score
                
            except Exception as e:
                print(f"⚠️ 循环捕获到异常: {e}")
                self.page.screenshot(path="debug_error.png")
                return False, round_score