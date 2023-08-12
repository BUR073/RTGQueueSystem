import tkinter as tk
from tabulate import tabulate

onTour = []
tout = ["HEB", "ABC", "EFG", "GHI", "GHF", "IUY", "YRT", "NMB"]
timeOut = ["YUT"]

def addRTG(name):
    name = name.strip()
    if len(tout) < 8:
        tout.append(name)
    else:
        timeOut.append(name)

def removeRTG(name):
    if name in tout:
        tout.remove(name)
    elif name in timeOut:
        timeOut.remove(name)
    elif name in onTour:
        print("You cannot remove RTG from roster when on tour.")

def sendOnTour(name):
    if name in tout:
        if name == tout[0]:
            onTour.append([name])
            tout.remove(name)
            
        if timeOut:
            tout.append(timeOut[0])
            del timeOut[0]
    else:
        print("Name is not valid")

def returnFromTour(name):
    name = name.strip()
    found = False
    
    for i in onTour:
        if i[0] == name:
            onTour.remove(i)
            addRTG(name)
            found = True
            break
    
    if not found:
        print(f"{name} is not on tour")

def displayQueue():
    tout_table = [[num, rtg] for num, rtg in enumerate(tout, start=1)]
    timeOut_table = [[num, rtg] for num, rtg in enumerate(timeOut, start=1)]
    onTour_table = [[num, rtg[0]] for num, rtg in enumerate(onTour, start=1)]
    
    queue_text = f"\nTouting Queue:\n{tabulate(tout_table, headers=['#', 'RTG'])}\n"
    queue_text += f"\nTimeout Queue:\n{tabulate(timeOut_table, headers=['#', 'RTG'])}\n"
    queue_text += f"\nOn Tour:\n{tabulate(onTour_table, headers=['#', 'RTG'])}\n"
    
    queue_label.config(text=queue_text)

def add_rtg_button_clicked():
    rtg_name = add_rtg_entry.get()
    addRTG(rtg_name)
    displayQueue()

def send_on_tour_button_clicked():
    rtg_name = send_on_tour_entry.get()
    sendOnTour(rtg_name)
    displayQueue()

def return_from_tour_button_clicked():
    rtg_name = return_from_tour_entry.get()
    returnFromTour(rtg_name)
    displayQueue()

root = tk.Tk()
root.title("RTG Management System")

title_label = tk.Label(root, text="RTG Management System", font=("TkDefaultFont", 18, "bold"))
title_label.pack(pady=10)

# Add empty space
empty_label1 = tk.Label(root, text="", font=("TkDefaultFont", 14))
empty_label1.pack()

add_rtg_label = tk.Label(root, text="Add RTG", font=("TkDefaultFont", 16, "bold"))
add_rtg_label.pack()

add_rtg_entry = tk.Entry(root)
add_rtg_entry.pack()

add_rtg_button = tk.Button(root, text="Add RTG", font=("TkDefaultFont", 14), command=add_rtg_button_clicked)
add_rtg_button.pack()

# Add empty space
empty_label2 = tk.Label(root, text="", font=("TkDefaultFont", 14))
empty_label2.pack()

send_on_tour_label = tk.Label(root, text="Send RTG on Tour", font=("TkDefaultFont", 16, "bold"))
send_on_tour_label.pack()

send_on_tour_entry = tk.Entry(root)
send_on_tour_entry.pack()

send_on_tour_button = tk.Button(root, text="Send On Tour", font=("TkDefaultFont", 14), command=send_on_tour_button_clicked)
send_on_tour_button.pack()

# Add empty space
empty_label3 = tk.Label(root, text="", font=("TkDefaultFont", 14))
empty_label3.pack()

return_from_tour_label = tk.Label(root, text="Return RTG from Tour", font=("TkDefaultFont", 16, "bold"))
return_from_tour_label.pack()

return_from_tour_entry = tk.Entry(root)
return_from_tour_entry.pack()

return_from_tour_button = tk.Button(root, text="Return From Tour", font=("TkDefaultFont", 14), command=return_from_tour_button_clicked)
return_from_tour_button.pack()

# Add empty space
empty_label4 = tk.Label(root, text="", font=("TkDefaultFont", 14))
empty_label4.pack()

queue_label = tk.Label(root, text="")
queue_label.pack()

displayQueue()  # Initial display

root.mainloop()
