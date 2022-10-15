from capacityException import CapacityException


class Node:

    def __init__(self,id,capacity):
        self.id = id
        self.capacity=capacity
    
    def checkCapacity(self,required_capacity):

        if(self.capacity<required_capacity):
            self.capacity -= required_capacity
        else:
            raise CapacityException("capacité insuffisante")     

