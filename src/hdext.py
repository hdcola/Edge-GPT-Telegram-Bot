from telegram import Bot, BotCommand, Update
from telegram.ext import ContextTypes


async def updatecmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if await set_command(update.get_bot()):
        await update.effective_message.reply_text(
            "Leave the conversation and come back, you will see the updated command prompt"
        )


async def set_command(bot: Bot) -> bool:
    commands = [
        BotCommand("new", "New a topic"),
        BotCommand("upcmd", "Update command list"),
        BotCommand("settings", "Change your settings"),
    ]
    return await bot.set_my_commands(commands)
