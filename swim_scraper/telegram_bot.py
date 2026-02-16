from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application, Defaults
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pprint #pretty
import re

#my own stuff
import swim_api
from data import saving

#.env stuff for bot token security
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("telegram bot token not given. either insert into .env file or replace with token string")


# === COMMAND FUNCTIONS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("bot is running!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is the help command!\n\n" \
    "GENERAL: \n/start\n/help\n\n" \
    "REMINDER: \n/setreminder [first word of location] [start time]<am|pm> ([start month]-[start day] | today) [days to remind]\nEXAMPLE: /setreminder garnet 06:30am 03-02 mon wed fri\n/delreminder [index]\n/reminders")


async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reminders = context.bot_data["reminders"]
    if context.args:
        location, time, date = context.args[0], context.args[1], context.args[2]
        #check location time and date for validity

        days = context.args[3:]

        nextDate = None
        found = None
        #subtract 1 day from date bc api is weird
        if date == "today":
            date = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        else:
            date = f"{datetime.now().year}-{date}"
        
        dt = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)
        dt = dt.strftime("%Y-%m-%d")

        section, nextDate = swim_api.get_data(date=dt)

        print(f"DATE: {date} | NEXT DATE: {nextDate}")
        # -- FIND OBJECT --
        for obj in section:
            if ((str.lower(str.split(obj.location, " ")[0]) == location) and 
            (str.lower(str.split(obj.time, " ")[0] + str.split(obj.time, " ")[1]) == time) and 
            (datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', obj.date), "%a, %b %d, %Y").strftime("%Y-%m-%d") == date)): #convert Sun, Feb 1st, 2026 into 2026-02-01 for example, idk (%a for abbreviate weekday, %b for month, etc.)
                await update.message.reply_text("found! adding to reminders...")

                found = obj
                reminders[found.courseId] = { #to save data in file
                                    "days": days,
                                    "location": found.location,
                                    "time": found.time,
                                    "chat_id": update.effective_chat.id
                                }
                print(f"OBJECT FOUND: {found.location} at {found.time} on {found.date}")
                
                break
            #unnecessarily long print debug, too lazy to shorten lol not that important
            print(f"{str.lower(str.split(obj.location, " ")[0]) == location}, {str.lower(str.split(obj.time, " ")[0]) == time}, {datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', obj.date), "%a, %b %d, %Y").strftime("%Y-%m-%d") == date} - {obj.location}, {str.lower(str.split(obj.time, " ")[0] + str.split(obj.time, " ")[1])}, {obj.date} TO {location}, {time}, {date}")
        
        if not found:
            await update.message.reply_text(f"not found. make sure info is correct: location: {location}, time: {time}, date: {date}")
            print(f"OBJECT NOT FOUND: {location}, {time}, {date}")
        else:
            start_jobs(context.application, reminders)
            saving.save_reminders(reminders)
            await update.message.reply_text(f"sucessfully set reminder!")


#function to send message without user input (reminder)
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data

    course_id = data["course_id"]
    dt = datetime.now() - timedelta(days=1)
    found = swim_api.findLocationFromCourseId(course_id, dt)

    if found:
        await context.bot.send_message(
            chat_id=data["chat_id"],
            text=f"Did you book {found.location} at {found.time} yet? if not, heres the link: {swim_api.generateButtonUrl(found.id, found.rawDate)}" #put link to event register page, as well as yes/no to automatically book
        )
    else:
        print(f"reminder not found! courseid: {course_id}")


async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reminders = context.bot_data["reminders"]
    if reminders != {}:
        if context.args:
            index = context.args[0]

            for i, id in enumerate(reminders):
                if str(i) == index:
                    reminder = reminders[id]
                    location, time, days = reminder["location"], reminder["time"], reminder["days"]
                    saving.delete_reminders(id)
                    del reminders[id]
                    await update.message.reply_text(f"reminder removed for: {location} at {time} on {days}")
                    return
            await update.message.reply_text(f"reminder not found! make sure index is correct")
        else:
            await update.message.reply_text(f"you need to say what you want to remove! (number)")
    else:
        await update.message.reply_text(f"you have no reminders!")


async def display_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reminders = context.bot_data["reminders"]
    await update.message.reply_text(f"all reminders: \n{"\n".join(f"{i}: {pprint.pformat(reminder)}" for i, reminder in enumerate(reminders.values()))}")


def initialize(application: Application):
    reminders = saving.load_reminders()
    start_jobs(application, reminders)
    application.bot_data["reminders"] = reminders


def start_jobs(application: Application, reminders: dict):
    # -- REMIND --
    WEEKDAYS = { #convert weekdays to numbers (IN TELEGRAM API SUN = 0, SAT = 6)
        "sun": 0,
        "mon": 1,
        "tue": 2,
        "wed": 3,
        "thu": 4,
        "fri": 5,
        "sat": 6,
    }

    #load data from reminders
    for courseId, reminder in reminders.items():
        days = reminder["days"]
        time = reminder["time"]
        chat_id = reminder["chat_id"]
        
        # ...convert weekdays to numbers
        weekdays = []
        for d in days:
            d = d.lower()
            if d not in WEEKDAYS: #some error handling
                print(f"invalid weekday: {d}")
                continue
            weekdays.append(WEEKDAYS[d])
        weekdays = tuple(weekdays) #convert to tuple to use in job_queue
        if not weekdays:
            continue

        #convert reminder time
        splitTime = str.split(time, " ")
        remind_time = datetime.strptime(splitTime[0] + splitTime[1], "%I:%M%p").time()

        #use job_queue to remind 1 day before to book
        application.job_queue.run_daily(
            send_reminder,
            time=datetime.strptime("17:00:00", "%H:%M:%S").time(), #5pm, reasonable time
            days=tuple((weekday-1) % 7 for weekday in weekdays), #weekday-1 to do previous day
            data={
                "chat_id": chat_id,
                "course_id": courseId
            },
            name=f"{courseId}_{weekdays}Before"
        )

        #use job_queue to remind on days specified
        naiveTime = "13:00:00" if remind_time.hour >= 13 else "05:00:00" #1pm if time is after 1pm, else do 5am (earlist possible is 6am i think)

        a = application.job_queue.run_daily(
            send_reminder,
            time=datetime.strptime(naiveTime, "%H:%M:%S").time(),
            days=weekdays,
            data={
                "chat_id": chat_id,
                "course_id": courseId
            },
            name=f"{courseId}_{weekdays}"
        )

        #testing
        application.job_queue.run_once(
            send_reminder,
            when=5,
            data={"chat_id": chat_id, "course_id": courseId}
        )


def main():
    my_timezone = ZoneInfo("America/New_York")

    defaults = Defaults(tzinfo=my_timezone)
    app = ApplicationBuilder().token(TOKEN).defaults(defaults).build()
    
    app.add_handlers(handlers={
        1: [CommandHandler("start", start), CommandHandler("help", help)],
        2: [CommandHandler("setreminder", set_reminder), CommandHandler("delreminder", delete_reminder), CommandHandler("reminders", display_reminders)]
    })

    initialize(app)
    
    app.run_polling()

    

if __name__ == "__main__":
    main()