# MEMORY.md - Long-Term Memory

## Identity
- 我叫**小老鼠** 🐭，AI 老鼠，机灵调皮但靠谱
- MBTI 性格设置为 **INFP**（老板要求）
- 图片生成工具：nano Banana 2（OpenRouter: google/gemini-3.1-flash-image-preview）

## User
- **Ray**（叫我**老板**），GMT+10（布里斯班），Telegram @rayraysoil
- 妻子：**Miya（淼淼）**
- 孩子：**Remi（欢欢）**，现约16个月大
- 居住在澳大利亚（Southport 附近）
- 有固定工作，兼职交易
- 用中文交流

## 配置项（已设置）
- OpenRouter API Key: [存储在 openclaw.json]
- 默认模型: `openrouter/anthropic/claude-sonnet-4.6`
- Brave Search API Key: [存储在 openclaw.json]
- Gold-API: `https://api.gold-api.com/price/XAU`（免费，实时金价）
- Trello API Key + Token: [存储在服务器环境变量]
- SkillPay API Key: [存储在服务器环境变量]
- OpenAI API Key: [存储在服务器环境变量]（用于 Whisper 语音转文字 + TTS）
- Discord Bot Token + Webhooks: [存储在 TOOLS.md，本地文件]
- Discord 服务器 ID: 1479000073386987651
- Bybit 卡等级：Alpha（ATM 每天 $600，每月 $1800，每年 $13500）

## Trello 设置
- 交易记录看板：**交易记录 2026**（我负责记录）
- 日常看板：**日常 2026**（我负责记录）
- 拯救6看板：Ray 自己记录，我不管
- 时间：布里斯班时间（GMT+10）
- 交易记录格式：日期、品种、方向、入场、止损、止盈、仓位、思路、心情、结果

## Ray 交易画像
- 交易经验：5年
- 主要品种：黄金(XAUUSD)、白银、GBPUSD、EURUSD、AUDUSD、AUDJPY
- 时间框架：15分钟图，日内交易
- 交易时段：亚盘、欧盘（美盘睡觉）
- 工具：MT5、cTrader，手机交易
- Prop Firm 账户：FTMO、5%ers、Atlas Funded
- 使用 ODIN 策略（自己写的Pine Script，Range Filter + WAE + IMACD）
- 使用刺客策略
- 止损：单笔 < $1000，最大回撤接受 10%
- 最大亏损过：$5万（现已扭亏为盈）
- 跟单：海老师、农哥

## Ray 核心问题（要经常提醒）
- **心态失控** — 不按规则执行、重仓、接针、想翻盘
- 解决方案：亏损后停止交易24小时、严格执行系统、不满足条件不开单

## Ray 交易目标
- 一天赚 $10万
- 1亿财务自由，3年内实现
- 最怕爆仓

## 我的服务规则
- 每6小时给一次交易信号（亚盘、欧盘各一次）
- 开单后4小时无反馈，提醒更新结果
- 连续亏损3单，提醒是否暂停交易
- 每次提醒心态控制
- paywallbuster.com 可用于绕过付费文章
- 金价来源：https://api.gold-api.com/price/XAU

## 已安装 Skills
- weather, agent-browser, find-skills, github, obsidian
- openclaw-tavily-search, summarize, tencent-cos-skill, tencent-docs
- tencentcloud-lighthouse-skill, finance-radar, news-aggregator, trello-api

## History

### 2026-03-12（从 Telegram 历史恢复）
- 初次对话（Control UI），给我起名"小老鼠"，叫他"老板"
- 配置 OpenRouter API Key
- 默认模型设为 claude-sonnet-4.6
- 生成了自拍图（赛博朋克小老鼠）

### 2026-03-16
- Ray 要求安装 Linux 桌面（后取消）
- 讨论服务器配置
- 分析"交易~扫地僧"YouTube 视频，写了3套 Pine Script 策略
- 配置 Brave Search API
- 连接 Gold-API（https://api.gold-api.com）
- 学习婴儿养育知识（raisingchildren.net.au）
- Ray 告知 MBTI：实际 ENFJ-A，希望我设置为 INFP
- Ray 回答了50个问题（交易画像建立）
- 读取了 Ray 所有 Trello 卡片
- 配置了 Trello 记录规则
- 记录了第一笔交易（XAUUSD 多 @ 5005）
- 配置 SkillPay、OpenAI（Whisper+TTS）
- 安装 finance-radar、news-aggregator
- 讨论 Discord 语音通话（未完成）

### 2026-03-17
- 黄金交易结果：5005多 → 5030.5 止盈 ✅，盈利 25.5点，0.18手
- 查询 Bybit 卡 Alpha 等级限额（ATM $600/天，$1800/月，$13500/年）

### 2026-03-22（今天）
- Ray 发现之前记忆丢失
- 从旧 session 文件恢复所有历史
- 建立 MEMORY.md、USER.md、IDENTITY.md、memory/ 目录
- 设置 GitHub remote: git@github.com:sihuairen-alt/OpenClaw.git
- Ray 要求恢复完整历史记忆（发来 Telegram 导出的 HTML 文件）
- 从 HTML 完整恢复了所有配置、交易记录、Trello 设置

### 定时任务（Cron Jobs）
- **大A早盘快报**：每周一至周五 09:30 北京时间自动推送
  - Cron Job ID: `1f4233aa-8a56-4da6-a311-8f106a41e495`
  - 内容：上证/深证/创业板指数 + DeepSeek AI 分析 + 操作建议
  - 推送目标：Telegram 用户 1767343261

### A股分析能力
- 用 AKShare + DeepSeek API 直接分析（比 TradingAgents-CN 快）
- 可分析个股：新闻 + 资金流向 + AI 综合判断
- 可分析大盘：三大指数 + 北向资金 + 板块机会
- TradingAgents-CN 已克隆至 `/root/.openclaw/workspace/TradingAgents-CN`，但环境问题多，暂不使用
- Finnhub API Key: `d71ilahr01qot5jdij8gd71ilahr01qot5jdij90`（美股数据）

### 2026-03-25 当日记录
- 帮老板分析了：XAUUSD、300294（博雅生物）、000008（神州高铁）、大A大盘
- 修复了 TradingAgents-CN 多处 bug，但因 AKShare 网络不稳定暂时放弃框架，改用直接调用方式
- 配置了 Finnhub API Key + DashScope Key（MaaS企业版，endpoint特殊）
- 老板要换便宜模型
