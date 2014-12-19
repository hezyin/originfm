#!/usr/bin/env python

import os
import argparse

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
                if token == "x":
                    continue
                if i == target:
                    temp_string = token + " " + temp_string
                else:
                    temp_string += (str(i) + ":" + token + " ")
            outf.write(temp_string + "\n")
    inf.close()
    outf.close()
                  
