import tkinter as tk
from tkinter import ttk  # Import ttk for themed widgets
from tabulate import tabulate


onTour = []
# Tout queue already full to make testing easier, same with timeOut queue
tout = ["HEB", "ABC", "EFG", "GHI", "GHF", "IUY", "YRT", "NMB"] 
timeOut = ["YUT"]

def addRTG(code):
    code = code.strip()
    if len(tout) < 8:
        tout.append(code)
    else:
        timeOut.append(code)

def removeRTG(code):
    if code in tout:
        tout.remove(code)
    elif code in timeOut:
        timeOut.remove(code)
    elif code in onTour:
        print("You cannot remove RTG from roster when on tour.")

def sendOnTour(code):
    if code in tout:
        if code == tout[0]:
            onTour.append([code])
            tout.remove(code)
            
        if timeOut:
            tout.append(timeOut[0])
            del timeOut[0]
    else:
        print("code is not valid")

def returnFromTour(code):
    code = code.strip()
    found = False
    
    for i in onTour:
        if i[0] == code:
            onTour.remove(i)
            addRTG(code)
            found = True
            break
    
    if not found:
        print(f"{code} is not on tour")

def displayQueue():
    tout_table = [[num, rtg] for num, rtg in enumerate(tout, start=1)]
    timeOut_table = [[num, rtg] for num, rtg in enumerate(timeOut, start=1)]
    onTour_table = [[num, rtg[0]] for num, rtg in enumerate(onTour, start=1)]
    
    queue_text = f"\nTouting Queue:\n{tabulate(tout_table, headers=['#', 'RTG'])}\n"
    queue_text += f"\nTimeout Queue:\n{tabulate(timeOut_table, headers=['#', 'RTG'])}\n"
    queue_text += f"\nOn Tour:\n{tabulate(onTour_table, headers=['#', 'RTG'])}\n"
    
    queue_label.config(text=queue_text)

def add_rtg_button_clicked():
    rtg_code = add_rtg_entry.get()
    addRTG(rtg_code)
    displayQueue()

def send_on_tour_button_clicked():
    rtg_code = send_on_tour_entry.get()
    sendOnTour(rtg_code)
    displayQueue()

def return_from_tour_button_clicked():
    rtg_code = return_from_tour_entry.get()
    returnFromTour(rtg_code)
    displayQueue()

def remove_rtg_button_clicked():
    rtg_name = remove_rtg_entry.get()
    removeRTG(rtg_name)
    displayQueue()

root = tk.Tk()
root.title("RTG Management System")

# Centered title
title_label = tk.Label(root, text="RTG Management System", font=("TkDefaultFont", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Add RTG section
add_rtg_label = tk.Label(root, text="Add RTG", font=("TkDefaultFont", 16, "bold"))
add_rtg_label.grid(row=1, column=0, columnspan=2)

add_rtg_entry = tk.Entry(root)
add_rtg_entry.grid(row=2, column=0, columnspan=2)

add_rtg_button = tk.Button(root, text="Add RTG", font=("TkDefaultFont", 14), command=add_rtg_button_clicked)
add_rtg_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

# Send on Tour section
send_on_tour_label = tk.Label(root, text="Send RTG on Tour", font=("TkDefaultFont", 16, "bold"))
send_on_tour_label.grid(row=1, column=2, columnspan=2)

send_on_tour_entry = tk.Entry(root)
send_on_tour_entry.grid(row=2, column=2, columnspan=2)

send_on_tour_button = tk.Button(root, text="Send On Tour", font=("TkDefaultFont", 14), command=send_on_tour_button_clicked)
send_on_tour_button.grid(row=3, column=2, columnspan=2, pady=(0, 10))

# Return from Tour section
return_from_tour_label = tk.Label(root, text="Return RTG from Tour", font=("TkDefaultFont", 16, "bold"))
return_from_tour_label.grid(row=4, column=0, columnspan=2)

return_from_tour_entry = tk.Entry(root)
return_from_tour_entry.grid(row=5, column=0, columnspan=2)

return_from_tour_button = tk.Button(root, text="Return From Tour", font=("TkDefaultFont", 14), command=return_from_tour_button_clicked)
return_from_tour_button.grid(row=6, column=0, columnspan=2, pady=(0, 10))

# Remove RTG section
remove_rtg_label = tk.Label(root, text="Remove RTG", font=("TkDefaultFont", 16, "bold"))
remove_rtg_label.grid(row=4, column=2, columnspan=2)

remove_rtg_entry = tk.Entry(root)
remove_rtg_entry.grid(row=5, column=2, columnspan=2)

remove_rtg_button = tk.Button(root, text="Remove RTG", font=("TkDefaultFont", 14), command=remove_rtg_button_clicked)
remove_rtg_button.grid(row=6, column=2, columnspan=2, pady=(0, 10))

# Queue display
queue_label = tk.Label(root, text="")
queue_label.grid(row=7, column=0, columnspan=4)

displayQueue()  # Initial display

root.mainloop()
