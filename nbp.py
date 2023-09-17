# -*- coding: utf-8 -*-
# Name: nbp
# Description: Currency exchange rates by NBP (api.nbp.pl/en.html)
# Version: 0.1a2
# Owner: Ruslan Korniichuk

import pandas as pd
import requests


def get_rate(code='usd'):

    code = code.lower()

    url = f"http://api.nbp.pl/api/exchangerates/rates/c/{code}/"
    headers = {"Accept": "application/json"}

    r = requests.get(url, headers=headers)
    data = r.json()

    buy = data['rates'][0]['bid']
    sell = data['rates'][0]['ask']
    effective_date = data['rates'][0]['effectiveDate']

    text = f"{code.upper()}\n*buy*: {buy}\n*sell*: {sell}\n\n{effective_date}"

    return text


def get_table(table='c'):

    table = table.lower()

    url = f"http://api.nbp.pl/api/exchangerates/tables/{table}"
    headers = {"Accept": "application/json"}

    r = requests.get(url, headers=headers)
    data = r.json()
    effective_date = data[0]['effectiveDate']

    df = pd.DataFrame.from_dict(data[0]["rates"])

    if (table == 'a') or (table == 'b'):
        df.rename(columns={"currency": "name", "code": "currency",
                           "mid": "mid-rate"}, inplace=True)
        tmp = df[["currency", "mid-rate"]].sort_values(by=["currency"])
    elif table == 'c':
        df.rename(columns={"currency": "name", "code": "currency",
                           "bid": "buy", "ask": "sell"}, inplace=True)
        tmp = df[["currency", "buy", "sell"]].sort_values(by=["currency"])

    markdown = tmp.to_markdown(index=False)
    text = f"```\n{markdown}\n\n```{effective_date}"

    return text
