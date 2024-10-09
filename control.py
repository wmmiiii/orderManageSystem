import time

from playwright.sync_api import Playwright, sync_playwright

# C:\Users\xiaozai\AppData\Local\ms-playwright
with sync_playwright() as playwright:
    browser = playwright.chromium.launch_persistent_context(
        # 指定本机用户缓存地址
        user_data_dir=r"C:\Users\Administrator\AppData\Local\google\Chrome\User Data",
        # 指定本机google客户端exe的路径
        channel='chrome',
        # # 要想通过这个下载文件这个必然要开  默认是False
        # accept_downloads=True,
        # 设置不是无头模式
        headless=False,
    )
    page = browser.new_page()
    page.goto("https://admin.shopify.com/store/alanna-mx/orders?inContextTimeframe=none")

    page.goto("https://admin.shopify.com/store/alanna-mx/orders.json?inContextTimeframe=none")
    time.sleep(5)
    print(page.query_selector('pre').inner_text())
    browser.close()
