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
        for i in range(settings.max_rounds):
            print(f"--- 第 {i+1} 轮开始 ---")
            self._answer_single_round()
            self.is_first_question = True  # 每一轮结束重置标识

    def _answer_single_round(self):
        question_count = 0  # 初始化题目计数器
        
        while True:
            try:
                # 核心优化：将触发动作（goto 或 execute）放在 expect_response 内部
                # 这样可以确保"先监听，后触发"，不会错过任何请求
                with self.page.expect_response("**/getPracticeQuestion*", timeout=10000) as resp_info:
                    if self.is_first_question:
                        print("🌐 正在进入答题页面...")
                        self.page.goto(settings.question_url)
                        self.is_first_question = False
                    else:
                        # 非第一题时，上一次循环的 execute 已经完成了点击
                        # 这里只需要静等响应即可，如果逻辑需要，也可以把 click 放在这里
                        pass
                
                resp = resp_info.value
                data = resp.json()
                
                # 校验接口状态
                if data.get("result") != 1:
                    print(f"🏁 轮次可能已结束: {data.get('msg')}")
                    break
                    
                raw_data = data.get("data", {})
                question = APIQuestionParser.parse(raw_data)
                
                print(f"📝 正在处理题号: {question.id}")
                print(f"📋 题目详情: {question}")
                
                # 查找答案
                question = self.finder.find_answer(question)
                print(f"📋 答案详情: {question}")
                
                # 获取对应的处理器
                handler = QuestionHandlerFactory.get_handler(question.type)
                
                # 执行动作：填空或点击（这会触发下一个 getPracticeQuestion 请求）
                handler.execute(self.page, question)
                
                # 答题间隔（从配置读取）
                self.page.wait_for_timeout(settings.answer_interval)
                
                # 题目计数+1
                question_count += 1
                print(f"📊 本轮已答题数: {question_count}/{settings.questionlimit}")
                
                # 检查是否达到每轮题目上限
                if question_count >= settings.questionlimit:
                    self.page.wait_for_timeout(5000)
                    print(f"✅ 已达到本轮题目上限 ({settings.questionlimit} 题)，结束本轮")
                    break
                
            except Exception as e:
                print(f"⚠️ 循环捕获到异常: {e}")
                # 如果是因为找不到元素，可以尝试截图排查
                self.page.screenshot(path="debug_error.png")
                break