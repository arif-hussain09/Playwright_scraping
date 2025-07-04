from playwright.async_api import async_playwright
import asyncio
import csv 
import json

async def main():
    async with async_playwright() as p:
        browser=await p.firefox.launch(
            headless=False,
            slow_mo=2000,
        )
        page=await browser.new_page()                                                                                                   

        await page.goto("http://quotes.toscrape.com")
        await page.wait_for_selector(".quote")  # 🔥 ensures page is ready
        await page.screenshot(path="example.png")

        all_quotes=[]

        while True:

            quotes=await page.locator(".quote").all() # select tall the div container of class qoute

            for quote in quotes:
                text= await quote.locator(".text").inner_text()
                author= await quote.locator(".author").inner_text()
                tags= await quote.locator(".tags .tag").all_inner_texts()

                all_quotes.append({
                    "text": text,
                    "author": author,
                    "tags": tags
                })
            
            next_btn=page.locator("li.next > a")

            if await next_btn.count()==0:
                break
            await next_btn.click()

        await browser.close()

    # Saving to json file

    with open("quotes.json","w",encoding="utf-8") as f_json:
        json.dump(all_quotes,f_json,indent=2 , ensure_ascii=False)

    # Saving to csv

    with open("quotes.csv","w",encoding='utf-8',newline='') as f_csv:
        writer=csv.DictWriter(f_csv,fieldnames=["Quote","Author","tages"])
        writer.writeheader()
        for quote in all_quotes:
            writer.writerow({
                     "Quote": quote["text"],
                    "Author": quote["author"],
                    "tages": ", ".join(quote["tags"])
                }
            )

    
    for i , q in enumerate(all_quotes[:3]):
        print(f"{i+1} : {q['text'] }\n{q['author'] }\n{q['tags'] }\n")


if __name__=="__main__":
    asyncio.run(main())