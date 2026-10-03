# # Enter your code here. Read input from STDIN. Print output to STDOUT
# itertools.combinations_with_replacement(iterable, r)
# This tool returns  length subsequences of elements from the input iterable allowing individual elements to be repeated more than once.

# Combinations are emitted in lexicographic sorted order. So, if the input iterable is sorted, the combination tuples will be produced in sorted order.

# Sample Code

# >>> from itertools import combinations_with_replacement
# >>> 
# >>> print list(combinations_with_replacement('12345',2))
# [('1', '1'), ('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '2'), ('2', '3'), ('2', '4'), ('2', '5'), ('3', '3'), ('3', '4'), ('3', '5'), ('4', '4'), ('4', '5'), ('5', '5')]
# >>> 
# >>> A = [1,1,3,3,3]
# >>> print list(combinations(A,2))
# [(1, 1), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (3, 3), (3, 3), (3, 3)]
# Task

# You are given a string .
# Your task is to print all possible size  replacement combinations of the string in lexicographic sorted order.

# Input Format

# A single line containing the string  and integer value  separated by a space.

# Constraints


# The string contains only UPPERCASE characters.

# Output Format

# Print the combinations with their replacements of string  on separate lines.

# Sample Input

# HACK 2
# Sample Output

# AA
# AC
# AH
# AK
# CC
# CH
# CK
# HH
# HK
# KK
# Language
# Pypy 3
# More
# 12345678
# # Enter your code here. Read input from STDIN. Print output to STDOUT
# from itertools import combinations_with_replacement
# s,k = input().split()
# k = int(k)
# s = sorted(s)

# for combination in combinations_with_replacement(s,k):
#     print("".join(combination))
# Line: 1 Col: 1

# Test against custom input
# Python
# You have earned 10.00 points!
# You are now 30 points away from the 3rd star for your python badge.
# 25%80/110
# Congratulations
# You solved this challenge. Would you like to challenge your friends?Share on XShare on LinkedIn

# Test case 0

# Test case 1

# Test case 2

# Test case 3

# Test case 4

# Test case 5
# Compiler Message
# Success
# Input (stdin)
# HACK 2
# Expected Output
# AA
# AC
# AH
# AK
# CC
# CH
# CK
# HH
# HK
# KK

from itertools import groupby
from itertools import combinations_with_replacement




# s,k = input().split()
# k = int(k)
# s = sorted(s)

# for combination in combinations_with_replacement(s,k):
#     print("".join(combination))