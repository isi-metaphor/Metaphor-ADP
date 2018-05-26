#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Convert logical forms into Henry input, adding nonmerge contraints
# Ekaterina Ovchinnikova <katya@isi.edu>, 2012
# Jonathan Gordon <jgordon@isi.edu>, 2014

# In order to see options, run
#   ./IntParser2Henry.py -h

import argparse
import sys
import re
import os
import json
from collections import defaultdict

id2prop = defaultdict(list)
pred2farg = defaultdict(list)


def add_id2prop(id_str,arg):
    ids = id_str.split(',')
    for id in ids:
        id2prop[id].append(arg)


def generate_sameID_nm():
    nm = ''
    for id in id2prop.keys():
        if len(id2prop[id])>1:
            nm += ' (!='
            for arg in id2prop[id]:
                nm += ' ' + arg
            nm += ')'
    return nm


def generate_freqPred_nm():
    nm = ''
    for pred in pred2farg.keys():
        if len(pred2farg[pred])>1:
            nm += ' (!='
            for arg in pred2farg[pred]:
                nm += ' ' + arg
            nm += ')'
    return nm


def main():
    parser = argparse.ArgumentParser(description='Convert logical forms into '
                                     'Henry input, adding nonmerge contraints.')
    parser.add_argument('--input', default=None,
                        help='Input file containg logical forms.')
    parser.add_argument('--output', default=None,
                        help='Output file containing Henry input.')
    parser.add_argument('--textid', default=False, action='store_true',
                        help='Text IDs used.')
    parser.add_argument('--nonmerge', nargs='+', default=[],
                        help='Add nonmerge constraints. Values: samepred '
                        '(args of a pred cannot be merged), sameid (args of '
                        'preds with same id cannot be merged), freqpred (args '
                        'of frequent preds cannot be merged).')
    parser.add_argument('--cost', type=int, default=1,
                        help='Input observation costs.')

    pa = parser.parse_args()

    samepred = 'samepred' in pa.nonmerge
    sameid = 'sameid' in pa.nonmerge
    freqpred = 'freqpred' in pa.nonmerge

    lines = open(pa.input, 'r') if pa.input else sys.stdin
    ofile = open(pa.output, 'w') if pa.output else sys.stdout

    output_str = ''
    id_prop_args_pattern = re.compile('(\[(\d+)\]:)?([^\[\(]+)(\((.+)\))?')
    sent_id_pattern = re.compile('id\((.+)\)')
    text_id_pattern = re.compile('% TEXTID\s*\(\s*([^\s\t]+)')
    postfix_pattern = re.compile('.+-([a-z]+)$')
    sent_id = ''
    prop_id_counter = 0
    text_id = ''
    just_TEXT_ID = 0
    for line in lines:
        if line.startswith('%'):
            TIDmatchObj = text_id_pattern.match(line)
            if TIDmatchObj:
                if text_id != '':
                    if freqpred: ofile.write(generate_freqPred_nm())
                    ofile.write('))\n')
                    pred2farg.clear()
                text_id = TIDmatchObj.group(1)
                ofile.write('(O (name ' + text_id + ') (^')
                just_TEXT_ID = 1
                prop_id_counter = 0
        elif line.startswith('id('):
            SIDmatchObj = sent_id_pattern.match(line)
            if SIDmatchObj:
                sent_id = SIDmatchObj.group(1)
                if not pa.textid:
                    ofile.write('(O (name ' + sent_id + ') (^')
            #else: print 'Strange sent id: ' + line

            if just_TEXT_ID == 1:
                just_TEXT_ID = 2
            else: just_TEXT_ID = 0
        elif line.strip() and just_TEXT_ID!=2:
            props = line.split(' & ')
            for prop in props:
                matchObj = id_prop_args_pattern.match(prop)
                if matchObj:
                    prop_id_counter+= 1

                    if matchObj.group(2): word_id = matchObj.group(2)
                    else: word_id = 'ID'+str(prop_id_counter)

                    prop_name = matchObj.group(3)
                    prop_name = re.sub(r"[\s_:./]+",'-',prop_name)

                    # Don't include predicates not containing letters or
                    # numbers
                    if not bool(re.search('[a-z0-9]', prop_name,
                                          re.IGNORECASE)):
                        continue

                    if matchObj.group(5):
                        prop_args = matchObj.group(5)
                    else: prop_args = ''

                    nm = ''
                    if prop_args != '':
                        prop_args = ' ' + prop_args.replace(',', ' ')
                        if samepred: nm = ' (!=' + prop_args + ')'
                        if sameid or freqpred:
                            args = prop_args.split()
                            if sameid and matchObj.group(2):
                                add_id2prop(matchObj.group(2), args[0])
                            if freqpred:
                                postfixObj = postfix_pattern.match(prop_name)
                                if not postfixObj or \
                                  postfixObj.group(1) == 'in':
                                    if args[0] not in pred2farg[prop_name]:
                                        pred2farg[prop_name].append(args[0])

                    ofile.write(' (' + prop_name + prop_args + ' :' + \
                                str(pa.cost) + ':' + sent_id + '-' + \
                                str(prop_id_counter) + ':[' + word_id + '])')
                    if samepred:
                        ofile.write(nm)
                #else: print 'Strange proposition: ' + prop + '\n'

            if sameid:
                ofile.write(generate_sameID_nm())
            id2prop.clear()
            if not pa.textid:
                if freqpred:
                    ofile.write(generate_freqPred_nm())
                ofile.write('))\n')
                prop_id_counter = 0
                pred2farg.clear()

    if text_id != '':
        if freqpred: ofile.write(generate_freqPred_nm())
        ofile.write('))\n')
    ofile.close()


if __name__ == '__main__':
    main()
