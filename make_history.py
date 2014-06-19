from sh import git
import sys, random, uuid, string, os, shutil

if len(sys.argv) < 2:
    print "You need to supply the number of entries desired"
    sys.exit(0)


currentBranch = "master"
codeDir = './code/'
if not os.path.exists(codeDir):
    os.mkdir(codeDir)
existingFiles = os.listdir(codeDir)

def randomWord(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def randomLine():
    return ' '.join([randomWord(random.randint(6,10)) for ii in range(4,random.randint(5,10)) ])

def commit():
    global currentBranch, existingFiles, codeDir    
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

    print "Commiting all file changes on `"+currentBranch+"`"
    git.add("-A",".")
    ticket = str(random.randint(1000,4000))
    git.commit("-am",'"CFO-'+ticket+' - Helpful message about this commit"')

def checkout(branch):
    try:    
        # Branch already exists
        git.checkout('-b',branch)
    except:
        pass
    git.checkout(branch)

def changeBranch():
    global currentBranch
    target = 'development'
    source = 'master'    
    if "development" is currentBranch:
        target = 'master'
        source = 'development'
        
    print "Checking out "+target
    checkout(target)
    currentBranch = target

def merge(source,target):
    global codeDir
    checkout(source)
    try:
        git.merge(target)
    except:
        print "Conflicts occurred - Blowing away all code and keep going"
        shutil.rmtree(codeDir)
        os.mkdir(codeDir)
        commit()
        

def merge1():
    print "Merging master into development"
    merge('development','master')

def merge2():
    print "Merging development into master"
    merge('master','development')

def switch(x):
    return {
        'commit':commit,
        'changeBranch':changeBranch,
        'merge1':merge1,
        'merge2':merge2
    }.get(x,False)

entriesCount = int(sys.argv[1])
print "Creating "+str(entriesCount) + " git entries"

operations = [(0,80,"commit"),(81,96,"changeBranch"),(97,98,"merge1"),(99,100,"merge2")]
def pickOp():    
    percent = random.randint(0,100)
    for op in operations:    
        if percent >= op[0] and percent <= op[1]:
            return op[2]

while entriesCount > 0:
    entriesCount -= 1
    op = pickOp()
    print "Performing "+op
    switch(op)()