from List import List
from Node import Node


class SinglyLinkedList(List):
    def __init__(self):
        self.head = None
        self.size = 0
        return

    # Create new node: if self.head is none, create new node
    # Search for the last node
    # Change the next node of the last node to the created node
    def add(self, data):
        #create new node
        node = Node(data, None)

        # List is empty
        if self.head is None:
            self.head = node
            self.size = self.size + 1
            return

        current_node = self.head
        while True:
            if current_node.getNextNode() is None:
    #intput new node
                current_node.changeNextNode(node)
                break
            current_node = current_node.getNextNode()
        self.size = self.size + 1

    def getNode(self, index):
        if self.size <= index:
            raise ValueError("Error: index is over the size")

        node = self.head
        for i in range(0, index):
            node = node.getNextNode()

        return node

    #for commit
    # Insert data to the index
    # Create new node and insert to the middle of the nodes
    def insert(self, index, data):
        new_node2 = Node(data)
        #if index < 0: invalid
        if self.head is None:
            self.head = Node(index, data, None)
        return
        #if head == 0:
        if self.head == 0:
            self.head = new_node2

        #elif self.head == -1
        elif self.head == -1:
            self.head = new_node2

        #if user identify index and number of noe
        previous_node = None
        current_node = self.head
        #elif previous node become new node
        if current_node:
            previous_node = new_node2
        #previous(new_node) become previous node
            new_node2.previous = previous_node
        #inserted node become new_node
            new_node2 = current_node
            current_node = new_node2
        #current_noe become previous node.




    # Search for data in array and remove node
    def remove(self, data):
    #if there is no node that is removed. return
        if self.head is None:
            return #finish method
    #elif: if there is next node, copy next node into current node, then remove next node.
        elif data.getNextNode:
        #copy next node's data into current node
            data.getData() == data.getNextNode()
        #remove next node
            data.getNextNode() == data.changeNextNode()
    #else: if there is no next node.
        else:
            current_node = self.head
        #previous node become NULL
            previous_node = None


    # Return true when size is zero
    # Otherwise false
    def isEmpty(self)-> bool:
        if self.head == None:
            return True

        return False

    # Return current size
    def getSize(self)-> int:
        return self.size

    # Return array that represents the list
    def toArray(self):
        result = []
        node = self.head
        while node is not None:
            result.append(node.getData())
            node = node.getNextNode()
        return result

    # Print inside of array
    # Call toArray inside this function to print it
    # No need to change it
    def print(self):
        print(self.toArray())
        return