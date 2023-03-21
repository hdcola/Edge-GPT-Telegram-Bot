from telegram import Bot, BotCommand, Update
from telegram.ext import ContextTypes
import database as db
import edge_tts
import io
import utils as ut


async def updatecmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if await set_command(update.get_bot()):
        await update.effective_message.reply_text(
            "Leave the conversation and come back, you will see the updated command prompt"
        )


async def update_cookies_file(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    cid = ut.cid(update)
    if cid in ut.settings("admin"):
        if db.cached(cid):
            if update.message.document:
                file = await update.message.document.get_file()
                await file.download_to_drive(custom_path=ut.path("cookies"))
                await update.effective_message.reply_text(
                    "updated cookies.json"
                )
            else:
                await ut.send(update, "Please send a file to save")


async def conv_voice(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    text = " ".join(context.args)
    if not text:
        await update.effective_message.reply_text(
            "Please use '/v message' to send the message you want to convert to speech"
        )
        return

    cid = update.effective_chat.id
    comm = edge_tts.Communicate(text, db.voice(cid))
    with io.BytesIO() as out:
        async for message in comm.stream():
            if message["type"] == "audio":
                out.write(message["data"])
        out.seek(0)
        await update.effective_message.reply_voice(out)


async def set_command(bot: Bot) -> bool:
    commands = [
        BotCommand("new", "New a topic"),
        BotCommand("upcmd", "Update command list"),
        BotCommand("v", "Converts your message into speech"),
        BotCommand("settings", "Change your settings"),
    ]
    return await bot.set_my_commands(commands)
