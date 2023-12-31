import time
from Niid_Correction import correct_regNoNiid
from main import correct_regNo
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '6679542308:AAFwAJJ3wIj5LZ9fxjm_SPS07N8mpJlrVuw'
BOT_USERNAME: Final = '@A_and_G_bot'
POLICY = ""
REG = ""
Working = False

print('Starting up bot...')


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /Reg Number Correction
async def regcorrection_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Send the policy number the Correct Reg number and the incorrect reg number\n \nPlease make sure the '
        'information you provide is correct\nWrite The policy and Reg Number in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'examplepolicynumber,exampleregnumber,exampleincorrectregnumber')



def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I\'m good!'

    if 'i love python' in processed:
        return 'Remember to subscribe!'

    if f"/regcorrection":

        return 'Working on it👨‍💻'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text
    chat_id = update.message.chat_id


    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    POLICY_INFO = text.split(",")
    POLICY_NUMBER = POLICY_INFO[0]
    REG_NUMBER = POLICY_INFO[1]
    INCORRECT_REGNUMBER = POLICY_INFO[2]
    print(POLICY_INFO)
    print(POLICY_NUMBER)
    print(REG_NUMBER)

    async def callback_30(context: ContextTypes.DEFAULT_TYPE):

        correct_regNo(POLICY_NUMBER, REG_NUMBER)
        await context.bot.send_message(chat_id=chat_id, text='Updated the policy on A&G third party platform ✅')
        time.sleep(0.5)
        correct_regNoNiid(POLICY_NUMBER, REG_NUMBER, INCORRECT_REGNUMBER)
        await context.bot.send_message(chat_id=chat_id, text='Updated the policy on NIID ✅')
        time.sleep(0.5)
        await context.bot.send_message(chat_id=chat_id, text='Policy Update Successful ✅')
        print('Done✅')

    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=chat_id, text='There was an error')

    job_queue.run_once(callback_30, 2)
    app.add_error_handler(error)

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)

        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    job_queue = app.job_queue

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('regcorrection', regcorrection_command))

    # reply after Commands

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)



