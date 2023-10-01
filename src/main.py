import time
import awswrangler as wr
import polars as pl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from bs4 import BeautifulSoup
def get_driver() -> webdriver:
    """
    Return a webdriver
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return webdriver.Chrome(options=chrome_options)
def get_table_of_prices(driver):
    """
    Return the table with all cryptocurrency's
    """
    driver.get("https://coinmarketcap.com/")
    time.sleep(5)
    div =  driver.find_element(By.CLASS_NAME,'sc-66133f36-2')
    return div.find_element(By.CLASS_NAME,'sc-66133f36-3')

def get_bitcoin_price(driver) -> float:
    """
    Return the current price of bitcoin
    """

    table = get_table_of_prices(driver)

    element = table.find_element(By.CLASS_NAME,'sc-a0353bbc-0')

    price= float(element.text[1:].replace(',',''))
    return price

def price_negative(price)-> bool:
    """
    Return True if the element price is have a element with class name  icon-Caret-up 
    Return False if the element don't have the element with the class name icon-Caret-up
    """
    try:
        price.find_element(By.CLASS_NAME,'icon-Caret-up')
        return False
    except NoSuchElementException:
        return True

def get_price_variation_last_hour(table_of_prices) -> float:
    """
    Return the variation of bitcoin price in the last hour
    """
    price_last_hour = table_of_prices.find_element(By.CLASS_NAME,'sc-d55c02b-0')
    if price_negative(price_last_hour):
        return float(price_last_hour.text[:-1]) * -1
    return float(price_last_hour.text[:-1])


def get_price_variations(driver) -> list:
    """
    Return a list of price variations
    the first element is the variation of the last hour
    the second element is the variation of the last 24 hour
    the third element is the variation of the last sevend days
    example of return [-0.14,-0.38,2.51]
    """

    table = get_table_of_prices(driver)
    variation_last_hour = get_price_variation_last_hour(table)

    print(variation_last_hour)
    return [variation_last_hour]

def write_parquet(dataframe: pl.DataFrame, path: str) -> None:
    """
    Write a Pandas DataFrame to S3 in Parquet format in append mode.

    Args:
        dataframe: The Polars DataFrame to write.
        path: The S3 path to write the DataFrame to.
    Returns:
        None.
    """

    wr.s3.to_parquet(dataframe.to_pandas(), path, dataset=True, mode='append')

def create_dataframe(bitcoin_price,variation_last_hour):
    """
    Create a Polars dataframe with columns bitcoin_price,variation_last_hour and datetime
    Args:
        bitcoin_price: the price of bitcoin in current_time
        variation_last_hour: the variation of bitcoin price in last hour
    Returns:
        Polars DataFrame
    """
    data = [
        pl.Series("bitcoin_price", [bitcoin_price],dtype=pl.Float32),
        pl.Series("variation_last_hour", [variation_last_hour],dtype=pl.Float32),
        pl.Series("datetime", [datetime.now()],dtype=pl.Datetime)
    ]
    return pl.DataFrame(data)

if __name__ == '__main__':
    PATH = 's3://bitcoin-crawler-7493/raw/'
    chrome_driver = get_driver()
    table = get_table_of_prices(chrome_driver)
    variation_last_hour = get_price_variation_last_hour(table)
    df = create_dataframe(
        get_bitcoin_price(chrome_driver),
        variation_last_hour
    )
    write_parquet(df,PATH)
    chrome_driver.close() 
