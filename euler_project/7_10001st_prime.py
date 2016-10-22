#!/usr/bin/env python3.4

import math
import pdb


def is_prime(number):
    if number>1:
        if number in [2,3,5,7]: 
            return True
        if number % 2 == 0:
            return False
        for divisons_to_test in range(3,int(math.sqrt(number))+1,2):
            if number % divisons_to_test ==  0:
                return False
        return True
    return False


test_dummy=[i for i in range(10)]

def get_primes(start_number):
    while True:
        if is_prime(start_number):
            yield start_number
        start_number += 1


count_primes=0
for next_prime in get_primes(1):
    print(next_prime)
    count_primes += 1
    if count_primes == 10001:
        print("10001 prime is:", next_prime)
        break
