from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID, SEARCH_TIMEOUT

# ভিডিও লিস্ট
VIDEOS = {
    "movie1": [101, 102],
    "movie2": [201]
}

# বট ক্লায়েন্ট
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ---------------------
# /start কমান্ড
# ---------------------
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Welcome! আমি আপনার বট। এখানে আপনি মুভি সার্চ করতে পারবেন।\n\n"
        "👉 ব্যবহার করুন: /search movie1"
    )

# ---------------------
# /search কমান্ড
# ---------------------
@app.on_message(filters.command("search"))
async def search(client, message):
    query = " ".join(message.command[1:]).lower()
    if query in VIDEOS:
        buttons = []
        for idx in range(len(VIDEOS[query])):
            buttons.append([InlineKeyboardButton(f"Watch Part {idx+1}", callback_data=f"{query}:{idx}")])
        reply_markup = InlineKeyboardMarkup(buttons)
        sent_msg = await message.reply_text("Select video to watch:", reply_markup=reply_markup)

        # SEARCH_TIMEOUT পরে মেসেজ ডিলিট
        asyncio.get_event_loop().call_later(
            SEARCH_TIMEOUT,
            lambda: asyncio.create_task(sent_msg.delete())
        )
    else:
        await message.reply_text("No video found.")

# ---------------------
# Inline বাটন ক্লিক হ্যান্ডলার
# ---------------------
@app.on_callback_query()
async def button_click(client, callback_query):
    movie, idx = callback_query.data.split(":")
    idx = int(idx)

    video_id = VIDEOS[movie][idx]

    # ভিডিও ফরওয়ার্ড
    await client.forward_messages(
        chat_id=callback_query.message.chat.id,
        from_chat_id=CHANNEL_ID,
        message_ids=video_id
    )

    # যদি পরবর্তী পার্ট থাকে, দেখান "Next Part" বাটন
    next_idx = idx + 1
    if next_idx < len(VIDEOS[movie]):
        keyboard = [[InlineKeyboardButton("Next Part", callback_data=f"{movie}:{next_idx}")]]
        await callback_query.message.reply_text("Next part available:", reply_markup=InlineKeyboardMarkup(keyboard))

# ---------------------
# বট চালান
# ---------------------
app.run()
