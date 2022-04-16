import pandas as pd
import requests
from bs4 import BeautifulSoup
import src.commons.FileIO as FileIO

code_names = ["shanghai-composite-historical-data", "hang-sen-40-historical-data"]

# record is a list [date, close, open, high, low, volumn, rise_rate]
# 日期 收盘 开盘 高 低 交易量 涨跌幅
# #down load the latest market record
def get_latest_record(code_name):
    headers = {'User-Agent': 'Mozilla/5.0 3578.98 Safari/537.36'}
    url_base = "https://cn.investing.com/indices/"
    url = url_base + code_name
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    latest_record = soup.find("table", id="curr_table").find_all("tr")[1].find_all("td")

    date = FileIO.convertToStandardDate(latest_record[0].text)
    close = float(latest_record[1].text.replace(",", ""))
    open = float(latest_record[2].text.replace(",", ""))
    high = float(latest_record[3].text.replace(",", ""))
    low = float(latest_record[4].text.replace(",", ""))
    volumn = latest_record[5].text.replace(",", "")
    rise_rate = float(latest_record[6].text.replace("%", ""))/100
    record_list = [date, close, open, high, low, volumn, rise_rate]
    print(record_list)

get_latest_record(code_names[0])