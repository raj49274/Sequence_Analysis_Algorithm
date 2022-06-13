# Project : Sequence Analysis Algorithm
# 
# Authors: Aditya Raj (AU1920177)
#        : Sanya Zaveri (AU1920064)
# 



#------------------- Imports ----------------
import argparse


#------------------global variables -------------
prefixes = {}
suffixes = []
no_of_reads = 0
read_size = 0


# ---------- Helper Functions ------------------------
# Encoding of the ACTG
def encode(character):
    x = {
         "A": 1,
         "C": 2,
         "T": 3,
         "G": 4
    }
    return x[character]

# Calculating the reverse complement
def reverseComplement(read):
    # Reversing the string
    itr = reversed(read)
    res = ""
    # Now complementing the read
    for i in range(len(read)):
        code = next(itr)
        if(code == 'A'):
            res = res + 'T'
        elif(code == 'C'):
            res = res + 'G'
        elif(code == 'G'):
            res = res + 'C'
        elif(code == 'T'):
            res = res + 'A'
    return res

# Calculating the value of the number
def calculateValue(x):
    res = 0
    i = 0
    while(x > 0):
        y = x%10
        x = x//10
        res = y*(5**i) + res
        i += 1
    return res

# getting read size
def getReadSize(file_name):
    global read_size
    with open(file_name, "r") as file: 
        data = file.readline()
        read_size = len(data)
            


# ------------ Function to create prefix and storing in a data structure --------

# Now adding an element to the fingerepring at the right (Prefixes)
def consume_char_at_right(f, c):
    c_int = encode(c)
    return (f*5 + c_int)%prime


# Creating suffixes from strart length
def createPrefix(read, readId, minLength, prefix_index):
    # calculating starting fingerprint
    fingerprint = 0
    for i in range(minLength):
        fingerprint = fingerprint*10 + encode(read[i])
    
    fingerprint = calculateValue(fingerprint)%prime
    
    # adding first suffix in the inverted index
    prefix_index[(fingerprint, minLength)] = [readId]
    
    # starting consuming characters
    for i in range(minLength, len(read) - 1, 1):
        fingerprint = consume_char_at_right(fingerprint, read[i])
        # checking and adding the fingerprint
        if (fingerprint, i+1) in prefix_index:
            prefix_index[(fingerprint, i+1)].append(readId)
        else:
            prefix_index[(fingerprint, i+1)] = [readId]
    
    return 0




# ------------ Function to create suffix and storing in a data structure --------

# Assuming the function takes f, n is suffix length and c as character
def consume_char_from_left(f, n, c):
    c_int = encode(c)
    return (f + c_int*(5**(n-1)))%prime

# Crating suffix from minLength of suffix
def createSuffix(read, readId, minLength, suffix_index):
    # calculating starting fingerprint
    fingerprint = 0
    readLength = len(read)
    startIndex = readLength - minLength
    suffixLength = minLength
    
    for i in range(startIndex, readLength, 1):
        fingerprint = fingerprint*10 + encode(read[i])
    
    fingerprint = calculateValue(fingerprint)%prime
    
    # adding first suffix in the inverted index
    suffix_index.append((suffixLength, fingerprint, readId))
    
    # starting consuming characters
    for i in range(startIndex, 0, -1):
        suffixLength = suffixLength + 1
        startIndex = startIndex - 1;
        fingerprint = consume_char_from_left(fingerprint, suffixLength, read[startIndex])
        # checking and adding fingerprint
        suffix_index.append((suffixLength, fingerprint, readId))
        
    return 0

#-----------Creating Fingerprint-----------------
def createFingerprint(file_name, minLength):
    global no_of_reads
    prefix_index = {}
    suffix_index = []
    # opening the file and reading the line by line
    with open(file_name, "r") as file: 
        data = file.readlines()
        i = 0
        j = 0
        for line in data:
            if j == 0:
                j = 1
                continue
            else:
                j = 0
                
            no_of_reads = no_of_reads + 1
            if no_of_reads == 20000:
                break
            
            word = line.split()[0]
            
            # Now calculating prefix and suffix
            readId = 2*i
            cReadId = 2*i + 1
            rcText = reverseComplement(word)
            
            createPrefix(word, readId, minLength, prefix_index)
            createPrefix(rcText, cReadId, minLength, prefix_index)
            createSuffix(word, readId, minLength, suffix_index)
            createSuffix(rcText, cReadId, minLength, suffix_index)
            i = i + 1
    return prefix_index, suffix_index




# ----------- Creating graph ------------------

def createGraph(pfix, sfix, r):
    graph = []
    
    # Assigning None to every element in the graph
    for i in range(r):
        graph.append(None)
        
    sfix.sort(reverse= True)
    
    for i in sfix:
        if graph[i[2]] != None and graph[i[2]][0][1] > i[0] and i[0] < 85:
            continue
        else:
            lp = pfix.get((i[1], i[0]))
            if lp != None:
                if graph[i[2]] == None:
                    graph[i[2]] = []
                for j in lp:
                    graph[i[2]].append((j, i[0]))
                    
    with open("graph.gfa", "w") as file:
        for i in range(r):
            if graph[i] != None:
                file.write(f"S\t{i+1}\t*\tLN:i:{read_size}\n")
                for k in graph[i]:
                    file.write(f"L\t{i+1}\t+\t{k[0]}\t+\t{k[1]}M\n")
        
        
    print(graph)
    return 0


# -------- Driver Function -----------
def main():
    global prefixes, suffixes
    minLength = args.minLength
    file_name = args.fileName
    
    getReadSize(file_name)
    
    prefixes, suffixes  = createFingerprint(file_name, minLength)
    
    createGraph(prefixes, suffixes, no_of_reads*2)
    return 0


# -------------- Running the file ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="taking inputs: prime, text, pattern")
    
    # Adding Arguments and parsing it
    parser.add_argument('-f', '--fileName', default="reads.fasta", type=str)
    parser.add_argument('-p', '--prime', default=1073741789, type=int)
    parser.add_argument('-l', '--minLength', default=5, type=int)
    args = parser.parse_args()
    
    prime =  args.prime
    

    main()