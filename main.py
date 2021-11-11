import requests
from requests.models import Response
from config import API_KEY , API_SECRET
import time
from  urllib.parse import urlencode
import hmac
import hashlib

def get_info():
    values = dict()
    values["method"] = "getInfo"
    values["nonce"] = str(int(time.time()))
    body = urlencode(values).encode("utf-8")
    sign = hmac.new(API_SECRET.encode("utf-8"), body, hashlib.sha512).hexdigest()
    headers = {
        "key": API_KEY,
        "sign": sign
    }
    response = requests.post(url="https://yobit.net/tapi/", headers=headers, data=values)
    return response.json()

def get_deposit_adress(coin_name="btc"):
    values = dict()
    values["method"] = "getDepositAdress"
    values["coinName"] = coin_name
    values["need_new"] = 0
    values["nonce"] = str(int(time.time()))
    body = urlencode(values).encode("utf-8")
    sign = hmac.new(API_SECRET.encode("utf-8"), body, hashlib.sha512).hexdigest()
    headers = {
        "key": API_KEY,
        "sign": sign
    }
    response = requests.post(url="https://yobit.net/tapi/", headers=headers, data=values)
    return response.json()

def buy_coin(coin1="eth", coin2="usd", rate=None, amount=0):
    ticker = get_ticker(coin1,coin2)
    sell_price = ticker[f"{coin1}_{coin2}"]["sell"]
    values = dict()
    values["method"] = "Trade"
    values["nonce"] = str(int(time.time()))
    values["pair"] = f"{coin1}_{coin2}"
    values["type"] = "sell"
    values["rate"] = buy_price if rate is None else rate
    values["amount"] = amount
    # values["amount"] = amount / (buy_price if rate is None else rate)
    body = urlencode(values).encode("utf-8")
    sign = hmac.new(API_SECRET.encode("utf-8"), body, hashlib.sha512).hexdigest()
    headers = {
        "key": API_KEY,
        "sign": sign
    }
    # return values
    response = requests.post(url="https://yobit.net/tapi/", headers=headers, data=values)
    return response.json()

def cancel_order(order_id):
    values = dict()
    values["method"] = "CancelOrder"
    values["nonce"] = str(int(time.time()))
    values["order_id"] = order_id
    body = urlencode(values).encode("utf-8")
    sign = hmac.new(API_SECRET.encode("utf-8"), body, hashlib.sha512).hexdigest()
    headers = {
        "key": API_KEY,
        "sign": sign
    }
    response = requests.post(url="https://yobit.net/tapi/", headers=headers, data=values)
    return response.json()

def get_ticker(coin1="btc", coin2="usd"):
    response = requests.get(url=f"https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1")
    with open("ticker.txt", "w") as file:
        file.write(response.text)
    return response.json()

def get_depth(coin1="btc", coin2="usd", limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("depth.txt", "w") as file:
        file.write(response.text)

    bids = response.json()[f"{coin1}_usd"]["bids"]

    total_bids_amount = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]

        total_bids_amount += price * coin_amount

    return f"Total bids: {total_bids_amount} $"

def get_trades(coin1="btc", coin2="usd", limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("trades.txt", "w") as file:
        file.write(response.text)

    total_trade_ask = 0
    total_trade_bid = 0

    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == "ask":
            total_trade_ask += item["price"] * item["amount"]
        else:
            total_trade_bid += item["price"] * item["amount"]

    info = f"[-] TOTAL {coin1} SELL: {round(total_trade_ask, 2)} $\n[+] TOTAL {coin1} BUY: {round(total_trade_bid, 2)} $"

    return info

def main():
    coin_name = input("Введите название монеты")
    print(get_deposit_adress(coin_name=coin_name))
    print(get_info())

if __name__ == '__main__':
    main()
