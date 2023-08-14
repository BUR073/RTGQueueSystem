import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class RTGManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("RTG Management System")
        self.queue_data = {
            'Steps': {
                'tout': ["HEB", "FGH", "IOU", "OIU", "BVC", "TRE", "CXZ", "GHF"],
                'timeOut': ["MMM"],
                'onTour': []
            },
            'Bridge': {
                'tout': [],
                'timeOut': [],
                'onTour': []
            }
        }
        self.selected_station = 'Steps'

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(self.root, text="RTG Management System", font=("TkDefaultFont", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Create frames for each section
        self.add_rtg_frame = tk.Frame(self.root, bd=2, relief="solid", padx=10, pady=10)
        self.add_rtg_frame.grid(row=1, column=0, columnspan=2, padx=10)

        self.send_on_tour_frame = tk.Frame(self.root, bd=2, relief="solid", padx=10, pady=10)
        self.send_on_tour_frame.grid(row=1, column=2, columnspan=2, padx=10)

        self.return_from_tour_frame = tk.Frame(self.root, bd=2, relief="solid", padx=10, pady=10)
        self.return_from_tour_frame.grid(row=2, column=0, columnspan=2, padx=10)

        self.remove_rtg_frame = tk.Frame(self.root, bd=2, relief="solid", padx=10, pady=10)
        self.remove_rtg_frame.grid(row=2, column=2, columnspan=2, padx=10)

        # Add RTG section
        add_rtg_label = tk.Label(self.add_rtg_frame, text="Add RTG", font=("TkDefaultFont", 16, "bold"))
        add_rtg_label.pack()

        self.add_rtg_entry = tk.Entry(self.add_rtg_frame)
        self.add_rtg_entry.pack()

        add_rtg_button = tk.Button(self.add_rtg_frame, text="Add RTG", font=("TkDefaultFont", 14), command=self.add_rtg_button_clicked)
        add_rtg_button.pack()

        # Send on Tour section
        send_on_tour_label = tk.Label(self.send_on_tour_frame, text="Send RTG on Tour", font=("TkDefaultFont", 16, "bold"))
        send_on_tour_label.pack()

        self.send_on_tour_entry = tk.Entry(self.send_on_tour_frame)
        self.send_on_tour_entry.pack()

        send_on_tour_button = tk.Button(self.send_on_tour_frame, text="Send On Tour", font=("TkDefaultFont", 14), command=self.send_on_tour_button_clicked)
        send_on_tour_button.pack()

        # Return from Tour section
        return_from_tour_label = tk.Label(self.return_from_tour_frame, text="Return RTG from Tour", font=("TkDefaultFont", 16, "bold"))
        return_from_tour_label.pack()

        self.return_from_tour_entry = tk.Entry(self.return_from_tour_frame)
        self.return_from_tour_entry.pack()

        return_from_tour_button = tk.Button(self.return_from_tour_frame, text="Return From Tour", font=("TkDefaultFont", 14), command=self.return_from_tour_button_clicked)
        return_from_tour_button.pack()

        # Remove RTG section
        remove_rtg_label = tk.Label(self.remove_rtg_frame, text="Remove RTG", font=("TkDefaultFont", 16, "bold"))
        remove_rtg_label.pack()

        self.remove_rtg_entry = tk.Entry(self.remove_rtg_frame)
        self.remove_rtg_entry.pack()

        remove_rtg_button = tk.Button(self.remove_rtg_frame, text="Remove RTG", font=("TkDefaultFont", 14), command=self.remove_rtg_button_clicked)
        remove_rtg_button.pack()

        # Radio buttons for station selection
        station_frame = tk.Frame(self.root)
        station_frame.grid(row=3, column=0, columnspan=4, pady=(0, 10))

        self.station_var = tk.StringVar()
        steps_radio = tk.Radiobutton(station_frame, text="Steps", variable=self.station_var, value="Steps", command=self.station_radio_selected)
        bridge_radio = tk.Radiobutton(station_frame, text="Bridge", variable=self.station_var, value="Bridge", command=self.station_radio_selected)
        steps_radio.pack(side="left", padx=10)
        bridge_radio.pack(side="left", padx=10)

        # Queue display
        queue_tree_frame = tk.Frame(self.root, bd=2, relief="solid", padx=10, pady=10)
        queue_tree_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 20))

        self.queue_tree = ttk.Treeview(queue_tree_frame, columns=("No.", "Name", "Status"), show="headings", height=10)
        self.queue_tree.heading("No.", text="No.")
        self.queue_tree.heading("Name", text="RTG Code")
        self.queue_tree.heading("Status", text="Status")
        self.queue_tree.pack()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def display_queue(self):
        self.queue_tree.delete(*self.queue_tree.get_children())  # Clear previous data

        for num, i in enumerate(self.queue_data[self.selected_station]['tout'], start=1):
            if num == 1:
                self.queue_tree.insert("", "end", values=("Next on tour", i, "Touting"))
            else:
                self.queue_tree.insert("", "end", values=(num - 1, i, "Touting"))

        for num, i in enumerate(self.queue_data[self.selected_station]['timeOut'], start=len(self.queue_data[self.selected_station]['tout']) + 1):
            self.queue_tree.insert("", "end", values=(num, i, "Timeout"))

        for num, i in enumerate(self.queue_data[self.selected_station]['onTour'], start=len(self.queue_data[self.selected_station]['tout']) + len(self.queue_data[self.selected_station]['timeOut']) + 1):
            self.queue_tree.insert("", "end", values=(num, i, "On Tour"))

    def add_rtg_button_clicked(self):
        name = self.add_rtg_entry.get().strip()
        if name:
            self.addRTG(name)
            self.add_rtg_entry.delete(0, "end")
            self.display_queue()

    def send_on_tour_button_clicked(self):
        name = self.send_on_tour_entry.get().strip()
        if name:
            self.sendOnTour(name)
            self.send_on_tour_entry.delete(0, "end")
            self.display_queue()

    def return_from_tour_button_clicked(self):
        name = self.return_from_tour_entry.get().strip()
        if name:
            self.returnFromTour(name)
            self.return_from_tour_entry.delete(0, "end")
            self.display_queue()

    def remove_rtg_button_clicked(self):
        name = self.remove_rtg_entry.get().strip()
        if name:
            self.removeRTG(name)
            self.remove_rtg_entry.delete(0, "end")
            self.display_queue()

    def station_radio_selected(self):
        self.selected_station = self.station_var.get()
        self.display_queue()

    def addRTG(self, name):
        if len(self.queue_data[self.selected_station]['tout']) < 8:
            self.queue_data[self.selected_station]['tout'].append(name)
        else:
            self.queue_data[self.selected_station]['timeOut'].append(name)

    def sendOnTour(self, name):
        found = False

        if name in self.queue_data[self.selected_station]['tout']:
            self.queue_data[self.selected_station]['tout'].remove(name)
            found = True

        elif name in self.queue_data[self.selected_station]['timeOut']:
            self.queue_data[self.selected_station]['timeOut'].remove(name)
            found = True

        elif name in self.queue_data[self.selected_station]['onTour']:
            self.alert("RTG is already on tour")
        else:
            self.alert("RTG not found")

        if found:
            self.queue_data[self.selected_station]['onTour'].append(str(name))

        if self.queue_data[self.selected_station]['timeOut']:
            self.queue_data[self.selected_station]['tout'].append(self.queue_data[self.selected_station]['timeOut'][0])
            del self.queue_data[self.selected_station]['timeOut'][0]

    def returnFromTour(self, name):
        if name in self.queue_data[self.selected_station]['onTour']:
            self.queue_data[self.selected_station]['onTour'].remove(name)
            self.addRTG(name)
        else:
            self.alert("RTG is not on tour")

    def removeRTG(self, name):
        for key in self.queue_data[self.selected_station]:
            if name in self.queue_data[self.selected_station][key]:
                self.queue_data[self.selected_station][key].remove(name)
                self.alert(name + " has been removed")
                break

    def alert(self, message):
        messagebox.showinfo("Alert", message)

    def run(self):
        self.display_queue()  # Initial display
        self.center_window(650, 550)
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RTGManagementSystem(root)
    app.run()
