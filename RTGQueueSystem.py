import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# Separate queues for 'Steps' and 'Bridge' RTG stations
queue_data = {
    'Steps': {
        'tout': ["HEB", "FGH", "IOU", "OIU", "BVC", "TRE", "CXZ", "GHF"],
        'timeOut': ["MMM"],
        'onTour': [],
    },
    'Bridge': {
        'tout': [], 
        'timeOut': [],
        'onTour': [],
    }
}

selected_station = 'Steps'  # Default selected station

def isOnShift(name): # Check if name is alreay in tout, timeOut or onTour
    return name in queue_data[selected_station]['tout'] or name in queue_data[selected_station]['timeOut'] or name in queue_data[selected_station]['onTour']

def alert(message): # Create alert box containing message
    messagebox.showinfo("Alert", message)


def displayQueue():
    queue_tree.delete(*queue_tree.get_children())  # Clear previous data

    for num, i in enumerate(queue_data[selected_station]['tout'], start=1): # Loop through tout list of selected station
        if num == 1: # If num equals 1 print next on tour rather than 1
            queue_tree.insert("", "end", values=("Next on tour", i, "Touting"))
        else: # Else just print the number
            queue_tree.insert("", "end", values=(num-1, i, "Touting"))

    for num, i in enumerate(queue_data[selected_station]['timeOut'], start=8): 
        queue_tree.insert("", "end", values=(num, i, "Timeout"))
        # Loop through timeOut and print out data and position in queue starting from 8

    for num, i in enumerate(queue_data[selected_station]['onTour'], start=len(queue_data[selected_station]['timeOut']) + 9):
        queue_tree.insert("", "end", values=(num, i, "On Tour"))
        # Same as above but with onTour and 9

def add_rtg_button_clicked():
    name = add_rtg_entry.get().strip() # Get input from add_rtg_entry and strip whitespace
    if name: # If name contains a value
        addRTG(name) # Call fucntion addRTG and pass in name
        add_rtg_entry.delete(0, "end") # Clear the input for add_rtg_entry
        displayQueue() # Call function displayQueue

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
    global selected_station # Create global value selected_station
    selected_station = station_var.get() # Get value from station_var radio button
    displayQueue() # Call function displayQueue

def format(name):
    return name.upper() # Return input in uppercase

def addRTG(name):
    name = format(name) 
    if isOnShift(name): # If isOnShift() returns True
        alert("RTG is already on shift")
        return
    
    if len(queue_data[selected_station]['tout']) < 8: # If there are less than 8 RTGs touting
        queue_data[selected_station]['tout'].append(name) # Append name to tout on the selected station
    else:
        queue_data[selected_station]['timeOut'].append(name) # Append name to timeOut


def sendOnTour(name):
    name = format(name)
    if isOnShift(name):
        found = False

        # Find name in lists, when found set found to True and remove name 
        # Unless is found in onTour, then alert as RTG cannot be removed
        # when on tour

        if name in queue_data[selected_station]['tout']:
            queue_data[selected_station]['tout'].remove(name)
            found = True

        elif name in queue_data[selected_station]['timeOut']:
            queue_data[selected_station]['timeOut'].remove(name)
            found = True

        elif name in queue_data[selected_station]['onTour']:
            alert("RTG is already on tour")

        if found:
            queue_data[selected_station]['onTour'].append(name) # Add name to onTour if found in lists

        if queue_data[selected_station]['timeOut']: # If there are RTGs on timeOut
            # Append the first name in timeOut to tout and remove them from timeOut
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
            addRTG(name)
        else:
            alert("RTG is not on tour")
    else:
        alert("RTG is not on shift or code is not found")

def removeRTG(name):
    name = format(name)
    if isOnShift(name):
        if name in queue_data[selected_station]['tout']:
            queue_data[selected_station]['tout'].remove(name)

        elif name in queue_data[selected_station]['timeOut']:
            queue_data[selected_station]['timeOut'].remove(name)

        elif name in queue_data[selected_station]['onTour']:
            alert("RTG is on tour and cannot be removed")
    else:
        alert("RTG is not on shift or code is not found")

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
queue_tree_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=(10, 10))

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
center_window(root, 622, 510)


# Display the initial queues
displayQueue()  # Initial display

root.mainloop()
