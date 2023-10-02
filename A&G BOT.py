import logging
import time
import os
from dotenv import load_dotenv
from telegram import __version__ as TG_VER

from Change_Name import change_name
from Chassis_Update import correct_chassisNO
from Niid_Correction import correct_regNoNiid
from Niid_RegandChassis_correction import correct_reg_and_chassisNo_Niid
from Niid_chassis_only import correct_chassisNo_Niid
from VerifyPolicy import verify_policy
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



FIRST_CHOICE, CHOOSING, REG_CHOICE, CHASIS_CHOICE, VERIFY_CHOICE, CHASSIS_ONLY_CHOICE, NAME_CHOICE = range(
    7)


# Reply keyboards
reply_keyboard = [
    ["Scratch Card Platform", "E-PIN Platform"],
    ["Cancel❌"]
]
reply_keyboard2 = [
    ["Reg Correction", "Reg and Chassis Correction"],
    ["Chassis Correction", "Verify Policy"],
    ["Change Name"],
    ["Cancel❌"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)



# Loadinng and getting the enviromet variales
load_dotenv()
THIRD_PARTY_PLATFORM_LINK = os.getenv("3RD_PARTY_PLATFORM_LINK")
THIRD_PARTY_PLATFORM_EMAIL = os.getenv("3RD_PARTY_PLATFORM_EMAIL")

E_PIN_PARTY_PLATFORM_LINK = os.getenv('E_PIN_LINK')
E_PIN_PARTY_PLATFORM_EMAIL = os.getenv('E_PIN_EMAIL')

PLATFORMS_PASSWORD = os.getenv("PLATFORMS_PASSWORD")



# Starts the converstaion with the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Good Day I'm A&G Policy Corrections Bot.\n"
        "How may i help you today?\nIn what platform would you like to make corrections?",
        reply_markup=markup,
    )

    return FIRST_CHOICE

#Getting the Platform link from the choice the user will make when asked the pltform in which corrections will be made
def getLink(PLATFORM_CHOICE):
    Scratch_Card_Platform_Link = THIRD_PARTY_PLATFORM_LINK
    E_PIN_LINK = E_PIN_PARTY_PLATFORM_LINK
    if PLATFORM_CHOICE == 'Scratch Card Platform':
        email = 'mayowa_admin'
        password = 'Gbohunmi17'
        link = Scratch_Card_Platform_Link
        return link,email,password,PLATFORM_CHOICE
    else:
        email = 'mayowa1022'
        password = 'Gbohunmi17'
        link = Scratch_Card_Platform_Link
        return E_PIN_LINK,email,password,PLATFORM_CHOICE


# ask for the platform in which updates will be made
async def Platform_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    text = update.message.text
    global PLATFORM_LINK
    PLATFORM_LINK = getLink(text)

    if PLATFORM_LINK[3] == 'Scratch Card Platform':
        await update.message.reply_text(
            "Policy corrections will will be updated on the Scratch Platform\n"
            "What correction would you like to make?",
            reply_markup=markup2,
        )
    else:
        await update.message.reply_text(
            "Policy corrections will will be updated on the E_PIN Platform\n"
            "What correction would you like to make?",
            reply_markup=markup2,
        )


    return CHOOSING


# E_PIN PLATFORM FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------


# SCRATCH CARD PLTFROM FUNCTIONS
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

    POLICY_NUMBER = POLICY_INFO[0]
    REG_NUMBER = POLICY_INFO[1]
    print(POLICY_INFO)
    print(POLICY_NUMBER)
    print(REG_NUMBER)

    async def callback_30(context: ContextTypes.DEFAULT_TYPE):
        INCORRECT_REGNUMBER = correct_regNo(POLICY_NUMBER, REG_NUMBER,PLATFORM_LINK)
        if INCORRECT_REGNUMBER == 'Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed':
            await context.bot.send_message(chat_id=chat_id, text='Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed')
        else:
            await context.bot.send_message(chat_id=chat_id, text='Updated the policy on A&G third party platform ✅')
            correct_regNoNiid(POLICY_NUMBER, REG_NUMBER, INCORRECT_REGNUMBER)
            await context.bot.send_message(chat_id=chat_id, text='Updated the policy on NIID ✅')
            await context.bot.send_message(chat_id=chat_id, text='Policy Update Successful ✅', reply_markup=ReplyKeyboardRemove())
            print('Done✅')


    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'{context.error}')
        await context.bot.send_message(chat_id=chat_id, text=f'Sorry there might be a network error please try again', reply_markup=ReplyKeyboardRemove())

    application.add_error_handler(error)
    job_queue.run_once(callback_30, 0.2)
    return ConversationHandler.END


async def reg_and_chassis_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    await update.message.reply_text(f"This is your Policy details {text.upper()}")
    await update.message.reply_text(f"Working on it👨‍💻")
    POLICY_INFO = text.upper().split(',')
    print(POLICY_INFO)
    print(POLICY_INFO[0])
    print(POLICY_INFO[1])
    print(POLICY_INFO[2])

    POLICY_NUMBER = POLICY_INFO[0]
    REG_NUMBER = POLICY_INFO[1]
    CHASSIS_NUMBER = POLICY_INFO[2]

    async def callback_30(context: ContextTypes.DEFAULT_TYPE):
        # Getting the Incorrect reg number form the function

        INCORRECT_REGNUMBER = correct_reg_and_chassisNO(POLICY_NUMBER, REG_NUMBER,CHASSIS_NUMBER,PLATFORM_LINK)
        if INCORRECT_REGNUMBER == 'Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed':
            await context.bot.send_message(chat_id=chat_id,
                                           text='Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed')
        else:
            await context.bot.send_message(chat_id=chat_id, text='Updated the policy on A&G third party platform ✅')
            correct_reg_and_chassisNo_Niid(POLICY_NUMBER, REG_NUMBER, INCORRECT_REGNUMBER,CHASSIS_NUMBER)
            await context.bot.send_message(chat_id=chat_id, text='Updated the policy on NIID ✅')
            await context.bot.send_message(chat_id=chat_id, text='Policy Update Successful ✅', reply_markup=ReplyKeyboardRemove())
            print('Done✅')

        async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await context.bot.send_message(chat_id=chat_id, text='Sorry there might be a network error please try again', reply_markup=ReplyKeyboardRemove())


        application.add_error_handler(error)


    job_queue.run_once(callback_30, 0.2)

    return ConversationHandler.END

# Verify Policy Function

async def verify_policies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    await update.message.reply_text(f"This is your Policy certificate Number {text.upper()}")
    await update.message.reply_text(f"Working on it👨‍💻")
    POLICY_NUMBER = text.upper()
    print(POLICY_NUMBER)

    async def callback_30(context: ContextTypes.DEFAULT_TYPE):
        POLICY_DATA = verify_policy(POLICY_NUMBER,PLATFORM_LINK)
        if POLICY_DATA == "There is no Existing Policy Record for the Certificate Number you Typed":
            await context.bot.send_message(chat_id=chat_id, text='There is no Existing Policy Record for the Certificate Number you Typed')
        else:
            All_DATA = "\n".join(POLICY_DATA)
            await context.bot.send_message(chat_id=chat_id, text='Record')
            await context.bot.send_message(chat_id=chat_id, text=f'{All_DATA.upper()}',
                                           reply_markup=ReplyKeyboardRemove())
            print('Done✅')


    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=chat_id, text='Sorry there might be a network error please try again', reply_markup=ReplyKeyboardRemove())

    job_queue.run_once(callback_30, 0.2)
    application.add_error_handler(error)

    return ConversationHandler.END


async def chassis_OnlyChoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    await update.message.reply_text(f"This is your Policy details {text.upper()}")
    await update.message.reply_text(f"Working on it👨‍💻")
    POLICY_INFO = text.upper().split(',')

    POLICY_NUMBER = POLICY_INFO[0]
    CHASSIS_NUMBER = POLICY_INFO[1]
    print(POLICY_INFO)
    print(POLICY_NUMBER)
    print(CHASSIS_NUMBER)

    async def callback_30(context: ContextTypes.DEFAULT_TYPE):

        REG_NUMBER = correct_chassisNO(POLICY_NUMBER, CHASSIS_NUMBER,PLATFORM_LINK)
        if REG_NUMBER == 'Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed':
            await context.bot.send_message(chat_id=chat_id,
                                           text='Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed')
        else:
            await context.bot.send_message(chat_id=chat_id, text='Updated the policy on A&G third party platform ✅')
            # Since the agent only wants to update the chasis number that means the reg number on the policy is correct so
            # I copied the reg number form the policy and im updating the policy on NIIID
            correct_chassisNo_Niid(POLICY_NUMBER, REG_NUMBER, CHASSIS_NUMBER, )
            await context.bot.send_message(chat_id=chat_id, text='Updated the policy on NIID ✅')
            await context.bot.send_message(chat_id=chat_id, text='Policy Update Successful ✅', reply_markup=ReplyKeyboardRemove())
            print('Done✅')


    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=chat_id, text='Sorry there might be a network error please try again', reply_markup=ReplyKeyboardRemove())

    job_queue.run_once(callback_30, 0.5)
    application.add_error_handler(error)

    return ConversationHandler.END


async def changeName(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    await update.message.reply_text(f"This is your Policy Number {text.upper()}")
    await update.message.reply_text(f"Working on it👨‍💻")
    POLICY_INFO = text.split(',')
    print(POLICY_INFO[0])
    print(POLICY_INFO[1])
    print(POLICY_INFO[2])

    POLICY_NUMBER = POLICY_INFO[0]
    FIRSTNAME = POLICY_INFO[1]
    LASTNAME = POLICY_INFO[2]

    async def callback_30(context: ContextTypes.DEFAULT_TYPE):
        ERROR_MESSAGE = change_name(POLICY_NUMBER, FIRSTNAME, LASTNAME,PLATFORM_LINK)
        if ERROR_MESSAGE == 'Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed':
            await context.bot.send_message(chat_id=chat_id,
                                           text='Sorry. The Policy Number you entered does not exist or may have expired and has not been renewed')
        else:
            await context.bot.send_message(chat_id=chat_id, text='Name Changed✅', reply_markup=ReplyKeyboardRemove())
            time.sleep(0.5)
            print('Done✅')

    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=chat_id, text='Sorry there might be a network error please try again', reply_markup=ReplyKeyboardRemove())

    job_queue.run_once(callback_30, 0.5)
    application.add_error_handler(error)

    return ConversationHandler.END

# custom ask the details of the policy


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Send the policy number and the Correct Reg number\n \nPlease make sure the '
        'information you provide is correct\nWrite The policy and Reg Number in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'policyNumber,regNumber')

    return REG_CHOICE


# runs the correction for the chassis number and reg number
async def another_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Send the policy number, Correct Reg number, and the chassis number\n \nPlease make '
        'sure the'
        'information you provide is correct\nWrite The details in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'policyNumber,regNumber,chassisNumber')

    return CHASIS_CHOICE

# verifies the policy


async def verify_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text("Send the correct Certificate Number\n"
                                    'Make sure the information you provide is correct\nWrite The details in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'certificateNumber',

    )

    return VERIFY_CHOICE

# runs the correction for chassis number only


async def chasis_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text("Send the correct required Policy details\n"
                                    'Make sure the information you provide is correct\nWrite The details in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'policyNumber,chassisNumber')

    return CHASSIS_ONLY_CHOICE


async def change_name_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text("Send the correct required Policy details\n"
                                    'Make sure the information you provide is correct\nWrite The details in this format👇')
    # time.sleep(1)
    await update.message.reply_text(
        'policyNumber,firstname,lastname')

    return NAME_CHOICE

# CANCELS THE OPERATION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Operation Canceled",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

# LOGS ERROR


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# def main() -> None:


if __name__ == "__main__":
    """Run the bot."""

    # #Clearing the console one the Authentication is complete
    # def clear_console():
    #     os.system('cls' if os.name == 'nt' else 'clear')
    # clear_console()

    application = Application.builder().token(
        "6679542308:AAFwAJJ3wIj5LZ9fxjm_SPS07N8mpJlrVuw").read_timeout(500).write_timeout(500).build()
    job_queue = application.job_queue

    # Add conversation handler with the states CHOOSING, REG_CHOICE, CHASISS_CHOICE, VERIFY_CHOICE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start, block=False)],
        states={
            FIRST_CHOICE: [
                MessageHandler(filters.Regex(
                    "^Scratch Card Platform$"), Platform_choice),
                MessageHandler(filters.Regex(
                    "^E-PIN Platform$"), Platform_choice),
                MessageHandler(filters.Regex("^Cancel") |
                                filters.Regex("^Cancel"), cancel),
            ],
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^Reg Correction"), custom_choice),
                MessageHandler(filters.Regex(
                    "^Reg and Chassis Correction$"), another_choice),
                MessageHandler(filters.Regex(
                    "^Verify Policy$"), verify_choice),
                MessageHandler(filters.Regex(
                    "^Chassis Correction"), chasis_choice),
                MessageHandler(filters.Regex("^Change Name"),
                                change_name_choice),
                MessageHandler(filters.Regex("^Cancel") |
                                filters.Regex("^Cancel"), cancel),

            ],
            REG_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Cancel")), regular_choice
                )
            ],
            CHASIS_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Cancel")), reg_and_chassis_choice
                )
            ],
            VERIFY_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Cancel")), verify_policies
                )
            ],
            CHASSIS_ONLY_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Cancel")), chassis_OnlyChoice
                )
            ],
            NAME_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                         filters.Regex("^Cancel")), changeName
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Cancel"), cancel)],
    )

    application.add_error_handler(error)

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # Create the Application and pass it your bot's token.



