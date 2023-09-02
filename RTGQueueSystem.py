import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter
from datetime import datetime

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


# Separate queues for 'Steps' and 'Bridge' RTG stations
queue_data = {
    'Steps': {
        'tout': ["HEB", "FGH", "IOU", "OIU", "BVC", "TRE", "CXZ", "GHF"],
        'timeOut': ["MMM"],
        'onTour': [],
        'history': [],
    },
    'Bridge': {
        'tout': [], 
        'timeOut': [],
        'onTour': [],
        'history': [],
    }
}

selected_station = 'Steps'  # Default selected station


def getTime():
    return str(datetime.now().strftime("%H:%M:%S"))

def updateHistory(name, action):
    queue_data[selected_station]['history'].append(name + action + getTime())
    printHistory()

def printHistory():
    print("History")
    print("")
    for i in queue_data[selected_station]['history']:
        print(i)

def isOnShift(name):
    return name in queue_data[selected_station]['tout'] or name in queue_data[selected_station]['timeOut'] or name in queue_data[selected_station]['onTour']

def alert(message):
    messagebox.showinfo("Alert", message)


def displayQueue():
    queue_tree.delete(*queue_tree.get_children())  # Clear previous data

    for num, i in enumerate(queue_data[selected_station]['tout'], start=1):
        queue_tree.insert("", "end", values=(num, i, "Touting"))

    for num, i in enumerate(queue_data[selected_station]['timeOut'], start=len(queue_data[selected_station]['tout']) + 1):
        queue_tree.insert("", "end", values=(num, i, "Timeout"))

    for num, i in enumerate(queue_data[selected_station]['onTour'], start=len(queue_data[selected_station]['tout']) + len(queue_data[selected_station]['timeOut']) + 1):
        queue_tree.insert("", "end", values=(num, i, "On Tour"))

def add_rtg_button_clicked():
    name = add_rtg_entry.get().strip()
    if name:
        addRTG(name, True)
        add_rtg_entry.delete(0, "end")
        displayQueue()

def send_on_tour_button_clicked():
    name = send_on_tour_entry.get().strip()
    if name:
        sendOnTour(name)
        send_on_tour_entry.delete(0, "end")
        displayQueue()

def return_from_tour_button_clicked():
    name = return_from_tour_entry.get().strip()
    if name:
        returnFromTour(name)
        return_from_tour_entry.delete(0, "end")
        displayQueue()

def remove_rtg_button_clicked():
    name = remove_rtg_entry.get().strip()
    if name:
        removeRTG(name)
        remove_rtg_entry.delete(0, "end")
        displayQueue()

def station_radio_selected():
    global selected_station
    selected_station = station_var.get()
    displayQueue()

def format(name):
    return name.upper().strip()

def addRTG(name, new):
    name = format(name)
    if isOnShift(name):
        alert("RTG is already on shift")
        return
    
    if len(queue_data[selected_station]['tout']) < 8:
        queue_data[selected_station]['tout'].append(name)
    else:
        queue_data[selected_station]['timeOut'].append(name)

    if new:
        updateHistory(name, " clocked in at ")

    


def sendOnTour(name):
    name = format(name)
    if isOnShift(name):
        found = False

        if name in queue_data[selected_station]['tout']:
            queue_data[selected_station]['tout'].remove(name)
            found = True

        elif name in queue_data[selected_station]['timeOut']:
            queue_data[selected_station]['timeOut'].remove(name)
            found = True

        elif name in queue_data[selected_station]['onTour']:
            alert("RTG is already on tour")

        if found:
            queue_data[selected_station]['onTour'].append(str(name))
            updateHistory(name, " went on tour at ")

        if queue_data[selected_station]['timeOut']:
            queue_data[selected_station]['tout'].append(queue_data[selected_station]['timeOut'][0])
            del queue_data[selected_station]['timeOut'][0]
    
    else:
        alert("RTG is not on shift or code is not found")
        return

def returnFromTour(name):
    name = format(name)
    if isOnShift(name):
        if name in queue_data[selected_station]['onTour']:
            queue_data[selected_station]['onTour'].remove(name)
            addRTG(name, False)
            updateHistory(name, " returned from tour at ")
        else:
            alert("RTG is not on tour")
    else:
        alert("RTG is not on shift or code is not found")


def removeRTG(name):
    name = format(name)
    if isOnShift(name):
        if name in queue_data[selected_station]['tout']:
            queue_data[selected_station]['tout'].remove(name)
            updateHistory(name, " clocked out at ")


        elif name in queue_data[selected_station]['timeOut']:
            queue_data[selected_station]['timeOut'].remove(name)
            updateHistory(name, " clocked out at ")

        elif name in queue_data[selected_station]['onTour']:
            alert("RTG is on tour and cannot be removed")
    else:
        alert("RTG is not on shift or code is not found")

    if len(queue_data[selected_station]['timeOut']) != 0 and len(queue_data[selected_station]['tout']) < 8:
        queue_data[selected_station]['tout'].append(queue_data[selected_station]['timeOut'][0])
        del queue_data[selected_station]['timeOut'][0]
    

root = customtkinter.CTk()
root.title("RTG Management System")

# Centered title
title_label = customtkinter.CTkLabel(root, text="RTG Management System", font=("TkDefaultFont", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Create frames for each section
add_rtg_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")
add_rtg_frame.grid(row=1, column=0, columnspan=2, pady=(10, 10))

send_on_tour_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")
send_on_tour_frame.grid(row=1, column=2, columnspan=2, pady=(10, 10))

# Return from Tour section (Position swapped)
return_from_tour_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")
return_from_tour_frame.grid(row=2, column=2, columnspan=2, pady=(10, 10))

remove_rtg_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")
remove_rtg_frame.grid(row=2, column=0, columnspan=2, pady=(10, 10))

# Add RTG section
add_rtg_label = customtkinter.CTkLabel(add_rtg_frame, text="Add RTG", font=("TkDefaultFont", 16, "bold"), fg_color="transparent")
add_rtg_label.pack()

add_rtg_entry = customtkinter.CTkEntry(add_rtg_frame, width=140, height=25, fg_color="transparent")
add_rtg_entry.pack()

add_rtg_button = customtkinter.CTkButton(add_rtg_frame, text="Add RTG", font=("TkDefaultFont", 14), command=add_rtg_button_clicked)

add_rtg_button.pack()

# Send on Tour section
send_on_tour_label = customtkinter.CTkLabel(send_on_tour_frame, text="Send RTG on Tour", font=("TkDefaultFont", 16, "bold"), fg_color="transparent")
send_on_tour_label.pack()

send_on_tour_entry = customtkinter.CTkEntry(send_on_tour_frame, width=140, height=25, fg_color="transparent")
send_on_tour_entry.pack()

send_on_tour_button = customtkinter.CTkButton(send_on_tour_frame, text="Send On Tour", font=("TkDefaultFont", 14), command=send_on_tour_button_clicked)
send_on_tour_button.pack()

# Return from Tour section
return_from_tour_label = customtkinter.CTkLabel(return_from_tour_frame, text="Return RTG from Tour", font=("TkDefaultFont", 16, "bold"), width=140, fg_color="transparent")
return_from_tour_label.pack()

return_from_tour_entry = customtkinter.CTkEntry(return_from_tour_frame, width=140, height=25, fg_color="transparent")
return_from_tour_entry.pack()

return_from_tour_button = customtkinter.CTkButton(return_from_tour_frame, text="Return From Tour", font=("TkDefaultFont", 14), command=return_from_tour_button_clicked)
return_from_tour_button.pack()

# Remove RTG section
remove_rtg_label = customtkinter.CTkLabel(remove_rtg_frame, text="Remove RTG", font=("TkDefaultFont", 16, "bold"), width=140, fg_color="transparent")
remove_rtg_label.pack()

remove_rtg_entry = customtkinter.CTkEntry(remove_rtg_frame, width=140, height=25, fg_color="transparent")
remove_rtg_entry.pack()

remove_rtg_button = customtkinter.CTkButton(remove_rtg_frame, text="Remove RTG", font=("TkDefaultFont", 14), command=remove_rtg_button_clicked)
remove_rtg_button.pack()

# Radio buttons for station selection
station_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")
station_frame.grid(row=3, column=0, columnspan=4, pady=(10, 10))

station_var = tk.StringVar()
steps_radio = customtkinter.CTkRadioButton(station_frame, text="Steps", variable=station_var, value="Steps", command=station_radio_selected, hover=True)
bridge_radio = customtkinter.CTkRadioButton(station_frame, text="Bridge", variable=station_var, value="Bridge", command=station_radio_selected, hover=True)
steps_radio.pack(side="left", padx=10)
bridge_radio.pack(side="left", padx=10)

# Queue display
queue_tree_frame = customtkinter.CTkFrame(master=root)
queue_tree_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 20))

queue_tree = ttk.Treeview(queue_tree_frame, columns=("No.", "Name", "Status"), show="headings", height=10)
queue_tree.heading("No.", text="No.")
queue_tree.heading("Name", text="RTG Code")
queue_tree.heading("Status", text="Status")
queue_tree.pack()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

# Center the main application window
center_window(root, 650, 550)


# Display the initial queues
displayQueue()  # Initial display

root.mainloop()
