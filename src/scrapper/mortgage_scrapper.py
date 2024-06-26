import asyncio
from typing import Annotated, List, Dict

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Page
from pydantic import BaseModel, Field


class MortgageInputData(BaseModel):
    fullPrice: Annotated[int, Field(ge=1_000_000, le=999_999_999, default=10_000_000)]
    downPayment: Annotated[int, Field(ge=100_000, le=500_000_000, default=2_000_000)]
    loanDurationInYears: Annotated[int, Field(ge=1, le=50, default=20)]
    loanRate: Annotated[float, Field(gt=0, le=20, default=10)]


user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 '
              'Safari/537.36')
url_to_scrap = "https://www.sravni.ru/ipoteka/kalkuljator-ipoteki/"


async def get_website_mortgage_result_table(mortgage_data: MortgageInputData) -> List[Dict[str, any]]:
    async with async_playwright() as p:
        url = url_to_scrap
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        async with await browser.new_context(ignore_https_errors=True,
                                             user_agent=user_agent) as context:
            page = await context.new_page()
            await page.goto(url)
            page = await _fill_mortgage_calc_fields(page, mortgage_data)
            paymentsDictList = await _get_table_from_page_content(page)
            await _get_result_page_pdf(page)
        return paymentsDictList


async def _fill_mortgage_calc_fields(page: Page, mortgage_data: MortgageInputData) -> Page:
    await page.get_by_label("Стоимость недвижимости").click()
    await page.get_by_label("Стоимость недвижимости").fill(str(mortgage_data.fullPrice))
    await page.get_by_label("Первый взнос").click()
    await page.get_by_label("Первый взнос").fill(str(mortgage_data.downPayment))
    await page.get_by_role("textbox", name="Срок кредита").click()
    await page.get_by_role("textbox", name="Срок кредита").fill(str(mortgage_data.loanDurationInYears))
    await page.get_by_role("textbox", name="Ставка").fill(str(mortgage_data.loanRate).replace(".", ","))
    await page.get_by_role("button", name="Рассчитать").click()
    await asyncio.sleep(2)
    await page.get_by_role("heading", name="График платежей").click()
    await page.get_by_text("Нажмите, чтобы посмотреть все строки").click()
    await page.click(
        "#__next > div.style_wrapper__ZbiR_ > div > div.style_wrapper__T6rb4 > div:nth-child(3) > a > div.btn-close")
    return page


async def _get_table_from_page_content(page: Page) -> List[Dict[str, any]]:
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find('table', {'class': 'Table_table__svHvy Table_tableAccordion__XhRxN'})
    head_items = [header.text for header in table.find_all('th')]
    paymentsDictList = [
        {head_items[i]: cell.string.strip("<>/td").replace("\xa0", "") for i, cell in enumerate(row.find_all('td'))}
        for row in table.find_all('tr')]
    return paymentsDictList


async def _get_result_page_pdf(page: Page) -> str:
    path_to_pdf = "page.pdf"
    await page.emulate_media(media="screen")
    await page.pdf(path=path_to_pdf, scale=0.8)
    return path_to_pdf
