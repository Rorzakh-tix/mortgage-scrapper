import asyncio
import json
import re
import time

from playwright.async_api import async_playwright, Playwright
from bs4 import BeautifulSoup


async def get_website_content():
    """Use this to get the text content of a website."""
    async with async_playwright() as p:  # pylint: disable=invalid-name
        # can be used for local debugging in jupyter notebook
        # p = await async_playwright().start()
        # browser = await p.chromium.launch(headless=False)
        url = "https://www.sberbank.ru/ru/person/credits/home/ipotechniy-kalkulyator"
        browser = await p.chromium.launch(headless=False, )
        context = await browser.new_context(ignore_https_errors=True,
                                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        page = await context.new_page()

        content = await page.content()

        print(f"Goto {url}")
        await page.goto(url)
        await page.frame_locator("iframe[title=\"Основной контент\"]").locator("[data-test-id=\"input\"]").get_by_role(
            "textbox").fill("Санкт-Петербург")
        await page.frame_locator("iframe[title=\"Основной контент\"]").locator("div").filter(
            has_text=re.compile(r"^Санкт-Петербург$")).click()
        await page.frame_locator("iframe[title=\"Основной контент\"]").locator(
            ".dropdown-root-7b1-11-0-3 > .ppr-container-ab9-11-0-0 > div > div > .inpt-root-670-11-0-8 > .inpt-inputContainer-d7e-11-0-8").click()
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_text(
            "Квартира в новостройкеот 6%").click()
        #time.sleep(1)
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
                                                                                   name="Ипотека для IT от 5%").click()
        #await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Стоимость недвижимости376").click()
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Стоимость недвижимости").click()
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Стоимость недвижимости").fill(
            "8 000 000")
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Первоначальный взнос").click()
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Первоначальный взнос").fill(
            "3 000 000")
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Срок кредита").click()
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Срок кредита").fill("20")
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
                                                                                   name="График платежей").click()
        # await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
        #                                                                            name="Скачать график").click()
        # try:
        #     async with page.expect_download() as download_xlsx:
        #         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
        #                                                                                    name="XLSX").click()
        #     download = await download_xlsx.value
        #     await download.save_as("1" + download.suggested_filename)
        # except:
        #     print(f"Не получилось скачать XLSX")
        # try:
        #     async with page.expect_download() as download_pdf:
        #         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button", name="PDF").click()
        #     downloadpdf = await download_pdf.value
        #     await downloadpdf.save_as("1" + downloadpdf.suggested_filename)
        # except:
        #     print("Не получилось скачать")
        # get page content
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
                                                                                   name="График платежей в таблице").click()
        await asyncio.sleep(1)
        await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("heading",
                                                                                   name="График платежей").click()

        page.frame_locator()
        content = await page.content()
        await asyncio.sleep(1)
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find('div', {'class': 'modal-root-14-0-14 modal-root--with-title-14-0-14'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.fin_all('td')

        print(table_body)
        await context.close()


async def get_website_content2():
    """Use this to get the text content of a website."""
    async with async_playwright() as p:  # pylint: disable=invalid-name
        # can be used for local debugging in jupyter notebook
        # p = await async_playwright().start()
        # browser = await p.chromium.launch(headless=False)
        url = "https://www.sravni.ru/ipoteka/kalkuljator-ipoteki/"
        browser = await p.chromium.launch(headless=False, )
        context = await browser.new_context(ignore_https_errors=True,
                                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        page = await context.new_page()
        print(f"Goto {url}")
        await page.goto(url)
        await page.get_by_label("Стоимость недвижимости").click()
        await page.get_by_label("Стоимость недвижимости").fill("8000000")
        await page.get_by_label("Первый взнос").click()
        await page.get_by_label("Первый взнос").fill("300 0000")
        await page.get_by_role("textbox", name="Срок кредита").click()
        await page.get_by_role("textbox", name="Срок кредита").fill("20")
        await page.get_by_role("textbox", name="Ставка").fill("8,6")
        await page.get_by_role("textbox", name="Ставка").press("Enter")
        #await page.get_by_label("Начало выплат").click()
        #await page.get_by_label("Начало выплат").fill("20.12.2027")
        await asyncio.sleep(1)
        await page.get_by_role("button", name="Рассчитать").click()
        await asyncio.sleep(2)
        await page.get_by_role("heading", name="График платежей").click()
        await asyncio.sleep(1)
        await page.get_by_text("Нажмите, чтобы посмотреть все строки").click()
        await asyncio.sleep(1)
        content = await page.content()
        await asyncio.sleep(1)
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find('table', {'class': 'Table_table__svHvy Table_tableAccordion__XhRxN'})
        table_head = table.find('thead')
        table_body = table.find('tbody')
        head_items = table_head.find_all('th')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            for index in range(1, cols):
                payments_dict = {cols[0]: [{head_items[index]: cols[index]}]}

        print(payments_dict)
        await context.close()
