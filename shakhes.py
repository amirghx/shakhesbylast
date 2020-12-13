import json
import pandas as pd
import requests
import matplotlib.pyplot as plt
import datetime


def store_file(sakhes, withLast):
    df = pd.read_excel('Data\تاریخچه.xlsx')

    date = df['تاریخ'].values.tolist()
    sakhes_list = df['شاخص'].values.tolist()
    with_last_list = df['شاخص با پایانی'].values.tolist()

    sakhes_list.append(sakhes)
    with_last_list.append(withLast)
    date.append(str(datetime.datetime.now()))

    plt.plot(date,sakhes_list, label="Index")
    plt.plot(date, with_last_list, label="Index with Last")

    plt.xlabel('Day')
    plt.ylabel('index')
    plt.title('index plot')
    plt.legend()
    plt.savefig('books_read.png')
    # function to show the plot


    date.insert(0,'تاریخ')
    sakhes_list.insert(0, 'شاخص')
    with_last_list.insert(0, 'شاخص با پایانی')
    zipped = zip(date,sakhes_list, with_last_list)
    output = pd.DataFrame(zipped)
    output.to_excel('Data\تاریخچه.xlsx', index=False, header=False)


def send_request_shakhes():
    response = requests.get("http://mdapi.tadbirrlc.com/api/LastInfoIndex")
    data = response.text
    parsed = json.loads(data)
    x = parsed['IndexInfo']
    return x


def get_shakhes(data):
    high = ((data.get("IndexHistoricalDataResult")).get("IRX6XTPI0006")).get('LastIndexValue')
    return high


def yesterday_shakhes(data, shakhes):
    high = ((data.get("IndexHistoricalDataResult")).get("IRX6XTPI0006")).get('IndexChanges')
    final = shakhes - high
    return final


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
    sum_shakhes = sum_shakhes + (get_unit_count(data) * get_traded_price(data))
    sum_day = sum_day + (get_unit_count(data) * get_Last_traded_price(data))
    print('done')
data_shakhes = send_request_shakhes()

shakhes = yesterday_shakhes(data_shakhes, get_shakhes(data_shakhes))
shakhes = float(shakhes)
print(shakhes * (sum_day / sum_shakhes))
store_file(get_shakhes(data_shakhes), shakhes)
