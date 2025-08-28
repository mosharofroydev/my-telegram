from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==== আপনার তথ্য ====
API_ID = 24776633   # এখানে আপনার API_ID দিন
API_HASH = "57b1f632044b4e718f5dce004a988d69"  # এখানে আপনার API_HASH দিন
BOT_TOKEN = "8412041699:AAGr1YauyYo7g9iHt6vNtKATt3s_fklqaCc"  # নতুন Bot Token
CHANNEL_ID = -1002912984408   # আপনার প্রাইভেট চ্যানেল ID

# ==== বট তৈরি ====
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Start কমান্ড
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Welcome!\n\n🔍 সার্চ করতে নাম লিখুন..."
    )


# সার্চ সিস্টেম
@app.on_message(filters.text & ~filters.command("start"))
async def search(client, message):
    query = message.text.lower()
    await message.reply_text("⏳ খুঁজছি...")  # যাতে বোঝা যায় সার্চ হচ্ছে

    async for msg in client.search_messages(chat_id=CHANNEL_ID, query=query, limit=10):
        if msg.video:
            await message.reply_video(
                msg.video.file_id,
                caption=msg.caption or "🎬 আপনার ভিডিও",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔗 চ্যানেল", url="https://t.me/yourchannel")]]
                )
            )


print("🤖 Bot is starting...")
app.run()
