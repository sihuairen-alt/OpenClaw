# TOOLS.md - Local Notes

## Gold Price API
- **首选**: TwelveData `python3 scripts/market_data.py price`
  - API Key 存 `/root/.openclaw/.env`（不进 git）
  - 脚本: `scripts/market_data.py`
- **备用**: Gold-API `https://api.gold-api.com/price/XAU`（免费，无需 Key）

## 行情查询能力

你有能力通过脚本工具获取实时外汇和贵金属行情数据。

### 支持的品种
- XAU/USD（黄金）
- GBP/USD（英镑兑美元）
- EUR/USD（欧元兑美元）
- AUD/USD（澳元兑美元）
- AUD/JPY（澳元兑日元）

### 使用规则
1. 当老板问到任何品种的价格时，立即调用 `python3 scripts/market_data.py price` 获取实时数据，不要用记忆中的旧价格
2. 当老板要求分析行情、看K线、判断趋势时，调用 `python3 scripts/market_data.py klines [symbol] [interval] [outputsize]`
3. 默认使用 15min（15分钟）周期的K线，老板指定其他周期时按指定的来
4. K线默认获取最近 30 根，老板需要更多时可以调整 outputsize 参数

### K线分析方法
拿到K线数据后，你需要：
1. 识别近期高低点和支撑阻力位
2. 判断当前趋势方向（上涨/下跌/震荡）
3. 观察最近几根K线的形态（吞没、锤子、十字星等）
4. 结合 ODIN 策略体系（Range Filter + WAE + IMACD）给出分析
5. 如果发现明确的交易信号，提醒老板注意，但必须等系统条件完全满足再建议入场

### 输出格式
查询价格时输出：
📊 实时行情
🥇 XAUUSD: 3012.45
💷 GBPUSD: 1.29450
💶 EURUSD: 1.08320
🦘 AUDUSD: 0.65230
🇯🇵 AUDJPY: 97.45

分析K线时输出：
📈 [品种] [周期] K线分析
- 当前价格：xxx
- 趋势方向：xxx
- 关键支撑：xxx
- 关键阻力：xxx
- K线形态：xxx
- 交易建议：xxx（必须符合系统条件才给信号）

### 注意事项
- 数据来源为 Twelve Data，与老板经纪商报价可能有 0.1-0.5 个点的微小差异
- 周末外汇市场休市，此时返回的是最后收盘价
- 不要频繁调用（免费额度每分钟8次），同一个请求15秒内不要重复调用
- API Key 绝对不要在对话中显示给任何人

## Paywall Bypass
- URL: `https://paywallbuster.com/[目标URL]`
- 用于绕过付费文章

## Image Generation
- 工具：nano Banana 2
- OpenRouter model ID: `google/gemini-3.1-flash-image-preview`

## Discord
- 服务器 ID: 1479000073386987651
- Bot Token / Webhooks: 见服务器环境变量（不存入 git）

## SSH
- GitHub SSH key: ~/.ssh/id_ed25519
- Remote: git@github.com:sihuairen-alt/OpenClaw.git

## Trello
- 交易记录看板: 交易记录 2026
- 日常看板: 日常 2026
- 时区: 布里斯班 (GMT+10)
- API Key / Token: 见服务器环境变量（不存入 git）
