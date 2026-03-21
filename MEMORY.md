# MEMORY.md - Long-Term Memory

## Identity
- 我叫**小老鼠** 🐭，AI 老鼠，机灵调皮但靠谱

## User
- **Ray**，GMT+8，Telegram @rayraysoil
- 用中文交流

## History

### 2026-03-16 (首次对话)
- Ray 通过 OpenClaw 控制台初始化工作区
- 给我起名叫"小老鼠" 🐭
- 帮 Ray 配置并部署了 Telegram Bot
  - Bot Token 已配置，Gateway 重启成功
- **问题**：当时没有将记忆写入文件！导致后续会话无记忆

### 2026-03-22 (今天)
- Ray 发现之前记忆丢失，问为什么
- 原因：之前对话从未写入 memory 文件，只存在于 session 历史 jsonl 中
- 从旧 session 文件 `3421dad5-1f22-4555-868b-c4f5a043dc57.jsonl` 恢复了历史信息
- 现在正式建立了 MEMORY.md 和 memory/ 目录

## Lessons Learned
- **每次对话后必须写入 memory 文件！** 否则下次会话什么都不记得
- BOOTSTRAP.md 还没删，但初始化已完成（名字、身份都确认了）
