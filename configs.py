 # (c) @RoyalKrrishna

import urllib.parse
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest

# Config
class Config(object):
    API_ID = 24776633
    API_HASH = "57b1f632044b4e718f5dce004a988d69"
    BOT_TOKEN = "8210471056:AAEc76RNEX1w32M7WfyY3R8uKzEBy4aOb8s"
    BOT_USERNAME = "jacpotfilmbot_bot"
    BOT_OWNER = 7170990925
    CHANNEL_ID = -1002912984408
    UPDATES_CHANNEL = -1002995070932
    UPDATES_CHANNEL_USERNAME = "uddinee"
    FORCE_SUB = True
    RESULTS_PER_PAGE = 5

# Bot client
bot = TelegramClient("video_search_bot", Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)

# Subscription check
async def check_subscription(user_id):
    if not Config.FORCE_SUB:
        return True
    try:
        await bot(GetParticipantRequest(channel=Config.UPDATES_CHANNEL, participant=user_id))
        return True
    except:
        return False

# /start handler
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"হ্যালো! 😃\n\n"
        f"আমি @{Config.BOT_USERNAME}।\n"
        f"চ্যানেল @{Config.UPDATES_CHANNEL_USERNAME} এ থাকা ভিডিও সার্চ করতে আমাকে ব্যবহার করুন।",
        buttons=Button.url("Join Updates Channel", f"https://t.me/{Config.UPDATES_CHANNEL_USERNAME}")
    )

# Dictionary to store search results for pagination
user_searches = {}

# Search handler
@bot.on(events.NewMessage(incoming=True))
async def handler(event):
    if getattr(event.message, "post", False) or (event.text and event.text.startswith("/")):
        return

    query = event.text.strip() if event.text else ""
    if not query:
        return

    # Force subscription
    if Config.FORCE_SUB:
        is_subscribed = await check_subscription(event.sender_id)
        if not is_subscribed:
            await event.reply(
                f"Hey! Join @{Config.UPDATES_CHANNEL_USERNAME} to use me 😃",
                buttons=Button.url("Join Updates Channel", f"https://t.me/{Config.UPDATES_CHANNEL_USERNAME}")
            )
            return

    # Fetch all matching messages
    all_results = []
    async for msg in bot.iter_messages(Config.CHANNEL_ID, search=query):
        if msg.video or msg.document or msg.text:
            all_results.append(msg)

    if not all_results:
        google_link = f"https://www.google.com/search?q={urllib.parse.quote(query + ' movie')}"
        await event.reply(
            f"❌ No results found for **{query}**\n\n"
            f"🔎 [Search on Google]({google_link})",
            link_preview=False
        )
        return

    # Save user search
    user_searches[event.sender_id] = {"query": query, "results": all_results, "page": 0}

    # Show first page
    await send_results(event.sender_id)

# Function to send a page of results
async def send_results(user_id):
    data = user_searches[user_id]
    page = data["page"]
    results = data["results"]
    start = page * Config.RESULTS_PER_PAGE
    end = start + Config.RESULTS_PER_PAGE
    page_results = results[start:end]

    buttons = []
    for idx, msg in enumerate(page_results, start=1):
        if msg.video or msg.document:
            buttons.append([Button.inline(f"Send {idx}", data=f"send_{msg.id}")])
        elif msg.text:
            # Text messages don't need Send button
            await bot.send_message(user_id, msg.text)

    # Pagination buttons
    nav_buttons = []
    if start > 0:
        nav_buttons.append(Button.inline("⬅️ Back", data="back"))
    if end < len(results):
        nav_buttons.append(Button.inline("Next ➡️", data="next"))

    if buttons or nav_buttons:
        await bot.send_message(
            user_id,
            "Here are your search results:",
            buttons=buttons + [nav_buttons] if nav_buttons else buttons
        )

# Callback query handler
@bot.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode("utf-8")
    user_id = event.sender_id

    if user_id not in user_searches:
        await event.answer("❌ Search session expired.")
        return

    search_data = user_searches[user_id]

    if data.startswith("send_"):
        msg_id = int(data.split("_")[1])
        msg = await bot.get_messages(Config.CHANNEL_ID, ids=msg_id)
        if msg.video or msg.document:
            await bot.send_file(user_id, msg)
            await event.answer("✅ Sent to your chat!")
        else:
            await event.answer("❌ Cannot send this message.")
    elif data == "next":
        search_data["page"] += 1
        await event.delete()
        await send_results(user_id)
    elif data == "back":
        search_data["page"] -= 1
        await event.delete()
        await send_results(user_id)

print("🚀 JackpotFilmBot (Multi-video + Pagination + Inline) Started!")
bot.run_until_disconnected()
