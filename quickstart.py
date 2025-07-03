from  playwright.sync_api import sync_playwright

# Initalizing
pw=sync_playwright().start()

# Browser object
browser=pw.firefox.launch(
    headless=False ,
    slow_mo=2000, 
)

page.get_by_placeholder("Search term...")

page=browser.new_page()
page.goto(r"https://google.com")

print(page.title())
page.screenshot(path='example.png')



browser.close()