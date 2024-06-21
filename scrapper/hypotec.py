import asyncio
from typing import Annotated, List
import locale

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Page
from pydantic import BaseModel, Field


# async def get_website_content2():
#     """Use this to get the text content of a website."""
#     async with async_playwright() as p:  # pylint: disable=invalid-name
#         # can be used for local debugging in jupyter notebook
#         # p = await async_playwright().start()
#         # browser = await p.chromium.launch(headless=False)
#         url = "https://www.sberbank.ru/ru/person/credits/home/ipotechniy-kalkulyator"
#         browser = await p.chromium.launch(headless=False, slow_mo=100)
#         context = await browser.new_context(ignore_https_errors=True,
#                                             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
#
#                                             )
#         page = await context.new_page()
#
#         content = await page.content()
#
#         print(f"Goto {url}")
#         await page.goto(url)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").locator("[data-test-id=\"input\"]").get_by_role(
#             "textbox").fill("Санкт-Петербург")
#         await page.frame_locator("iframe[title=\"Основной контент\"]").locator("div").filter(
#             has_text=re.compile(r"^Санкт-Петербург$")).click()
#         await page.frame_locator("iframe[title=\"Основной контент\"]").locator(
#             ".dropdown-root-7b1-11-0-3 > .ppr-container-ab9-11-0-0 > div > div > .inpt-root-670-11-0-8 > .inpt-inputContainer-d7e-11-0-8").click()
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_text(
#             "Квартира в новостройкеот 6%").click()
#         #time.sleep(1)
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
#                                                                                    name="Ипотека для IT от 5%").click()
#         #await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Стоимость недвижимости376").click()
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Стоимость недвижимости").click()
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Стоимость недвижимости").fill(
#             "8 000 000")
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Первоначальный взнос").click()
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Первоначальный взнос").fill(
#             "3 000 000")
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Срок кредита").click()
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_label("Срок кредита").fill("20")
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
#                                                                                    name="График платежей").click()
#         # await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
#         #                                                                            name="Скачать график").click()
#         # try:
#         #     async with page.expect_download() as download_xlsx:
#         #         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
#         #                                                                                    name="XLSX").click()
#         #     download = await download_xlsx.value
#         #     await download.save_as("1" + download.suggested_filename)
#         # except:
#         #     print(f"Не получилось скачать XLSX")
#         # try:
#         #     async with page.expect_download() as download_pdf:
#         #         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button", name="PDF").click()
#         #     downloadpdf = await download_pdf.value
#         #     await downloadpdf.save_as("1" + downloadpdf.suggested_filename)
#         # except:
#         #     print("Не получилось скачать")
#         # get page content
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("button",
#                                                                                    name="График платежей в таблице").click()
#         #await asyncio.sleep(1)
#         await page.frame_locator("iframe[title=\"Основной контент\"]").get_by_role("heading",
#                                                                                    name="График платежей").click()
#
#         await page.frame_locator("modal-wrapper-14-0-14 modal-wrapper--extralarge-14-0-14").get_by_role("table").click()
#         content = await page.content()
#         await asyncio.sleep(1)
#         soup = BeautifulSoup(content, "html.parser")
#         table = soup.find('div', {'class': 'modal-root-14-0-14 modal-root--with-title-14-0-14'})
#         table_body = table.find('tbody')
#         rows = table_body.find_all('tr')
#         for row in rows:
#             cols = row.fin_all('td')
#
#         print(table_body)
#         await context.close()

class MortgageInputData(BaseModel):
    fullPrice: Annotated[int, Field(ge=1_000_000, le=999_999_999, default=10_000_000)]
    downPayment: Annotated[int, Field(ge=100_000, le=500_000_000, default=2_000_000)]
    loanDurationInYears: Annotated[int, Field(ge=1, le=50, default=20)]
    loanRate: Annotated[float, Field(gt=0, le=20, default=10)]


async def fill_mortgage_calc_fields(page: Page, mortgage_data: MortgageInputData) -> Page:
    await page.get_by_label("Стоимость недвижимости").click()
    await page.get_by_label("Стоимость недвижимости").fill(str(mortgage_data.fullPrice))
    await page.get_by_label("Первый взнос").click()
    await page.get_by_label("Первый взнос").fill(str(mortgage_data.downPayment))
    await page.get_by_role("textbox", name="Срок кредита").click()
    await page.get_by_role("textbox", name="Срок кредита").fill(str(mortgage_data.loanDurationInYears))
    await page.get_by_role("textbox", name="Ставка").fill(str(mortgage_data.loanRate).replace(".", ","))
    await page.get_by_role("button", name="Рассчитать").click()
    await asyncio.sleep(2)
    await page.get_by_role("heading", name="График платежей").click(delay=100)
    await page.get_by_text("Нажмите, чтобы посмотреть все строки").click()
    return page


async def get_table_from_page_content(page: Page) -> list[dict[str, any]]:
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find('table', {'class': 'Table_table__svHvy Table_tableAccordion__XhRxN'})
    head_items = [header.text for header in table.find_all('th')]
    paymentsDictList = [
        {head_items[i]: cell.string.strip("<>/td").replace("\xa0", "") for i, cell in enumerate(row.find_all('td'))}
        for row in table.find_all('tr')]
    return paymentsDictList


async def get_website_mortgage_result_table(mortgage_data: MortgageInputData) -> list[dict[str,any]]:
    async with async_playwright() as p:
        url = "https://www.sravni.ru/ipoteka/kalkuljator-ipoteki/"
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        context = await browser.new_context(ignore_https_errors=True,
                                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        page = await context.new_page()
        print(f"Goto {url}")
        await page.goto(url)
        page = await fill_mortgage_calc_fields(page, mortgage_data)
        paymentsDictList = await get_table_from_page_content(page)
        await context.close()
        return paymentsDictList
