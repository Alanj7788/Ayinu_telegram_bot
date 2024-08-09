import telegram.ext
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os



load_dotenv()
TOKEN = os.getenv('TOKEN')

# Load team members data from JSON file
with open('team_members.json', 'r', encoding='utf-8') as file:
    team_members = json.load(file)

def start(update, context):
    # Get the user's first name and username
    user_first_name = update.message.from_user.first_name
    user_username = update.message.from_user.username

    # Create a greeting message
    greeting_message = f"Hi {user_username or user_first_name}!"

    # Reply with the greeting message
    update.message.reply_text(greeting_message)
    update.message.reply_text(
        """
        Welcome to Ayinu Telegram Bot!", Please follow these commands:-
        
    /start: Start the Ayinu Bot.
    /info: Learn about the Ayinu Bot.
    /members: View Ayinu members.
        """
    )

def info(update, context):
    # Create an inline keyboard with buttons for each team member
    keyboard = []
    for member_name in team_members:
        keyboard.append([InlineKeyboardButton(member_name, callback_data=member_name)])

    # Create an inline keyboard markup
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the info message with the inline keyboard
    info_message = (
        "This bot is designed to introduce you to the Ayinu team. We are 13 diverse members, "
        "including pro coders, content creators, video editors, and academic achievers. "
        "Get to know us and our different areas of expertise!"
    )
    update.message.reply_text(info_message, reply_markup=reply_markup)

def member_info(update, context):
    query = update.callback_query
    member_name = query.data

    # Check if member name exists in team_members
    if member_name in team_members:
        member_data = team_members[member_name]

        # Construct the detailed information message
        info_message = f"**{member_name}**\n\n"
        info_message += f"{member_data['bio']}\n\n"
        info_message += "**Skills:** " + ", ".join(member_data.get('skills', [])) + "\n"
        info_message += f"**Education:** {member_data.get('education', '')}\n"
        info_message += "**Contact:** " + member_data.get('contact', '')

        # Send the detailed information message
        query.message.reply_text(info_message, parse_mode='Markdown')
    else:
        query.message.reply_text("Member information not found.")

def stop(update, context):
    update.message.reply_text("Stopping the bot. Goodbye!")
    updater.stop()
    updater.is_idle = False

def search_skills(update, context):
    # Get the skills entered by the user
    user_skills = update.message.text.split()[1:]  # Remove "/search_skills"

    # Find members with matching skills
    matching_members = []
    for member_name, member_data in team_members.items():
        member_skills = member_data.get('skills', [])
        if any(skill in member_skills for skill in user_skills):
            matching_members.append(member_name)

    # Check if any members were found
    if matching_members:
        # Create an inline keyboard with buttons for matching members
        keyboard = []
        for member_name in matching_members:
            keyboard.append([InlineKeyboardButton(member_name, callback_data=member_name)])

        # Create an inline keyboard markup
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the search results message
        search_message = f"Found members with skills: {', '.join(user_skills)}"
        update.message.reply_text(search_message, reply_markup=reply_markup)
    else:
        update.message.reply_text("No members found with the specified skills.")

# Set up the Telegram updater and dispatcher
updater = telegram.ext.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add handlers for commands and callbacks
dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('info', info))
dispatcher.add_handler(telegram.ext.CallbackQueryHandler(member_info))
dispatcher.add_handler(telegram.ext.CommandHandler('stop', stop))
dispatcher.add_handler(telegram.ext.CommandHandler('search_skills', search_skills))


# Start polling for updates
updater.start_polling()

# Run the bot until Ctrl-C is pressed or an error occurs
updater.idle()
