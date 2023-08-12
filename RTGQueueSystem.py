onTour = []
tout = ["HEB", "ABC", "EFG", "GHI", "GHF", "IUY", "YRT", "NMB"]
timeOut = ["YUT"]

def addRTG(name):
  if len(tout) < 8:
    # Assuming number of touts allowed is 8 or les
    # If there are 8 or more touts, new RTG will be put on timeout
    tout.append(name)
  else:
    timeOut.append(name)

def removeRTG(name):
  if name in tout:
    # Check if name is in tout list
    tout.remove(name)
  elif name in timeOut:
    # Check if name is in time out list
    timeOut.remove(name)
  elif name in onTour:
    # Else name must be in onTour list, you cannot remove someone from
    # the roster while on tour
    print("You cannot remove RTG from roster when on tour.")

def sendOnTour(name):
  if name in tout:
    if name == tout[0]:
      onTour.append([name])
      # Add guid to onTour list
    else:
      # If the RTG going on tour is not the next person to go on tour
      # then find out who they are behind and add it too a list
      # along with the name of the RTG and add it to the onTour list
      onTour.append([name, tout.index(name) + 1])
      tout.remove(name)
      # Remove guide from tout list
      
    if timeOut:
      # If there are people in time out
      tout.append(timeOut[0])
      # Add the next person to the tout queue
      del timeOut[0]
      # And remove them from timeOut
  else:
    print("Name is not valid")

def formatLists():
  if len(tout) > 8:
    diff = len(tout) - 8
    for i in range(7, 7 + diff):
      timeOut.insert(0, tout[i])
      del tout[i]
      
      
def returnFromTour(name):
  if [name] in onTour:
    onTour.remove(name)
    addRTG(name)
  else:
    while True:
      for i in tout:
        if i[0] == name and i[1] in tout:
          tout.insert(int(tout.index(i[1]) + 1), name)
          formatLists()
          break
      for i in timeOut:
          if i[0] == name and i[1] in timeOut:
            timeOut.insert(int(timeOut.index(i[1]) + 1), name)
            formatLists()
            break
        
                    
  # else:
  #   print("RTG is not on tour")
    
def displayQueue():
  print("")
  print("----------------------")
  
  print("Touting")
  print("")
  for num, i in enumerate(tout):
    print(num+1, ":", i)
  print("----------------------")
  
  print("Timeout")
  print("")
  for num, i in enumerate(timeOut):
    print(num+1, ":", i)
  print("----------------------") 
  
  print("On tour")
  print("")
  for num, i in enumerate(onTour):
    print(num+1, ":", i[0])
  print("----------------------")
  
def main():
  while True:
    print("1. Add RTG")
    print("2. Remove RTG")
    print("3. Send RTG on tour")
    print("4. RTG return from tour")
    print("5. Display queue")
    print("6. Exit")
    x = int(input("Input: "))
    print("")
    if x == 6:
      break
    elif x == 1:
      addRTG(input("RTG name: "))
    elif x == 2:
      removeRTG(input("RTG name: "))
    elif x == 3:
      sendOnTour(input("RTG name: "))
    elif x == 4:
      returnFromTour(input("RTG name: "))
    elif x == 5:
      displayQueue()
    elif x == 6:
      break
      
main()
    
  
