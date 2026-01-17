
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from game_manager import Game
from words import WORDS

TOKEN = os.getenv("TOKEN")
games = {}

def get_game(chat_id):
    if chat_id not in games:
        games[chat_id] = Game(chat_id)
    return games[chat_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Unirme", callback_data="join")],
        [InlineKeyboardButton("▶️ Empezar", callback_data="begin")]
    ]
    await update.message.reply_text(
        "🎭 Impostor de Palabras",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    game = get_game(query.message.chat.id)
    user = query.from_user

    if query.data == "join":
        game.add_player(user.id, user.first_name)
        await query.message.reply_text(f"{user.first_name} se unió al juego.")

    elif query.data == "begin":
        if not game.can_start():
            await query.message.reply_text("Se necesitan al menos 3 jugadores.")
            return

        word, impostors = game.start_game(WORDS)
        for uid in game.players:
            if uid in impostors:
                await context.bot.send_message(uid, "😈 Eres el IMPOSTOR")
            else:
                await context.bot.send_message(uid, f"✅ Palabra secreta: {word}")

        await query.message.reply_text("🕵️ El juego comenzó.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
