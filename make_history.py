from sh import git
import sys, random, uuid, string, os, shutil

if len(sys.argv) < 2:
    print "You need to supply the number of entries desired"
    sys.exit(0)


codeDir = './code/'
existingFiles = []

def makeCodeDir():
    global codeDir,existingFiles
    if not os.path.exists(codeDir):
        os.mkdir(codeDir)
    existingFiles = os.listdir(codeDir)

def randomWord(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def randomLine():
    return ' '.join([randomWord(random.randint(6,10)) for ii in range(4,random.randint(5,10)) ])

# Checks out the proper source branch
# Checks out a feature branch from the source
# Makes random commits against the branch
def commit(sourceBranch):
    global existingFiles, codeDir    

    branchPrefix = 'dev'
    if sourceBranch is 'master':
        branchPrefix = 'stable'
    checkout(sourceBranch)
    ticket = str(random.randint(1000,4000))    
    featureBranch=branchPrefix+"/cfo-"+ticket+"-"+str(uuid.uuid4())
    checkout(featureBranch)
    makeCodeDir()

    fileChanges = random.randint(1,5)    
    print "Making "+str(fileChanges)+" file changes in the code directory"
    while fileChanges > 0:
        fileChanges -= 1
        out = str(uuid.uuid4())+".js"
        if random.randint(1,2) is 1 and len(existingFiles)>0:
            out = random.choice(existingFiles)
        else:
            existingFiles.append(out)
        
        out = os.path.join(codeDir,out)

        f = open(out,'a')
        newLines = random.randint(10,50)
        while newLines > 0:
            newLines -= 1
            line = randomLine()+'\n'
            f.write(line)
        f.close()


    print "Commiting all file changes on `"+featureBranch+"`"
    git.add("-A",".")
    
    git.commit("-am",'"CFO-'+ticket+' - Helpful message about this commit"')
    checkout(sourceBranch)

def checkout(branch):
    print "Checking out "+branch
    try:    
        # Branch already exists
        git.checkout('-b',branch)
    except:
        pass
    git.checkout(branch)

def changeSourceBranch(sourceBranch):
    target = 'development'
    if "development" is sourceBranch:
        target = 'master'        
    return target


gitOperationCount = int(sys.argv[1])
print "Creating "+str(gitOperationCount) + " git entries"

sourceBranch = "master"
while gitOperationCount > 0:
    gitOperationCount -= 1
    if random.randint(0,1) == 1:
        sourceBranch = changeSourceBranch(sourceBranch)
    commit(sourceBranch)