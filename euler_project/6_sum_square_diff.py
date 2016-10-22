#!/usr/bin/env python3.4
import sys
print(sys.version)

squared_and_sum=0
sum=0
for i in range(1,101):
  squared_and_sum=i**2+squared_and_sum
  sum=i+sum


square_the_sum=sum*sum
print(square_the_sum - squared_and_sum)

