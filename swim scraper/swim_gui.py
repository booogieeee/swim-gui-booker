import tkinter as tk
from tkinter import ttk
import swim_api
import webbrowser

#comment from ian

def load_data(tree):
    # print("load_data")

    data = swim_api.get_data()
    if not tree:
        tree = create_tree(tree)
    
    filter_location_list = set()
    filter_time_list = set()

    for obj in data:
        # print(obj.location)
        tree.insert("", tk.END, values=(obj.date, obj.location, obj.time, obj.spots), iid=obj.iid, text=(obj.id, obj.rawDate))
        
        filter_location_list.add(obj.location)
        filter_time_list.add(obj.time)

    filter_location = ttk.Combobox(filter_frame, values=list(filter_location_list), state="readonly", width=50)
    filter_time = ttk.Combobox(filter_frame, values=list(filter_time_list), state="readonly", width=20)
    filter_clear = ttk.Button(filter_frame, text="clear filter")

    filter_location.grid(row=0, column=0, sticky="ew", padx=5)
    filter_time.grid(row=0, column=1, sticky="ew", padx=5)
    filter_clear.grid(row=0, column=2, sticky="ew", padx=5)

    filter_location.bind("<<ComboboxSelected>>", lambda event: filter_click(item=filter_location.get(), type="location", data=data, time_box=filter_time, location_box = filter_location))
    filter_time.bind("<<ComboboxSelected>>", lambda event: filter_click(item=filter_time.get(), type="time", data=data, time_box=filter_time, location_box = filter_location))
    filter_clear.bind("<ButtonRelease-1>" , lambda event: filter_click(item=None, type="clear", data=data, time_box=filter_time, location_box = filter_location))

def filter_click(item, type, data, time_box, location_box):
    time = time_box.get()
    location = location_box.get()
    # print(item, time, location)
    
    if type == "location":
        location = item

    elif type == "time":
        time = item

    elif type == "clear":
        location = None
        time = None
        time_box.set("")
        location_box.set("")

    for child in tree.get_children():
        tree.delete(child)

    if location is None and time is None:
        for obj in data:
            # print(obj.location) 
            tree.insert("", tk.END, values=(obj.date, obj.location, obj.time, obj.spots), iid=obj.iid, text=(obj.id, obj.rawDate))
        return
    else:
        for obj in data:
            if (location == "" or location is None or obj.location == location) and (time == "" or time is None or obj.time == time):
                tree.insert("", tk.END, values=(obj.date, obj.location, obj.time, obj.spots), iid=obj.iid, text=(obj.id, obj.rawDate))
                

def expand(type):
    pass

def item_click(event):
    selected_item = tree.focus()
    # print(tree.item(selected_item))
    if selected_item:
        print(tree.item(selected_item)["text"])
        item = tree.item(selected_item)["text"].split(" ")
        url = swim_api.generateButtonUrl(item[0], item[1])
        webbrowser.open_new_tab(url)

def create_tree(tree):
    if not tree:
        tree = ttk.Treeview(window, column=("c1", "c2", "c3", "c4"), show='headings')
        tree.column("#1", anchor=tk.CENTER)
        tree.heading("#1", text="date")
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text="location")
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text="time")
        tree.column("#4", anchor=tk.CENTER)
        tree.heading("#4", text="spots")
        tree.grid(row=2, column=0, sticky="nsew")
        tree.bind("<ButtonRelease-1>", item_click)
    return tree


window = tk.Tk()
window.title("SWIM booker")

window.rowconfigure(2, minsize=800, weight=1)
window.columnconfigure(0, minsize=800, weight=1)

frm_buttons = tk.Frame(window, relief=tk.SUNKEN, bd=2)
filter_frame = tk.Frame(window, relief=tk.SUNKEN, bd=2)

btn_load = tk.Button(frm_buttons, text="Load data", command= lambda: load_data(tree))

btn_load.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
filter_frame.grid(row=1, column=0, sticky="ns")

# treeStyle = ttk.Style()
# treeStyle.configure("Treeview.Heading")
tree = None #ttk.Treeview(window, column=(""), show='headings')
tree = create_tree(tree)
scrollBar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
tree.config(yscrollcommand=scrollBar.set)
scrollBar.grid(row=2, column=1, sticky="ns")

window.mainloop()