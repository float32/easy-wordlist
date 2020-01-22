#!/usr/bin/env python3

# MIT License
#
# Copyright 2020 Tyler Coy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



# Use this script to filter a wordlist, keeping only words that are 'easy' to
# type. Of course 'easy' is vague and subjective, but in this case we keep only
# words for which no finger must type two consecutive characters, assuming a
# QWERTY layout. For example, we filter out 'amulet' because 'mu' is difficult
# to type. We also filter out all words containing a hyphen because, come on.

# If you use the output of this script as a wordlist for a passphrase generator,
# be aware of the security implications. For example, applying it to EFF's
# large wordlist, which contains 7776 words and ~12.9 bits of entropy per word,
# results in a list of only 3440 words, ~11.7 bits per word.

import argparse
import sys
from operator import eq



parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='input_file', default='-',
    help='Input hex file (default stdin)')
parser.add_argument('-o', dest='output_file', default='-',
    help='Output hex file (default stdout)')
args = parser.parse_args()

if args.output_file == '-':
    args.output_file = sys.stdout

if args.input_file == '-':
    args.input_file = sys.stdin



with open(args.input_file) as file:
    wordlist = [line.split()[-1] for line in file.readlines()]

finger_groups = ('qaz', 'wsx', 'edc', 'rfvtgb', 'yhnujm', 'ik', 'ol', 'p')
finger_groups = zip(range(len(finger_groups)), finger_groups)
key_map = dict()
for group, keys in finger_groups:
    for key in keys:
        key_map[key] = group

def is_easy(word):
    code = tuple(key_map[key] for key in word)
    most = code[0:-1]
    rest = code[1:]
    return not any(map(eq, most, rest))

with open(args.output_file, 'w') as file:
    for word in wordlist:
        if '-' not in word and is_easy(word):
            try:
                file.write(word + '\n')
            except BrokenPipeError:
                pass
