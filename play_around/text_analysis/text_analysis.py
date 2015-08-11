import sys, string, re

# command line arguments
file = sys.argv[1]
target = sys.argv[2]
window = int(sys.argv[3])

a = open(file)
text = a.read() 
a.close()

tokens = text.split() # split on whitespace
keyword = re.compile(target, re.IGNORECASE)

for index in range( len(tokens) ):
    if keyword.match( tokens[index] ):
        start = max(0, index-window)
        finish = min(len(tokens), index+window+1)
        lhs = string.join( tokens[start:index] )
        rhs = string.join( tokens[index+1:finish] )
        print "%s [%s] %s" % (lhs, tokens[index], rhs)

