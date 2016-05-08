import sys
file = sys.argv[1]

clean = open(file).read().replace('\n\n', '\n')

print clean
