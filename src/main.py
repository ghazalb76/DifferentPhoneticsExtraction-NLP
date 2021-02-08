import csv
from anytree import Node, RenderTree, PreOrderIter


# A class for every word of the sentence that is in dictionary to save some information about it as below
class node():
    def __init__(self, name, parent, index):
        self.name = name
        self.parent = parent
        self.index = index
        self.children = []
        self.v = None


################################       Read needed files    ############################################
# Read input
f=open("../in/in_2.txt", encoding="utf8")
if f.mode == 'r':
    contents =f.read()
contents = contents.split()

# Read dictionary
with open("../in/Entries.csv", encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    data = []
    for row in reader:
        data.append(row)
    phonetics = []
    # Find phonetics of persian words from dictionary and save them in phonetics list
    for word in contents:
        for dWord in data:
            if word == dWord[1]:
                phonetics.append(dWord[0])
                break

########################################################################################################
#######################################   Find words ###################################################

# Stick all the phonetics together
sentence = ''
for word in phonetics:
    sentence+=word
print(sentence)

# Find first words that have meaning based on given dictionary
liste = []
for i in range(0, len(sentence)+1):
    sub = sentence[0:i]
    if len(sub) != 1 and any(sub in subl for subl in data) and sub is not '':
        liste.append(sub)

# Make tree for first words
root = node('root', None, -1)
word_obj = []
root.v = Node('root')
for r in liste:
    word = node(r, root, 0)
    word_obj.append(word)
    word.v = Node(r,root.v)


# Find all the children of all the nodes, make object for them and set them as the child of node
for word in word_obj:
    l = word.index+len(word.name)
    for i in range(l,len(sentence)+1):
        sub = sentence[l:i]
        if len(sub) != 1 and any(sub in subl for subl in data) and sub is not '':
            w = node(sub, word, l)
            word.children.append(w)
            word_obj.append(w)

# Make tree depend on parent and child relations
for word in word_obj:
    for child in word.children:
        child.v = Node(child.name, word.v)


# Print final tree
for pre, fill, node in RenderTree(root.v):
    print("%s%s" % (pre, node.name))
########################################################################################################
#######################################    Write part   ################################################

# Find all the pathes of the tree which their end word is equal to the end of the sentence, change their phonetics to persian and show them
post = [node.name for node in PreOrderIter(root.v)]
for k in post:
    if sentence.find(k)+len(k) == len(sentence):
        r = k
        break

final_list = []
f=open("../out/out_2.txt", 'w', encoding="utf8")
flag = False
for pre, fill, node in RenderTree(root.v):
    my_list = []
    if(node.name == r):
        node_p = node
        while(node_p.name != 'root'):
            my_list.append(node_p.name)
            node_p = node_p.parent
        my_list.reverse()
        print(my_list)
        de_phonetics = []
        count = 0
        for word in my_list:
            for dWord in data:
                if word == dWord[0]:
                    de_phonetics.append(dWord[1])
                    count +=1
                    break
  
        if count >= len(my_list):
            print(de_phonetics)
            for persia in de_phonetics:
                stri = ''
                stri += '['+persia+']'
                f.write(stri)
        
            f.write('\n')
