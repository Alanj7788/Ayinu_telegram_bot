import telegram.ext
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

with open('team_members.json', 'r', encoding='utf-8') as file:
    team_members = json.load(file)
with open('csea_class.json', 'r', encoding='utf-8') as file:
    students_data = json.load(file)


buttons_message = """\
/start : To start the bot.
/creators : Know about Ayinu members
/search_skills : Search Persons based on skills (eg: /search_skills HTML)
/csea : Know about CSEA students
"""

def start(update, context):
    user_first_name = update.message.from_user.first_name
    user_username = update.message.from_user.username

    update.message.reply_text(
        f"Hi {user_username or user_first_name}! "
        "Welcome to the Ayinu Telegram Bot! 🎉 We're thrilled to introduce you to our dynamic team of 13 members. Our group is a blend of pro coders, content creators, video editors, and academic achievers, each bringing unique skills to the table. Get to know us, explore our diverse expertise, and see how we make a difference together!"
    )
    update.message.reply_text(buttons_message)

def ayinu_info(update, context):
    keyboard = [[InlineKeyboardButton(member_name, callback_data=member_name)] for member_name in team_members]
    ayinu_reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ayinu Creators", reply_markup=ayinu_reply_markup)

def ayinu_member_info(update, context):
    query = update.callback_query
    member_name = query.data

    if member_name in team_members:
        member_data = team_members[member_name]
        info_message = f"**{member_name}**\n\n"
        info_message += f"{member_data['bio']}\n\n"
        info_message += "**Skills:** " + ", ".join(member_data.get('skills', [])) + "\n"
        info_message += f"**Education:** {member_data.get('education', '')}\n"
        info_message += "**Contact:** " + member_data.get('contact', '')

        query.message.reply_text(info_message, parse_mode='Markdown')
    else:
        query.message.reply_text("Member not found in Ayinu Creators.")
        print(f"Member {member_name} not found in team_members.")  # Debugging

    query.message.reply_text(buttons_message)

def csea_info(update, context):
    students = students_data['students']
    keyboard = [[InlineKeyboardButton(f"Roll No: {roll_no}", callback_data=str(roll_no))] for roll_no in students]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("CSEA Students", reply_markup=reply_markup)

def csea_member_info(update, context):
    query = update.callback_query
    roll_no = query.data

    students = students_data['students']
    student = students.get(roll_no, None)

    if student:
        info_message = f"**Name:** {student['name']}\n"
        info_message += f"**Register No:** {student['register_no']}\n"
        info_message += f"**Admission No:** {student['admission_no']}\n"
        info_message += f"**Honors/Minors:** {student['honors_minors']}"
        query.message.reply_text(info_message, parse_mode='Markdown')
    else:
        query.message.reply_text("Student information not found.")
        print(f"Student with Roll No {roll_no} not found in students_data.")  # Debugging statement

    query.message.reply_text(buttons_message)


def handle_callback_query(update, context):
    query = update.callback_query
    data = query.data

    # Ensure that the data is handled properly
    if data in team_members:
        ayinu_member_info(update, context)
    else:
        csea_member_info(update, context)

def search_skills(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Please provide skills to search. Usage: /search_skills HTML")
        return

    user_skills = context.args
    matching_members = [member_name for member_name, member_data in team_members.items() if
                        any(skill in member_data.get('skills', []) for skill in user_skills)]

    if matching_members:
        keyboard = [[InlineKeyboardButton(member_name, callback_data=member_name)] for member_name in matching_members]
        reply_markup = InlineKeyboardMarkup(keyboard)
        search_message = f"Found members with skills: {', '.join(user_skills)}"
        update.message.reply_text(search_message, reply_markup=reply_markup)
    else:
        update.message.reply_text("No members found with the specified skills.")

    update.message.reply_text(buttons_message)

updater = telegram.ext.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('creators', ayinu_info))
dispatcher.add_handler(telegram.ext.CommandHandler('search_skills', search_skills))
dispatcher.add_handler(telegram.ext.CommandHandler('csea', csea_info))
dispatcher.add_handler(telegram.ext.CallbackQueryHandler(handle_callback_query))

updater.start_polling()
updater.idle()
