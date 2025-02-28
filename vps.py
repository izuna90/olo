import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

BOT_TOKEN = "7636730003:AAFRKwkdag_9JwLRkwS7vhddut91jqIcJtM"
ALLOWED_USER_ID = 6073143283

async def terminal(update: Update, context: CallbackContext):
    """Executes a shell command via /terminal <command>"""
    user_id = update.effective_user.id
    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text("❌ Unauthorized access.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /terminal <command>")
        return

    command = " ".join(context.args)  # Join the command arguments

    # Restrict dangerous commands
    forbidden_commands = ["rm -rf /", "reboot", "shutdown", "poweroff"]
    if any(cmd in command for cmd in forbidden_commands):
        await update.message.reply_text("❌ This command is not allowed!")
        return

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout if result.stdout else result.stderr
        await update.message.reply_text(f"🖥️ Output:\n```\n{output[:4000]}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("terminal", terminal))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
