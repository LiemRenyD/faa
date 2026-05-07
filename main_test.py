from src.core.browser import BrowserManager

if __name__ == "__main__":
    success = 0
    fail = 0

    for i in range(1, 11):
        try:
            with BrowserManager() as page:          # 每次进入 with 都启动新浏览器
                BrowserManager.login(page)          # 执行登录
                success += 1
                page.wait_for_timeout(1500)
                # expect(page.locator(".van-nav-bar__left")).to_be_visible()
                page.locator(".van-nav-bar__left").click()
                # expect(page.get_by_text("退出", exact=True)).to_be_visible()
                page.get_by_text("退出", exact=True).click()
                page.wait_for_timeout(1500)
                
                print(f"第 {i} 次登录：✅ 成功")
            # with 块结束自动关闭浏览器和 playwright
        except Exception as e:
            fail += 1
            print(f"第 {i} 次登录：❌ 失败 ({e})")

    print(f"\n登录测试完成：成功 {success} 次，失败 {fail} 次")