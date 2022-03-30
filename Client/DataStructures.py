#Simple priority queue data structure
#Needs to be priority as certain inputs need to be dealt with immediately 
#Used in InputHandler object
class PriorityQueue:
    def __init__(self):
        #List where the data is stored [priority, item]
        #Private as it shouldn't be accessed outside of the queue
        self.__queue = []

    #Adds item to the correct point in the queue
    def Enqueue(self, priority, itemToAdd):
        #If list is empty appends it to the start of the list
        if self.__queue == []:
            self.__queue.append([priority, itemToAdd])
            return 0

        #items in self.__queue are lists [priority, actual item]
        for i in range(len(self.__queue)):
            #Goes through each item in the list
            #Checks if the priority is lower than the priority of the new item
            if priority > self.__queue[i][0]:
                #Splits string where item needs to go
                startOfQueue = self.__queue[:i]
                endOfQueue = self.__queue[i:]
                #Joins the lists together
                self.__queue = startOfQueue + [[priority, itemToAdd]] + endOfQueue
                break
    
            elif i == len(self.__queue) - 1:
                self.__queue.append([priority, itemToAdd])

    #Removes item from the start of the queue
    def Dequeue(self):
        if self.__queue != []:
            return self.__queue.pop(0)
        else:
            return []

    def GetLength(self):
        return len(self.__queue)

# thingsToAddToQueue = []
# queue = PriorityQueue()

# for thing in thingsToAddToQueue:
#     queue.Enqueue(thing[1], thing[0])

# thingRemoved = queue.Dequeue()
# while thingRemoved != []:
#     print(f"Priority: {thingRemoved[0]}\n Item: {thingRemoved[1]}\n")
#     thingRemoved = queue.Dequeue()