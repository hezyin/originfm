#!/usr/bin/env python 

import os, sys, hashlib

def hashstr(str, nr_bins):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(), 16)%(nr_bins - 1) + 1

def process_tr(src_path, dst_path):
    with open(dst_path, 'w+') as f:
        for line in open(src_path, 'r'):
            temp_string = ""
            for i, token in enumerate(line.rstrip().split(',')):
                if i == 0: 
                    continue
                elif i == 1:
                    temp_string = token + " " + temp_string
                elif 5 <= i and i <= 13:
                    temp_string += (str(i-1) + ":" + str(int(hashstr(token, 1e+6))) + " ") 
                else:
                    temp_string += (str(i-1) + ":" + token + " ")
            f.write(temp_string + "\n")
    f.close()

def process_te(src_path, dst_path):
    with open(dst_path, 'w+') as f:
        for line in open(src_path, 'r'):
            temp_string = "0 "
            for i, token in enumerate(line.rstrip().split(',')):
                if i == 0: 
                    continue
                elif 4 <= i and i <= 12:
                    temp_string += (str(i) + ":" + str(int(hashstr(token, 1e+6))) + " ") 
                else:
                    temp_string += (str(i) + ":" + token + " ")
            f.write(temp_string + "\n")
    f.close()

if __name__ == '__main__':

    usage_string = 'usage: pre-avazu.py {tr|te} input output'

    if len(sys.argv) != 4:
        print(usage_string)
        exit(1)

    dtype, src_path, dst_path = sys.argv[1:] 

    if dtype == "tr":
        process_tr(src_path, dst_path)
    else: 
        process_te(src_path, dst_path)


