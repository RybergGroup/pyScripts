#! /usr/bin/python3

import sys
import argparse

parser = argparse.ArgumentParser(description='Process FASTQ file.')
parser.add_argument('--cutoff', help='cut of symbol for what is considered low quality score', default=" ")
parser.add_argument('-f', '--file', help='input file. FASTQ format.', default='-')
parser.add_argument('--format', help='output format. FASTA/FASTQ', default='FASTQ')

options = parser.parse_args()

options.format = options.format.upper()

if not (options.format == 'FASTQ' or options.format == 'FASTA'):
    raise Exception ("Only FASTQ and FASTA are accepted output formats. Not: " + options.format) 

prev_colour = 0
options.cutoff = options.cutoff[0]

if  options.file:
    if options.file != '-':
        f = open(options.file, "r")
    else:
        f = sys.stdin

else:
    raise Exception ("File name or - (stdin) needed")

seq=''
qual=''
mode = '0'

while True:
    line = f.readline()
    line = line.strip()
    if not line:
        break

    if mode == '0' and line[0]=='@':
        if options.format=='FASTQ':
            print('@', end='')
        if options.format=='FASTA':
            print('>', end='')
        print(line.lstrip('@'))
        mode = 's'
    elif mode == 's':
        seq = line
        mode = '1'
    elif mode == '1' and line[0]=='+':
        mode = 'q'
    elif mode == 'q':
        qual = line
        mode = 'P'

    c = 0
    if mode == 'P':
        for base in seq:
            if qual[c] <= options.cutoff and prev_colour != 41:
                print ('\033[41m', end = '')
                prev_colour = 41
            elif qual[c] > options.cutoff and prev_colour != 0:
                print ('\033[0m', end = '')
                prev_colour = 0
            print (base, end='')
            c += 1
        if options.format=='FASTQ':
            print()
            if prev_colour != 0:
                print ('\033[0m', end = '')
                prev_colour = 0
            print('+')
            for base in qual:
                if base <= options.cutoff and prev_colour != 41:
                    print ('\033[41m', end = '')
                    prev_colour = 41
                elif base > options.cutoff and prev_colour != 0:
                    print ('\033[0m', end = '')
                    prev_colour = 0
                print(base, end='')
        if prev_colour != 0:
            print ('\033[0m', end = '')
            prev_colour = 0
        print()
        mode = '0'


if f != sys.stdin:
    f.close()
