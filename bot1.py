import os
from pyrogram import Client, filters
from pyrogram.types import Message

BOT_TOKEN = "7816494413:AAFLC5UBM2c7vOILrMkHbmAUPC05rKDOeuo"

app = Client(
    "bot",
    api_id=7706053,
    api_hash="a87b492b8fe379c5fd63793d29ca7a27",
    bot_token=BOT_TOKEN,
    in_memory=True
)

async def progress(current, total, message, file_name):
    if total == 0:
        return

    percent = int(current * 100 / total)

    if percent % 10 == 0:
        try:
            await message.edit_text(
                f"⬇️ {file_name}\n📊 التقدم: {percent}%"
            )
        except:
            pass

@app.on_message(filters.document)
async def handle_docs(client: Client, message: Message):
    doc = message.document
    file_name = doc.file_name

    if not file_name.lower().endswith(".db"):
        await message.reply("❌ مسموح فقط ملفات .db")
        return

    status = await message.reply(
        f"⬇️ بدء تحميل {file_name}\n"
        f"📦 الحجم: {doc.file_size / (1024**3):.2f} GB"
    )

    try:
        await message.download(
            file_name=os.path.abspath(file_name),  # 👈 نفس المجلد
            progress=progress,
            progress_args=(status, file_name)
        )
    except Exception as e:
        await status.edit_text(
            f"❌ فشل تحميل {file_name}\n{e}"
        )
        return

    await status.edit_text(f"✅ اكتمل تحميل {file_name}")

def run():
	app.run()
