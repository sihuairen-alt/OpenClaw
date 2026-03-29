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
import numpy as np

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
        print("📊 实时行情")
        for sym, info in data.items():
            e = EMOJI.get(sym, "📈")
            price = info.get("price", "N/A")
            print(f"{e} {sym}: {price}")
    else:
        e = EMOJI.get(symbol, "📈")
        print(f"{e} {symbol}: {data.get('price', 'N/A')}")

def _ema(data, period):
    alpha = 2.0 / (period + 1)
    result = np.zeros(len(data))
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = alpha * data[i] + (1 - alpha) * result[i - 1]
    return result

def calc_rf(closes, period=100, mult=3.0):
    n = len(closes)
    src = np.array(closes, dtype=float)

    abs_change = np.abs(np.diff(src, prepend=src[0]))
    avrng = _ema(abs_change, period)
    smrng = _ema(avrng, period * 2 - 1) * mult

    filt = np.zeros(n)
    filt[0] = src[0]
    for i in range(1, n):
        prev = filt[i - 1]
        filt[i] = max(prev, src[i] - smrng[i]) if src[i] > prev else min(prev, src[i] + smrng[i])

    upward = np.zeros(n)
    downward = np.zeros(n)
    for i in range(1, n):
        if filt[i] > filt[i - 1]:
            upward[i] = upward[i - 1] + 1
            downward[i] = 0
        elif filt[i] < filt[i - 1]:
            downward[i] = downward[i - 1] + 1
            upward[i] = 0
        else:
            upward[i] = upward[i - 1]
            downward[i] = downward[i - 1]

    hband = filt + smrng
    lband = filt - smrng

    long_cond = (src > filt) & (upward > 0)
    short_cond = (src < filt) & (downward > 0)
    cond_ini = np.zeros(n)
    buy = np.zeros(n, dtype=bool)
    sell = np.zeros(n, dtype=bool)
    for i in range(1, n):
        cond_ini[i] = 1 if long_cond[i] else (-1 if short_cond[i] else cond_ini[i - 1])
        buy[i] = long_cond[i] and cond_ini[i - 1] == -1
        sell[i] = short_cond[i] and cond_ini[i - 1] == 1

    return {
        'filter': filt, 'hband': hband, 'lband': lband,
        'smrng': smrng, 'upward': upward, 'downward': downward,
        'buy': buy, 'sell': sell
    }

def get_klines(symbol="XAU/USD", interval="15min", outputsize=100):
    """获取K线数据并输出 RF 分析"""
    url = f"{BASE_URL}/time_series?symbol={urllib.parse.quote(symbol, safe='/')}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}"
    data = fetch(url)

    if data.get("status") == "error":
        print(f"❌ 错误: {data.get('message')}")
        return

    values = data.get("values", [])
    if not values:
        print("❌ 无K线数据")
        return

    # 时间序列从旧到新
    values_asc = list(reversed(values))
    closes  = [float(v["close"]) for v in values_asc]
    times   = [v["datetime"] for v in values_asc]
    highs   = [float(v["high"]) for v in values_asc]
    lows    = [float(v["low"])  for v in values_asc]

    rf = calc_rf(closes)

    latest_idx = len(closes) - 1
    current    = closes[-1]
    filt_now   = rf['filter'][-1]
    hband_now  = rf['hband'][-1]
    lband_now  = rf['lband'][-1]
    smrng_now  = rf['smrng'][-1]
    up_now     = int(rf['upward'][-1])
    dn_now     = int(rf['downward'][-1])

    # 方向
    if up_now > 0:
        direction = f"↑上升第{up_now}根"
        signal_state = "🟢 多头区间"
    elif dn_now > 0:
        direction = f"↓下降第{dn_now}根"
        signal_state = "🔴 空头区间"
    else:
        direction = "→走平"
        signal_state = "⚪ 中性"

    # 价格 vs 滤波线
    diff = round(current - filt_now, 2)
    pos  = "上方" if diff > 0 else "下方"

    # 最近买卖信号
    last_buy = last_sell = None
    for i in range(latest_idx, -1, -1):
        if rf['buy'][i] and last_buy is None:
            last_buy = (times[i], round(closes[i], 2))
        if rf['sell'][i] and last_sell is None:
            last_sell = (times[i], round(closes[i], 2))
        if last_buy and last_sell:
            break

    # 交易建议
    if signal_state == "🟢 多头区间":
        direction_advice = "做多"
        entry = f"{round(filt_now, 2)} ~ {round(current, 2)}"
        sl    = f"{round(lband_now, 2)}（RF下轨）"
        tp    = f"{round(hband_now, 2)}（RF上轨）"
    elif signal_state == "🔴 空头区间":
        direction_advice = "做空"
        entry = f"{round(current, 2)} ~ {round(filt_now, 2)}"
        sl    = f"{round(hband_now, 2)}（RF上轨）"
        tp    = f"{round(lband_now, 2)}（RF下轨）"
    else:
        direction_advice = "观望"
        entry = sl = tp = "等待信号明确"

    print(f"━━ 📡 Range Filter 信号 ━━")
    print(f"\n【滤波线状态】")
    print(f"• 滤波线：{round(filt_now, 2)}")
    print(f"• 价格 vs 滤波线：{pos}，差距 {abs(diff)} 点")
    print(f"• 滤波方向：{direction}")
    print(f"• 信号状态：{signal_state}")
    print(f"\n【目标带】")
    print(f"• 上轨：{round(hband_now, 2)}")
    print(f"• 滤波线：{round(filt_now, 2)} ← 核心")
    print(f"• 下轨：{round(lband_now, 2)}")
    print(f"• 带宽：{round(smrng_now, 2)} 点")
    print(f"\n【最近信号】")
    print(f"• 最近 Buy：{last_buy[0]} @ {last_buy[1]}" if last_buy else "• 最近 Buy：暂无")
    print(f"• 最近 Sell：{last_sell[0]} @ {last_sell[1]}" if last_sell else "• 最近 Sell：暂无")
    print(f"\n【RF 交易建议】")
    print(f"▶ 方向：{direction_advice}")
    print(f"▶ 入场参考：{entry}")
    print(f"▶ 止损参考：{sl}")
    print(f"▶ 止盈参考：{tp}")
    print(f"\n⚠️ 以上为技术面参考，需等系统条件完全满足再入场")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "price"

    if cmd == "price":
        symbol = sys.argv[2] if len(sys.argv) > 2 else "XAU/USD,GBP/USD,EUR/USD,AUD/USD,AUD/JPY"
        get_price(symbol)
    elif cmd == "klines":
        symbol   = sys.argv[2] if len(sys.argv) > 2 else "XAU/USD"
        interval = sys.argv[3] if len(sys.argv) > 3 else "15min"
        size     = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        get_klines(symbol, interval, size)
    else:
        print("用法: market_data.py [price|klines] [symbol] [interval] [outputsize]")
