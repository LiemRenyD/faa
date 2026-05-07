from .base import BaseHandler
from src.config import settings
import random

class MultipleChoiceHandler(BaseHandler):
    def execute(self, page, question):
        target = list(question.answer) if question.answer else [random.choice(['A', 'B'])]
        page.wait_for_timeout(1500)
        print("当前 URL:", page.url)
        print("页面中 .question-item 的数量:", page.locator(".question-item").count())


        options = page.locator(".question-item").all()

        
        for i, opt in enumerate(options):
            char = chr(65 + i)
            if char in target:
                if "selected" not in (opt.get_attribute("class") or ""):
                    opt.click()
                    page.wait_for_timeout(settings.answer_interval)

        max_retry = 2  # 最多补点 2 次
        for retry in range(max_retry):
            all_selected = True
            for i, opt in enumerate(options):
                char = chr(65 + i)
                if char in target:
                    # 重新获取最新的 class 属性（避免缓存）
                    current_class = opt.get_attribute("class") or ""
                    if "selected" not in current_class:
                        all_selected = False
                        print(f"⚠️ 选项 {char} 未选中，尝试补点（第{retry+1}次）")
                        opt.click()
                        page.wait_for_timeout(settings.answer_interval)
            if all_selected:
                break

        # 针对选择题，通常需要手动点确定
        submit = page.locator("#mult-submit")
        if submit.is_visible(): submit.click()