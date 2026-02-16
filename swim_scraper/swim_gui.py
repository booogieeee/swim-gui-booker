import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pystray #tray library
from PIL import Image

import webbrowser
import sys
from pathlib import Path

import swim_api
import automation

# TODO:
# make already registered courses green
# make automated courses blue, red if failed

class SwimBookerApp: #dont wanna subclass tk.Tk cuz looks better for me like this
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("swim booker")

        self.window.rowconfigure(2, minsize=800, weight=1)
        self.window.columnconfigure(0, minsize=800, weight=1)

        self.unchecked_img = tk.PhotoImage(file=Path(__file__).parent/"assets"/"checkbox_unchecked.png")
        self.checked_img = tk.PhotoImage(file=Path(__file__).parent/"assets"/"checkbox_checked_big.png") # drew this checkmark myself, other one was too small
        self.checkbox_states = {}

        # treeStyle = ttk.Style()
        # treeStyle.configure("Treeview.Heading")
        self.tree = None #ttk.Treeview(window, column=(""), show='headings')
        

        #create ui
        self.create_frames()
        self.create_controls()
        self.create_tree()
        self.create_scrollbar()

    # === ui setup ===
    def create_tree(self):
        self.tree = ttk.Treeview(self.window, column=("c1", "c2", "c3", "c4"), show='tree headings')

        self.tree.column("#0", anchor=tk.CENTER)
        for i in range(1, 5):
            self.tree.column(f"#{i}", anchor=tk.CENTER)
        
        self.tree.heading("#1", text="date")
        self.tree.heading("#2", text="location")
        self.tree.heading("#3", text="time")
        self.tree.heading("#4", text="spots")

        self.tree.grid(row=2, column=0, sticky="nsew")
        self.tree.bind("<ButtonRelease-1>", self.item_click)
    
    def create_frames(self):
        self.frm_buttons = tk.Frame(self.window, relief=tk.SUNKEN, bd=2)
        self.filter_frame = tk.Frame(self.window, relief=tk.SUNKEN, bd=2)

        self.frm_buttons.grid(row=0, column=0, sticky="ns")
        self.filter_frame.grid(row=1, column=0, sticky="ns")
    
    def create_scrollbar(self):
        scrollBar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        
        self.tree.config(yscrollcommand=scrollBar.set)
        scrollBar.grid(row=2, column=1, sticky="ns")
    
    def create_controls(self):
        self.run_bg_var = tk.IntVar(name="run_bg")
        self.run_telegram_bot = tk.IntVar(name="run_telegram_bot")
        self.one_click_var = tk.IntVar(name="one_click")

        self.load_btn = tk.Button(self.frm_buttons, text="Load data", command=lambda: self.load_data(5)) #self.load_data(n) where n is amount of sections to load
        self.submit_btn = tk.Button(self.frm_buttons, text="submit auto-book", command=self.submit_auto)
        self.run_tray_btn = ttk.Checkbutton(self.frm_buttons, text="minimize to tray", variable=self.run_bg_var)
        self.run_tg_btn = ttk.Checkbutton(self.frm_buttons, text="run telegram bot", variable=self.run_telegram_bot) #tg = telegram
        self.one_click_btn = ttk.Checkbutton(self.frm_buttons, text="one click register", variable=self.one_click_var)

        self.load_btn.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.run_tray_btn.grid(row=0, column=4, sticky="ew", padx=5)
        self.run_tg_btn.grid(row=0, column=0, sticky="ew", padx=5)
        self.one_click_btn.grid(row=0, column=3, sticky="ew", padx=5)
        self.submit_btn.grid(row=0, column=1, sticky="ew", padx=5)
        

    # -- load data --
    def load_data(self, n):
        # print("load_data")
        nextDate = None
        self.locations = set()
        self.times = set()
        self.data = []

        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children()) # * expands into seperate args

        for _ in range(n):
            date = nextDate or datetime.now() - timedelta(days=1)
            section, nextDate = swim_api.get_data(date=date)
            print(f"DATE: {date} | NEXT DATE: {nextDate}")
            self.data += section

            for obj in section: #loop through every location object in section
                #print(obj.location)
                id = self.tree.insert(
                    "",
                    tk.END, 
                    values=(obj.date, obj.location, obj.time, obj.spots, obj.courseId),  #tkinter doesnt support widgets in trees, so i have to use images instead :(
                    image=self.unchecked_img,
                    tags=(obj.id, obj.rawDate),
                    #10 minutes after making thing below, i realized its useless, as i can just set the text when clicking submit. i am keeping this here.
                    text="auto-booked" if obj.date.split(", ")[0] in automation.booked and str(obj.courseId) in ", ".join(str(info["id"]) for info in automation.booked[obj.date.split(", ")[0]]) else "", #auto-booked/blank (atrocious, but im not changing it.) ;)
                )

                self.locations.add(obj.location)
                self.times.add(obj.time)
                self.checkbox_states[id] = False
            self.tree.update()
        
        self.create_filters(self.locations, self.times)

    # --- filters ---
    def create_filters(self, locations, times):
        #destroy/clear current widgets
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
        
        #function for converting time to datetime (ex. 6:30 am - 7:30 am -> 6:30 am datetime)
        def convertTime(time):
            start = time.split(" - ")[0]
            return datetime.strptime(start, "%I:%M %p")
        
        self.filter_location = ttk.Combobox(self.filter_frame, values=sorted(list(locations)), state="readonly", width=50)
        self.filter_time = ttk.Combobox(self.filter_frame, values=sorted(list(times), key=convertTime), state="readonly", width=20)
        self.filter_clear = ttk.Button(self.filter_frame, text="clear filter")

        self.filter_location.grid(row=0, column=0, sticky="ew", padx=5)
        self.filter_time.grid(row=0, column=1, sticky="ew", padx=5)
        self.filter_clear.grid(row=0, column=2, sticky="ew", padx=5)

        self.filter_location.bind(
            "<<ComboboxSelected>>", 
            lambda event: self.filter_click(filter_type="location", item=self.filter_location.get()))
        
        self.filter_time.bind(
            "<<ComboboxSelected>>", 
            lambda event: self.filter_click(filter_type="time", item=self.filter_time.get()))
        
        self.filter_clear.bind(
            "<ButtonRelease-1>" , 
            lambda event: self.filter_click(filter_type="clear", item=None))

    def filter_click(self, filter_type, item):
        time = self.filter_time.get()
        location = self.filter_location.get()
        print(item, time, location)
        
        if filter_type == "location":
            location = item

        elif filter_type == "time":
            time = item

        elif filter_type == "clear":
            location = None
            time = None
            self.filter_time.set("")
            self.filter_location.set("")

        for child in self.tree.get_children(): #clear all locations
            self.tree.delete(child) 
        
        for obj in self.data: #add locations only if filter is empty or same
            if (not location or obj.location == location) and (not time or obj.time == time):
                id = self.tree.insert(
                    "", 
                    tk.END, 
                    values=(obj.date, obj.location, obj.time, obj.spots, obj.courseId),
                    tags=(obj.id, obj.rawDate),
                    image=self.unchecked_img,
                    text="auto-booked" if obj.date.split(", ")[0] in automation.booked and str(obj.courseId) in ", ".join(str(info["id"]) for info in automation.booked[obj.date.split(", ")[0]]) else "",
                )
                
                self.checkbox_states[id] = False
                    

    # --- events ---
    def item_click(self, event):
        id = self.tree.identify_row(event.y) #get clicked row id to handle empty clicking properly
        col_id = self.tree.identify_column(event.x)
        if not id:
            if self.tree.selection():
                self.tree.selection_remove(self.tree.selection()[0]) #deselecting is more complicated for some reason
            return

        self.tree.selection_set(id) #set selection (blue thing) using id of row clicked
        
        print(f"selected item: {self.tree.item(id)["tags"]}")
        item = self.tree.item(id)
        tags = item["tags"]
        values = item["values"]
        
        if col_id == "#0": #if clicked checkbox
            print(f"CLICKED CHECKBOX ID: {self.checkbox_states[id]}, ROW ID: {id}")
            self.checkbox_states[id] = not self.checkbox_states[id]
            
            img = self.checked_img if self.checkbox_states[id] else self.unchecked_img
            self.tree.item(id, image=img)

        else: #if clicked row:
            #if automation box is checked:
            if self.one_click_var.get() and values[3].split()[0].isdigit():
                #automation thing
                url = swim_api.generateButtonUrl(tags[0], tags[1], True)
                automation.register(url=url)
            else: #not one click
                url = swim_api.generateButtonUrl(tags[0], tags[1])
                webbrowser.open_new_tab(url)
    

    #go through self.checkbox_states and send the ones that are true (checked) to automation.py with info
    def submit_auto(self):
        for id, checked in self.checkbox_states.items():
            if checked:
                item = self.tree.item(id)
                tags = item["tags"]
                values = item["values"]

                print(tags[1])
                print(type(values[4]))
                automation.autoBook(str(tags[1]), str(values[4]))
                self.checkbox_states[id] = False
            
                self.tree.item(id, image=self.unchecked_img, text="auto-booked")

    
    
    # --- window ----
    
    def close(self, close_callback=None):
        if self.run_bg_var.get():
            self.window.withdraw()
            image = Image.open("app.ico")
            menu = (pystray.MenuItem("show", self.show_window),
                    pystray.MenuItem("quit", self.quit_window))
            icon = pystray.Icon("icon", image, "swim booker", menu)
            icon.run()
        else:
            self.quit_window(callback=close_callback)
    
    def quit_window(self, icon=None, callback=None):
        if icon:
            icon.stop()
        if callback:
            callback() #external function to run when closing window (terminate telegram bot)
        self.window.destroy()
        sys.exit()
        
    
    def show_window(self, icon):
        icon.stop()
        self.window.deiconify()


    # -- run --
    def run(self):
        self.window.mainloop()
