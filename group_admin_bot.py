#!/usr/bin/env python3
"""
扫地僧群管理 Bot
- 欢迎新成员
- 检测广告并踢出
"""
import json, urllib.request, urllib.parse, time, re, os, sys

TOKEN = "8149546430:AAEhv7dI2EBelNwnN_sA0OdPHkjcj7L-8cs"
GROUP_ID = -1003634966014  # 扫地僧 The Sweeping Monk 群
ADMIN_ID = 1767343261      # Ray 的 Telegram ID

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# 广告关键词
AD_KEYWORDS = [
    r"加我", r"私聊", r"微信号", r"\bwx\b", r"薅羊毛", r"返利", r"兼职",
    r"日赚", r"月入", r"招募", r"代理", r"佣金", r"点击链接",
    r"赚钱", r"副业", r"免费领", r"扫码", r"拉人",
    r"算法推广", r"信号推广", r"加群",
    # 外部链接（非 YouTube 扫地僧官方）
    r"t\.me/\+(?!R2ib4lr6U0UxZDA1)",  # 非本群邀请链接
]

WELCOME_MSG = """🎉 欢迎 {mention} 加入交易交流大家庭！

📺 关注群主 YouTube：@扫地僧-ray
https://www.youtube.com/@扫地僧-ray
获取专业交易信号和策略分享

📌 群规：
1️⃣ 禁止发广告（其他群组、交易算法推广）
2️⃣ 禁止私加好友推销
3️⃣ 禁止发布外部链接（除非群主授权）
4️⃣ 文明交流，互相尊重
5️⃣ 交易有风险，跟单需谨慎

💬 这里可以：
✅ 交流交易心得
✅ 分享交易信号
✅ 闲聊放松
✅ 向群主提问

🤖 我是喵管家，有问题随时@我

违规将被警告/禁言/踢出，请遵守群规！"""


def api(method, **kwargs):
    url = f"{BASE_URL}/{method}"
    data = urllib.parse.urlencode(kwargs).encode()
    req = urllib.request.Request(url, data=data)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read())
    except Exception as e:
        print(f"API error {method}: {e}")
        return {}

def send_message(chat_id, text, parse_mode="HTML"):
    return api("sendMessage", chat_id=chat_id, text=text, parse_mode=parse_mode)

def kick_user(chat_id, user_id):
    api("banChatMember", chat_id=chat_id, user_id=user_id)
    time.sleep(0.5)
    api("unbanChatMember", chat_id=chat_id, user_id=user_id, only_if_banned=True)

def delete_message(chat_id, message_id):
    api("deleteMessage", chat_id=chat_id, message_id=message_id)

def is_ad(text):
    if not text:
        return False
    for kw in AD_KEYWORDS:
        if re.search(kw, text, re.IGNORECASE):
            return True
    return False

def notify_admin(text):
    send_message(ADMIN_ID, f"🤖 群管理通知：\n{text}")

def process_update(update):
    if "message" not in update:
        return

    msg = update["message"]
    chat_id = msg.get("chat", {}).get("id")

    if chat_id != GROUP_ID:
        return

    # 新成员加入 → 欢迎
    new_members = msg.get("new_chat_members", [])
    for member in new_members:
        if member.get("is_bot"):
            continue
        name = member.get("first_name", "新朋友")
        user_id = member.get("id")
        username = member.get("username", "")
        mention = f"<a href='tg://user?id={user_id}'>{name}</a>"
        welcome = WELCOME_MSG.format(mention=mention)
        send_message(GROUP_ID, welcome)
        print(f"✅ 欢迎: {name} (@{username})")

    # 检测广告 → 删帖踢出
    text = msg.get("text", "") or msg.get("caption", "")
    if text and is_ad(text):
        user = msg.get("from", {})
        user_id = user.get("id")
        user_name = user.get("first_name", "未知")
        username = user.get("username", "")
        msg_id = msg.get("message_id")

        delete_message(GROUP_ID, msg_id)
        kick_user(GROUP_ID, user_id)

        print(f"🚫 踢出广告用户: {user_name} (@{username})")
        notify_admin(
            f"🚫 已踢出广告用户\n"
            f"用户：{user_name} (@{username})\n"
            f"ID：{user_id}\n"
            f"内容：{text[:150]}"
        )

def main():
    print("🤖 扫地僧群管理 Bot 启动...")
    offset = 0

    offset_file = "/root/.openclaw/workspace/.bot_offset"
    if os.path.exists(offset_file):
        try:
            with open(offset_file) as f:
                offset = int(f.read().strip())
        except:
            offset = 0

    print(f"✅ 启动完成，offset={offset}")

    while True:
        try:
            url = f"{BASE_URL}/getUpdates?offset={offset}&timeout=30&allowed_updates=[\"message\"]"
            resp = json.loads(urllib.request.urlopen(url, timeout=35).read())
            updates = resp.get("result", [])

            for update in updates:
                try:
                    process_update(update)
                except Exception as e:
                    print(f"处理错误: {e}")
                offset = update["update_id"] + 1

            with open(offset_file, "w") as f:
                f.write(str(offset))

        except KeyboardInterrupt:
            print("\n⛔ 已停止")
            break
        except Exception as e:
            print(f"轮询错误: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
