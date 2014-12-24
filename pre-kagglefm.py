#!/usr/bin/env python
# this script is used to transform train.txt to train.kagglefm

import os
import argparse
import hashlib

def hashstr(str, nr_bins):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(), 16)%(nr_bins - 1) + 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Preprocess Dataset for my FM')
    parser.add_argument('dataset', help='path to data file')
    parser.add_argument('output', help='ouput path')
    parser.add_argument('-t', '--target', default=0, help='specify y column')

    args = vars(parser.parse_args())
    outf = open(args['output'], "w+")
    target = int(args['target'])
    with open(args['dataset']) as inf:
        for line in inf:
            temp_string = ""
            for i, token in enumerate(line.replace('\t', ',').rstrip().split(',')):
                if token == "":
                    temp_string += "1000001 " 
                elif i == 0:
                    temp_string = token + " " + temp_string
                else:
                    temp_string += (str(int(hashstr(token, 1e+6))) + " ")
            outf.write(temp_string + "\n")
    inf.close()

