# (c) @RoyalKrrishna
import urllib.parse
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from configs import Config

# Telethon Bot Client
bot = TelegramClient("video_search_bot", Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)

# Force Subscription check
async def check_subscription(user_id):
    if Config.FORCE_SUB == "False":
        return True
    try:
        await bot(GetParticipantRequest(channel=Config.UPDATES_CHANNEL, participant=user_id))
        return True
    except:
        return False

# /start হ্যান্ডলার
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"হ্যালো! 😃\n\n"
        f"আমি {Config.BOT_USERNAME}।\n"
        f"চ্যানেল @{Config.UPDATES_CHANNEL_USERNAME} এ থাকা ভিডিও সার্চ করতে আমাকে ব্যবহার করুন।\n\n"
        f"ভালোভাবে কাজ করার জন্য চ্যানেলে জয়েন করুন।",
        buttons=Button.url("Join Updates Channel", f"https://t.me/{Config.UPDATES_CHANNEL_USERNAME}")
    )

# Message handler
@bot.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.message.post or event.text.startswith("/"):
        return

    query = event.text.strip()
    if not query:
        return

    # Force subscription
    if Config.FORCE_SUB == "True":
        is_subscribed = await check_subscription(event.sender_id)
        if not is_subscribed:
            await event.reply(
                f"Hey! Join @{Config.UPDATES_CHANNEL_USERNAME} to use me 😃",
                buttons=Button.url("Join Updates Channel", f"https://t.me/{Config.UPDATES_CHANNEL_USERNAME}")
            )
            return

    found = False
    async for msg in bot.iter_messages(Config.CHANNEL_ID, search=query, limit=10):
        if msg.video or msg.document:
            await bot.send_message(event.chat_id, msg)
            found = True
        elif msg.text:
            await bot.send_message(event.chat_id, msg.text)
            found = True

    if not found:
        google_link = f"https://www.google.com/search?q={urllib.parse.quote(query + ' movie')}"
        await event.reply(
            f"❌ No results found for **{query}**\n\n"
            f"🔎 [Search on Google]({google_link})",
            link_preview=False
        )

print("🚀 JackpotFilmBot Started!")
bot.run_until_disconnected()
