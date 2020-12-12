import json
import pandas as pd
import requests


def send_request(isin):
    response = requests.get("http://mdapi.tadbirrlc.com/API/symbol?$filter=SymbolISIN+eq+%27" + isin + "%27")
    data = response.text
    parsed = json.loads(data)
    x = parsed['List'][0]
    return x


def get_traded_price(data):
    low = data.get("LowAllowedPrice")
    high = data.get("HighAllowedPrice")
    return (low + high) / 2


def get_unit_count(data):
    return data.get("UnitCount")


def get_Last_traded_price(data):
    return data.get("LastTradedPrice")


def_ref = pd.read_excel('Data\نمادها.xlsx')
Isin_list = def_ref['isin'].values.tolist()
Ref_sybols = def_ref['نماد'].values.tolist()
cleanedList = [x for x in Isin_list if str(x) != 'nan']

sum_shakhes = 0
sum_day = 0

for isin in cleanedList:
    data = send_request(isin)
    sum_shakhes = sum_shakhes +(get_unit_count(data) * get_traded_price(data))
    sum_day = sum_day + (get_unit_count(data) * get_Last_traded_price(data))

print('اندازه‌ی شاخص دیروز را وارد کنید')
shakhes = input()
shakhes = float(shakhes)
print(shakhes*(sum_day/sum_shakhes))