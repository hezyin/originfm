#!/usr/bin/env python

import os, sys, hashlib

def hashstr(str, nr_bins):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(), 16)%(nr_bins - 1) + 1

usage_string = 'usage: txt2csv.py input output'

if len(sys.argv) != 3:
    print(usage_string)
    exit(1)

src_path, dst_path = sys.argv[1:]

with open(dst_path, 'w') as f:
    for line in open(src_path, 'r'):
        temp_string = ""
        for i, token in enumerate(line.replace('\t', ',').rstrip().split(',')):
            if token == "":
                if i <= 38:
                    temp_string += "x,"
                else:
                    temp_string += "x\n"
                continue
            if i < 14:
                temp_string += (token + ",")
            elif i <= 38: 
                temp_string += str(int(hashstr(token, 1e+6))) + ","
            else:
                temp_string += str(int(hashstr(token, 1e+6))) + "\n"
        f.write(temp_string)
