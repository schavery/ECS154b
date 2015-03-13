class Gshare:
    def __init__(self,m,n):
        self.historyBuffer = 0 #the branch history buffer
        self.counters = [0]*(2**m) #the saturating counters
        self.branchAddresses = [0]*(2**m) #the branch addresses
        self.tags = [0]*(2**m) #the tag registers
        self.mask = 2**m - 1   #a mask to make sure we use only the bottom m bits
        self.half = 2**(n-1)   #1/2 the maximum count
        self.maxCount = 2**n -1 #the maximum value that can be stored in the counters
        self.minCount = 0       #the minimum value that can be stored in the counters
        self.m = m              #m

    def pred(self,PC):
        """
        make a prediction on whether the branch at address PC will be taken
        returns a tuple where the first element is whether to take the branch
        and the second is the branch address
        """
        address = (PC & self.mask) ^ (self.historyBuffer & self.mask)
        return (int(self.counters[address] >= self.half and self.tags[address] == PC), self.branchAddresses[address])

    def update(self,PC,branchTaken,BranchAddress):
        """
        update the branch predictor based on the new branch
        """
        address = (PC & self.mask) ^ (self.historyBuffer & self.mask)
        self.historyBuffer = ((self.historyBuffer << 1) & self.mask) | int(branchTaken)


        
        if(self.tags[address] == PC and int(branchTaken) == 1): #count up branch taken
            self.counters[address] = min(self.maxCount,self.counters[address] + 1)
        elif(self.tags[address] == PC and int(branchTaken) == 0): #count down branch taken
            self.counters[address] = max(self.minCount,self.counters[address] - 1)
        elif(self.tags[address] != PC and int(branchTaken) == 1): #new PC and branch taken set counter to 1 
            self.counters[address] = 1
        else: #new PC and branch not taken, set counter to 0
            self.counters[address] = 0
        #update the branch address
        self.branchAddresses[address] = BranchAddress
        self.tags[address] = PC

    def reset(self):
        """
        reset the predictor by setting it to its original state
        """
        self.historyBuffer = 0
        self.counters = [0]*(2**self.m)
        self.branchAddresses = [0]*(2**self.m)
        self.tags = [0]*(2**self.m)
        

if __name__ == '__main__':
    g = Gshare(5,2)

    for i in range(10):
        print i,g.pred(1),g.historyBuffer
        g.update(1,1,5)
    
    
