import re
from playwright.sync_api import sync_playwright
from src.config import settings

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=settings.headless)
        context = self.browser.new_context(**self.playwright.devices["iPhone 15 Pro Max"])
        return context.new_page()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()
        self.playwright.stop()

    @staticmethod
    def login(page):
        page.goto(settings.question_url)
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.get_by_role("textbox", name=re.compile("手机号|超星号")).fill(settings.phone_number)
        page.get_by_role("textbox", name=re.compile("密码")).fill(settings.password)
        
        # 隐私协议勾选
        privacy = page.get_by_role("paragraph").filter(has_text=re.compile("隐私政策|用户协议")).locator("span")
        if privacy.is_visible(): privacy.click()
        
        page.get_by_role("button", name="登录").click()
        print("登录完成")
        page.wait_for_timeout(1500)
        page.wait_for_url("**practice**", timeout=10000)   # 改为实际的目标路径
        print("登录成功，已跳转")