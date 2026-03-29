#!/usr/bin/env python3
"""
行情查询工具 - 使用 Twelve Data API
首选: TwelveData | 备用: Gold-API (仅黄金)
"""
import sys
import json
import os
import urllib.request
import urllib.parse

API_KEY = os.environ.get("TWELVEDATA_API_KEY", "fa789a8a0d3e43a89c931747a3f3cfc2")
BASE_URL = "https://api.twelvedata.com"

SYMBOLS = {
    "gold": "XAU/USD",
    "xauusd": "XAU/USD",
    "gbpusd": "GBP/USD",
    "eurusd": "EUR/USD",
    "audusd": "AUD/USD",
    "audjpy": "AUD/JPY",
}

EMOJI = {
    "XAU/USD": "🥇",
    "GBP/USD": "💷",
    "EUR/USD": "💶",
    "AUD/USD": "🦘",
    "AUD/JPY": "🇯🇵",
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def get_price(symbol="XAU/USD,GBP/USD,EUR/USD,AUD/USD,AUD/JPY"):
    """获取实时价格"""
    url = f"{BASE_URL}/price?symbol={urllib.parse.quote(symbol, safe=',/')}&apikey={API_KEY}"
    data = fetch(url)

    if "," in symbol:
        # 多品种
        print("📊 实时行情")
        for sym, info in data.items():
            e = EMOJI.get(sym, "📈")
            price = info.get("price", "N/A")
            print(f"{e} {sym}: {price}")
    else:
        # 单品种
        e = EMOJI.get(symbol, "📈")
        print(f"{e} {symbol}: {data.get('price', 'N/A')}")

def get_klines(symbol="XAU/USD", interval="15min", outputsize=30):
    """获取K线数据并分析"""
    url = f"{BASE_URL}/time_series?symbol={urllib.parse.quote(symbol)}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}"
    data = fetch(url)

    if data.get("status") == "error":
        print(f"❌ 错误: {data.get('message')}")
        return

    values = data.get("values", [])
    if not values:
        print("❌ 无K线数据")
        return

    latest = values[0]
    oldest = values[-1]

    highs = [float(v["high"]) for v in values]
    lows  = [float(v["low"])  for v in values]
    closes = [float(v["close"]) for v in values]

    current  = float(latest["close"])
    high_max = max(highs)
    low_min  = min(lows)

    # 简单趋势判断
    if closes[0] > closes[5]:
        trend = "📈 短期上涨"
    elif closes[0] < closes[5]:
        trend = "📉 短期下跌"
    else:
        trend = "➡️ 震荡"

    # 关键位
    resistance = round(high_max, 2)
    support    = round(low_min, 2)

    # 最近K线形态
    last = values[0]
    body = abs(float(last["close"]) - float(last["open"]))
    wick = float(last["high"]) - float(last["low"])
    if body < wick * 0.1:
        pattern = "十字星（犹豫）"
    elif float(last["close"]) > float(last["open"]):
        pattern = "阳线"
    else:
        pattern = "阴线"

    print(f"📈 {symbol} {interval} K线分析（最近{outputsize}根）")
    print(f"- 当前价格：{current}")
    print(f"- 趋势方向：{trend}")
    print(f"- 关键支撑：{support}")
    print(f"- 关键阻力：{resistance}")
    print(f"- K线形态：{pattern}")
    print(f"- 数据范围：{oldest['datetime']} → {latest['datetime']}")
    print(f"\n⚠️ 以上为技术面参考，需结合 ODIN 策略信号确认后再入场")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "price"

    if cmd == "price":
        symbol = sys.argv[2] if len(sys.argv) > 2 else "XAU/USD,GBP/USD,EUR/USD,AUD/USD,AUD/JPY"
        get_price(symbol)
    elif cmd == "klines":
        symbol   = sys.argv[2] if len(sys.argv) > 2 else "XAU/USD"
        interval = sys.argv[3] if len(sys.argv) > 3 else "15min"
        size     = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        get_klines(symbol, interval, size)
    else:
        print("用法: market_data.py [price|klines] [symbol] [interval] [outputsize]")
