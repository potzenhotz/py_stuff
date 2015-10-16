#!/usr/bin/python

x=False
range=20
range=range+1
k=0
for i in xrange (1,range):
  k=k+i
print k


i=20
while x is False:
  i=i+20
  counter=0
  for j in xrange(1,range):
    if (i % j == 0):
      counter=counter+j
      if (counter == k):
        print i
        x=True 
