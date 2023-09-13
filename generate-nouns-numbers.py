#!/usr/bin/env python3

nouns = "top_english_nouns_lower_10000.txt"
wordlist = "nouns-numbers.txt"

# open files for reads and writes
n_file = open(nouns,"r")
w_file = open(wordlist,"w")

# read noun list into memory
n_list = []
for n in n_file:
    n_list.append(n.strip())
n_file.close()

for n in n_list:
    for i in range(0,1000):
        i = str(i)
        i = ("0" * (3 - len(i))) + i # pad number with leading zeros as needed
        w_file.write(n + i + "\n") # write guess to wordlist
w_file.close()

