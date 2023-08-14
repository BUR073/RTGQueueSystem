import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

def isOnShift(name):
    return name in queue_data[selected_station]['tout'] or name in queue_data[selected_station]['timeOut'] or name in queue_data[selected_station]['onTour']

def alert(message):
    messagebox.showinfo("Alert", message)


def displayQueue():
    queue_tree.delete(*queue_tree.get_children())  # Clear previous data

    for num, i in enumerate(queue_data[selected_station]['tout'], start=1):
        if num == 1:
            queue_tree.insert("", "end", values=(num, i, "Touting"))
        else:
            queue_tree.insert("", "end", values=(num-1, i, "Touting"))

    for num, i in enumerate(queue_data[selected_station]['timeOut'], start=len(queue_data[selected_station]['tout']) + 1):
        queue_tree.insert("", "end", values=(num, i, "Timeout"))

    for num, i in enumerate(queue_data[selected_station]['onTour'], start=len(queue_data[selected_station]['tout']) + len(queue_data[selected_station]['timeOut']) + 1):
        queue_tree.insert("", "end", values=(num, i, "On Tour"))

def add_rtg_button_clicked():
    name = add_rtg_entry.get().strip()
    if name:
        addRTG(name)
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

def addRTG(name):
    name = format(name)
    if isOnShift(name):
        alert("RTG is already on shift")
        return
    
    if len(queue_data[selected_station]['tout']) < 8:
        queue_data[selected_station]['tout'].append(name)
    else:
        queue_data[selected_station]['timeOut'].append(name)


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

root = tk.Tk()
root.title("RTG Management System")

# Centered title
title_label = tk.Label(root, text="RTG Management System", font=("TkDefaultFont", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Create frames for each section
add_rtg_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
add_rtg_frame.grid(row=1, column=0, columnspan=2, padx=10)

send_on_tour_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
send_on_tour_frame.grid(row=1, column=2, columnspan=2, padx=10)

# Return from Tour section (Position swapped)
return_from_tour_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
return_from_tour_frame.grid(row=2, column=2, columnspan=2, padx=10)

remove_rtg_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
remove_rtg_frame.grid(row=2, column=0, columnspan=2, padx=10)

# Add RTG section
add_rtg_label = tk.Label(add_rtg_frame, text="Add RTG", font=("TkDefaultFont", 16, "bold"))
add_rtg_label.pack()

add_rtg_entry = tk.Entry(add_rtg_frame)
add_rtg_entry.pack()

add_rtg_button = tk.Button(add_rtg_frame, text="Add RTG", font=("TkDefaultFont", 14), command=add_rtg_button_clicked)
add_rtg_button.pack()

# Send on Tour section
send_on_tour_label = tk.Label(send_on_tour_frame, text="Send RTG on Tour", font=("TkDefaultFont", 16, "bold"))
send_on_tour_label.pack()

send_on_tour_entry = tk.Entry(send_on_tour_frame)
send_on_tour_entry.pack()

send_on_tour_button = tk.Button(send_on_tour_frame, text="Send On Tour", font=("TkDefaultFont", 14), command=send_on_tour_button_clicked)
send_on_tour_button.pack()

# Return from Tour section
return_from_tour_label = tk.Label(return_from_tour_frame, text="Return RTG from Tour", font=("TkDefaultFont", 16, "bold"))
return_from_tour_label.pack()

return_from_tour_entry = tk.Entry(return_from_tour_frame)
return_from_tour_entry.pack()

return_from_tour_button = tk.Button(return_from_tour_frame, text="Return From Tour", font=("TkDefaultFont", 14), command=return_from_tour_button_clicked)
return_from_tour_button.pack()

# Remove RTG section
remove_rtg_label = tk.Label(remove_rtg_frame, text="Remove RTG", font=("TkDefaultFont", 16, "bold"))
remove_rtg_label.pack()

remove_rtg_entry = tk.Entry(remove_rtg_frame)
remove_rtg_entry.pack()

remove_rtg_button = tk.Button(remove_rtg_frame, text="Remove RTG", font=("TkDefaultFont", 14), command=remove_rtg_button_clicked)
remove_rtg_button.pack()

# Radio buttons for station selection
station_frame = tk.Frame(root)
station_frame.grid(row=3, column=0, columnspan=4, pady=(0, 10))

station_var = tk.StringVar()
steps_radio = tk.Radiobutton(station_frame, text="Steps", variable=station_var, value="Steps", command=station_radio_selected)
bridge_radio = tk.Radiobutton(station_frame, text="Bridge", variable=station_var, value="Bridge", command=station_radio_selected)
steps_radio.pack(side="left", padx=10)
bridge_radio.pack(side="left", padx=10)

# Queue display
queue_tree_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
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
