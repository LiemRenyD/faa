# from .base import BaseHandler

# class TrueFalseHandler(BaseHandler):
#     def execute(self, page, question):
#         # 判断题 A正确 B错误
#         idx = 0 if question.answer == "正确" or question.answer == "A" else 1
#         options = page.locator(".question-item").all()
#         if idx < len(options):
#             options[idx].click()
#         # 判断题通常点击即跳转，无需点提交

from .base import BaseHandler
from src.config import settings

class TrueFalseHandler(BaseHandler):
    def execute(self, page, question):
        # 判断题 A正确 B错误
        idx = 0 if question.answer == "正确" or question.answer == "A" else 1

        # ✅ 添加与多选题相同的固定等待（确保渲染和事件绑定完成）
        page.wait_for_timeout(1500)

        options = page.locator(".question-item").all()
        if idx >= len(options):
            return

        # 第一轮点击
        if "selected" not in (options[idx].get_attribute("class") or ""):
            options[idx].click()
            page.wait_for_timeout(settings.answer_interval)

        # 验证补点
        max_retry = 2
        for retry in range(max_retry):
            current_class = options[idx].get_attribute("class") or ""
            if "selected" in current_class:
                break
            print(f"⚠️ 判断题选项未选中，尝试补点（第{retry+1}次）")
            options[idx].click()
            page.wait_for_timeout(settings.answer_interval)