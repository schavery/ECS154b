import random
import Gshare

def generateInput(seed, m,n, probNonBranch,maxBranchAddr=100):
    random.seed(seed)

    #create the instruction stream
    branches = [i for i in range(2**m)]

    #non branch instructions come later but their lower bits mirror the branch instructions
    nonbranches = [i + branches[-1] + 1 for i in range(2**m)]

    #of the instructions that are branches, where do they branch to
    branchAddr = {}
    for pc in branches:
        branchAddr[pc] = random.randint(0,maxBranchAddr)

    insts = []

    #saturate the branch history buffer so it is all ones
    for i in range(m):
        insts.append([branches[0], 1,1,branchAddr[branches[0]]])
        if random.random() <= probNonBranch:
            insts.append([random.choice(nonbranches),0,0,0])

    #now saturate the counters
    for branch in branches:
        for i in range(n+1):
            insts.append([branch,1,1,branchAddr[branch]])
            if random.random() <= probNonBranch:
                insts.append([random.choice(nonbranches),0,0,0])


    #move the branch history buffer back to zero
    for i in range(m):
        insts.append([branches[0], 1,0,branchAddr[branches[0]]])
        if random.random() <= probNonBranch:
            insts.append([random.choice(nonbranches),0,0,0])

    #now oscilate.
    for i in range(2*n + 1):
        insts.append([branches[0], 1,0,branchAddr[branches[0]]])
        insts.append([branches[0], 1,1,branchAddr[branches[0]]])
        if random.random() <= probNonBranch:
            insts.append([random.choice(nonbranches),0,0,0])
                     
    return insts
    
def createImageFiles(insts,g):
    #open files
    PCfile = open('PC.txt','w')
    isBranchFile = open('isbranch.txt','w')
    branchTakenFile = open('branchTaken.txt','w')
    branchAddressFile = open('branchAddress.txt','w')
    
    predsFile = open('preds.txt', 'w')
    predsAddressFile = open('predsAddress.txt', 'w')
    dontCareFile = open('dontCare.txt', 'w')

    #write header
    PCfile.write('v2.0 raw\n')
    isBranchFile.write('v2.0 raw\n')
    branchTakenFile.write('v2.0 raw\n')
    branchAddressFile.write('v2.0 raw\n')

    predsFile.write('v2.0 raw\n')
    predsAddressFile.write('v2.0 raw\n')
    dontCareFile.write('v2.0 raw\n')

    #write data
    for inst in insts:
        pred = g.pred(inst[0])
        
        PCfile.write(hex(inst[0])[2:] + '\n')
        isBranchFile.write(hex(inst[1])[2:] + '\n')
        branchTakenFile.write(hex(inst[2])[2:] + '\n')
        branchAddressFile.write(hex(inst[3])[2:] + '\n')
        
        predsFile.write(hex(pred[0])[2:] + '\n')
        predsAddressFile.write(hex(pred[1])[2:] + '\n')
        if inst[1] == 1:
            g.update(inst[0],inst[2],inst[3])
            dontCareFile.write('0\n')
        else:
            dontCareFile.write('1\n')

    #close files
    PCfile.close()
    isBranchFile.close()
    branchTakenFile.close()
    branchAddressFile.close()
    predsFile.close()
    predsAddressFile.close()
    dontCareFile.close()
    


if __name__ == '__main__':
    
    insts = generateInput(2,2,2,.2,100)
    g = Gshare.Gshare(2,2)
    print 'Number of instructions is', len(insts)
    count = 0
    for inst in insts:
        pred = g.pred(inst[0])
        print count,inst,pred
        if inst[1] == 1:
            g.update(inst[0],inst[2],inst[3])
        count = count + 1

    #g.reset()
    #createImageFiles(insts,g)
