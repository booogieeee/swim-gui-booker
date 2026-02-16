from swim_gui import SwimBookerApp
from pathlib import Path
#subprocess for bot to not crash gui
import subprocess
import sys
import threading

import automation

app = SwimBookerApp()

# -- TELEGRAM BOT --
bot_process = None

def start_bot():
    global bot_process
    if bot_process and bot_process.poll() is not None:
        return
    #turn bot on
    print("BOT ON")

    bot_process = subprocess.Popen(
        [sys.executable, f"{Path(__file__).resolve().parent}/telegram_bot.py"], #command to run, equivalent to "python telegram_bot.py" in terminal
        stdin=subprocess.DEVNULL
    )

def stop_bot():
    global bot_process
    if bot_process is None:
        return
    #turn bot off
    print("BOT OFF")

    bot_process.terminate()
    bot_process.wait()
    bot_process = None


#functions for traces
def set_telegram_bot(*_): # *_ basically just ignores multiple variables when unpacking, i dont need them so ya
    if app.run_telegram_bot.get() == 1:
        start_bot()
    else:
        stop_bot()

#attach traces (listeners)
app.run_telegram_bot.trace_add("write", set_telegram_bot)
app.window.protocol("WM_DELETE_WINDOW", lambda: app.close(close_callback=stop_bot))

threading.Thread(target=automation.start, daemon=True).start()

app.run()