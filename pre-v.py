#!/usr/bin/env python
# this script is used to transform train.csv (on server /disk1/kongdy/ad/train.csv) to train.libfm

import os
import argparse
import hashlib

def hashstr(str, nr_bins):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(), 16)%(nr_bins -1)+1

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Preprocess Dataset for my FM')
    parser.add_argument('dataset', help='path to data file')
    parser.add_argument('output', help='ouput path')
    parser.add_argument('-d', '--delimiter', help='specify delimiter of dataset')
    parser.add_argument('-t', '--target', default=0, help='specify y column')

    args = vars(parser.parse_args())
    outf = open(args['output'], "w+")
    target = int(args['target'])
    with open(args['dataset']) as inf:
        for line in inf:
            temp_string = ""
            for i, token in enumerate(line.rstrip().split(args['delimiter'])):
                if token == "":
                    continue
                if i == 0:
                    continue
                if i == 1:
                    temp_string = token + " " + temp_string
                elif i < 15:
                    temp_string += str(i-1) + ":" + token + " "
                else:
                    temp_string += str(i-1) + ":" + str(int(hashstr(token, 1e+6))) + " "
            outf.write(temp_string + "\n")
    inf.close()
