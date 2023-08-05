import logging
import time
from typing import Dict

from telegram import __version__ as TG_VER

from Niid_Correction import correct_regNoNiid
from Niid_RegandChassis_correction import correct_reg_and_chassisNo_Niid
from main import correct_regNo
from RegandChasis_correction import correct_reg_and_chassisNO

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, REG_CHOICE, CHASIS_CHOICE = range(4)

reply_keyboard = [
    ["Reg Correction", "Reg and Chassis Correction"],
    ["Cancel"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Good Day I'm A&G Policy Corrections Bot.\n"
        "How may i help you today?\nWhat correction would you like to make?",
        reply_markup=markup,
    )

    return CHOOSING


# the regular choice runs the registration number correction
async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    await update.message.reply_text(f"This is your Policy details {text.upper()}")
    await update.message.reply_text(f"Working on it👨‍💻")
    POLICY_INFO = text.upper().split(',')
    print(POLICY_INFO[0])
    print(POLICY_INFO[1])
    print(POLICY_INFO[2])

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
    application.add_error_handler(error)
    return ConversationHandler.END


async def reg_and_chassis_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    await update.message.reply_text(f"This is your Policy details {text.upper()}")
    await update.message.reply_text(f"Working on it👨‍💻")
    POLICY_INFO = text.upper().split(',')
    print(POLICY_INFO[0])
    print(POLICY_INFO[1])
    print(POLICY_INFO[2])
    print(POLICY_INFO[3])

    POLICY_NUMBER = POLICY_INFO[0]
    REG_NUMBER = POLICY_INFO[1]
    INCORRECT_REGNUMBER = POLICY_INFO[2]
    CHASSIS_NUMBER = POLICY_INFO[3]
    print(POLICY_INFO)
    print(POLICY_NUMBER)
    print(REG_NUMBER)
    print(CHASSIS_NUMBER)

    async def callback_30(context: ContextTypes.DEFAULT_TYPE):
        correct_reg_and_chassisNO(POLICY_NUMBER, REG_NUMBER,CHASSIS_NUMBER)
        await context.bot.send_message(chat_id=chat_id, text='Updated the policy on A&G third party platform ✅')
        time.sleep(0.5)
        correct_reg_and_chassisNo_Niid(POLICY_NUMBER, REG_NUMBER, INCORRECT_REGNUMBER,CHASSIS_NUMBER)
        await context.bot.send_message(chat_id=chat_id, text='Updated the policy on NIID ✅')
        time.sleep(0.5)
        await context.bot.send_message(chat_id=chat_id, text='Policy Update Successful ✅')
        print('Done✅')

    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=chat_id, text='There was an error')

    job_queue.run_once(callback_30, 2)
    application.add_error_handler(error)
    return ConversationHandler.END

# custom ask the details of the policy
async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Send the policy number the Correct Reg number and the incorrect reg number\n \nPlease make sure the '
        'information you provide is correct\nWrite The policy and Reg Number in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'examplepolicynumber,exampleregnumber,exampleincorrectregnumber')

    return REG_CHOICE


# runs the correction for the chassis number
async def another_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Send the policy number, Correct Reg number, incorrect reg number, and the chassis number\n \nPlease make '
        'sure the'
        'information you provide is correct\nWrite The details in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'policynumber,regnumber,eincorrectregnumber,chassisNumber')

    return CHASIS_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
    )

    return CHOOSING


# CANCELS THE OPERATION
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Operation Canceled",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


#LOGS ERROR
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# def main() -> None:


if __name__ == "__main__":
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6679542308:AAFwAJJ3wIj5LZ9fxjm_SPS07N8mpJlrVuw").build()
    job_queue = application.job_queue

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^Reg Correction"), custom_choice),
                MessageHandler(filters.Regex("^Reg and Chassis Correction$"), another_choice),
                MessageHandler(filters.Regex("^Cancel") | filters.Regex("^Cancel"), cancel),

            ],
            REG_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel")), regular_choice
                )
            ],
            CHASIS_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel")), reg_and_chassis_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Cancel"), cancel)],
    )

    application.add_error_handler(error)

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
