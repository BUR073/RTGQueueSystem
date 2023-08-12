# List to store RTGs currently on tour
onTour = []

# Lists to manage RTGs in different states
tout = ["HEB", "ABC", "EFG", "GHI", "GHF", "IUY", "YRT", "NMB"]  # RTGs available for tour
timeOut = ["YUT"]  # RTGs in timeout

# Function to add an RTG to appropriate list
def addRTG(name):
    name = name.strip()  # Remove whitespace
    if len(tout) < 8:
        # Add RTG to tout if there are less than 8 RTGs on tour
        tout.append(name)
    else:
        # Add RTG to timeout if tout is full
        timeOut.append(name)

# Function to remove an RTG from appropriate list
def removeRTG(name):
    if name in tout:
        tout.remove(name)  # Remove from tout list
    elif name in timeOut:
        timeOut.remove(name)  # Remove from timeout list
    elif name in onTour:
        print("You cannot remove RTG from roster when on tour.")  # Cannot remove while on tour

# Function to send an RTG on tour
def sendOnTour(name):
    if name in tout:
        if name == tout[0]:
            onTour.append([name])  # Add RTG to onTour list
            tout.remove(name)  # Remove from tout list
            
        if timeOut:
            tout.append(timeOut[0])  # Add next person from timeout to tout queue
            del timeOut[0]  # Remove from timeout
    else:
        print("Name is not valid")

# Function to return an RTG from tour
def returnFromTour(name):
    name = name.strip()  # Trim whitespace
    found = False  # Initialize a flag to track if the name is found
    
    # Iterate through onTour list to find the RTG
    for i in onTour:
        if i[0] == name:
            onTour.remove(i)  # Remove from onTour list
            addRTG(name)  # Add back using addRTG function
            found = True
            break  # Exit loop once found
    
    if not found:
        print(f"{name} is not on tour")

# Function to display the current state of RTGs
from tabulate import tabulate

def displayQueue():
    tout_table = [[num, rtg] for num, rtg in enumerate(tout, start=1)]
    timeOut_table = [[num, rtg] for num, rtg in enumerate(timeOut, start=1)]
    onTour_table = [[num, rtg[0]] for num, rtg in enumerate(onTour, start=1)]
    
    print("\nTouting Queue")
    print(tabulate(tout_table, headers=["#", "RTG"]))
    
    print("\nTimeout Queue")
    print(tabulate(timeOut_table, headers=["#", "RTG"]))
    
    print("\nOn Tour")
    print(tabulate(onTour_table, headers=["#", "RTG"]))
    print("----------------------\n")



# Main program loop
def main():
    while True:
        print("1. Add RTG")
        print("2. Remove RTG")
        print("3. Send RTG on tour")
        print("4. RTG return from tour")
        print("5. Display queue")
        print("6. Exit")
        x = int(input("Input: "))  # Get user choice
        print("")
        
        # Execute the chosen action
        if x == 6:
            break
        elif x == 1:
            addRTG(input("RTG name: "))  # Add RTG
        elif x == 2:
            removeRTG(input("RTG name: "))  # Remove RTG
        elif x == 3:
            sendOnTour(input("RTG name: "))  # Send RTG on tour
        elif x == 4:
            returnFromTour(input("RTG name: "))  # Return RTG from tour
        elif x == 5:
            displayQueue()  # Display the queue
        elif x == 6:
            break
      
main()  # Start the main program loop
    
  
