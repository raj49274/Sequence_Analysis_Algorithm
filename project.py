# Project : Sequence Analysis Algorithm
# 
# 



#------------------- Imports ----------------
import argparse


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
    for i in range(minLength, len(read), 1):
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
    return f + (c_int*(5**n))%prime

# Crating suffix from minLength of suffix
def createSuffix(read, readId, minLength, suffix_index):
    # calculating starting fingerprint
    fingerprint = 0
    readLength = len(read)
    startIndex = readLength - minLength - 1
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
    prefix_index = {}
    suffix_index = []
    # opening the file and reading the line by line
    with open(file_name, "r") as file: 
        data = file.readlines()
        i = 0
        for line in data:
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

def createGraph(r):
    graph = []
    
    # Assigning None to every element in the graph
    for i in range(r):
        graph[i] = None
    
    
    return 0


# -------- Driver Function -----------
def main():
    
    prefixes = {}
    suffixes = [] 
    minLength = args.minLength
    file_name = args.fileName
    
    prefixes, suffixes  = createFingerprint(file_name, minLength)
    
    
    print(prefixes)
    print(suffixes)
    return 0






# -------------- Running the file ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="taking inputs: prime, text, pattern")
    
    # Adding Arguments and parsing it
    parser.add_argument('-f', '--fileName', default="input.txt", type=str)
    parser.add_argument('-p', '--prime', default=1073741789, type=int)
    parser.add_argument('-l', '--minLength', default= 5, type=int)
    args = parser.parse_args()
    
    prime =  args.prime
    main()