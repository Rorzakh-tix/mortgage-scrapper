from src.scrapper.mortgage_scrapper import get_website_mortgage_result_table, MortgageInputData


async def test_mortgage_scrap():
    mortgage_data=MortgageInputData(
        fullPrice=10_000_000,
        downPayment=2_000_000,
        loanDurationInYears=20,
        loanRate=5,
    )
    # Act
    result = await get_website_mortgage_result_table(mortgage_data)
    # Assert
    assert not len(result)==0
    assert result[0]["Сумма платежа"] == "52796,46"""
