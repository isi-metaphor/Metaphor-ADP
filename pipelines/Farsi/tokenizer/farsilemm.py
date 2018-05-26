#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

input_fl = sys.stdin
output_fl = sys.stdout
dict_fl = open(sys.argv[1], "rb")

badChars1 = {
    u"ۀ":u"ه",
    u"ي":u"ی",
    u"ك":u"ک"}

PREFIXES = [
    u"می",
    u"نمی",
    u"بی",
    u"نا"]

POSTFIXES = [
    u"ام",
    u"ات",
    u"اش",
    u"ایم",
    u"اید",
    u"اند",
    u"یم",
    u"یت",
    u"یش",
    u"یمان",
    u"یتان",
    u"یشان",
    u"ها",
    u"تر",
    u"ترین",
    u"هایم",
    u"های",
    u"هایی",
    u"هایمان",
    u"هایتان",
    u"هایت",
    u"هایش",
    u"هایشان",
    u"ای",
    u"ایم",
    u"اید",
    u"اند",
    u"ترین",
    u"تران",
    u"ترها",
    u"ترینها",
    u"ترهای",
    u"ترینهای",
    u"ترانی",
    u"ترینهایی",
    u"ترینی",
    u"ترانی",
    u"تری"]

PREFIXES = [p.encode("utf-8") for p in PREFIXES]
POSTFIXES = [p.encode("utf-8") for p in POSTFIXES]

badChars = {}
for item in badChars1:
    badChars[item.encode("utf-8")] = badChars1[item].encode("utf-8")

lemm_dict = set()
for line in dict_fl:
    line = line.replace("\n", "")
    form, _, lemma = line.split("\t")[0:(len(line) - 1)]
    lemm_dict.add(form)
    lemm_dict.add(lemma)


def gen_bigrams(tokens):
    for i in xrange(len(tokens) - 1):
        yield tokens[i], tokens[i + 1]


def gen_trigrams(tokens):
    for i in xrange(len(tokens) - 2):
        yield tokens[i], tokens[i + 1], tokens[i + 2]


def preprocess_prefixes(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] in PREFIXES:
            yield tokens[i] + "-" + tokens[i + 1]
            i += 2
        else:
            yield tokens[i]
            i += 1

    while i < len(tokens):
        yield tokens[i]
        i += 1


def preprocess_postfixes(tokens):
    i = 1
    preprocessed = []
    for t in tokens:
        if t in POSTFIXES:
            preprocessed[-1] = preprocessed[-1] + "-" + t
        else:
            preprocessed.append(t)
    return preprocessed


def check_with_dict(tokens):
    bigrams = list(gen_bigrams(tokens))
    trigrams = list(gen_trigrams(tokens))
    mapped = []
    i = 0
    while i < len(tokens):
        if i < len(trigrams):
            if "%s-%s-%s" % trigrams[i] in lemm_dict:
                mapped.append("%s-%s-%s" % trigrams[i])
                i += 3
                continue

            elif "%s-%s%s" % trigrams[i] in lemm_dict:
                mapped.append("%s-%s%s" % trigrams[i])
                i += 3
                continue

            elif "%s%s-%s" % trigrams[i] in lemm_dict:
                mapped.append("%s%s-%s" % trigrams[i])
                i += 3
                continue

            elif "%s%s%s" % trigrams[i] in lemm_dict:
                mapped.append("%s%s%s" % trigrams[i])
                i += 3
                continue

        if i < len(bigrams):
            if "%s-%s" % bigrams[i] in lemm_dict:
                mapped.append("%s-%s" % bigrams[i])
                i += 2
                continue

            elif "%s%s" % bigrams[i] in lemm_dict:
                mapped.append("%s%s" % bigrams[i])
                i += 2
                continue

        mapped.append(tokens[i])
        i += 1

    return mapped


for line in input_fl:
    #line = line.replace("\n", "")
    line = line.strip()

    if line == "":
        output_fl.write("\n")
        continue

    for ch in badChars:
        line = line.replace(ch, badChars[ch])

    tokens = line.split(" ")
    lastToken=tokens[-1]

    removedChar = ""
    lastChar = lastToken[-1]

    if lastChar in [".", ",", ";", "?", "!", ":"]:
        removedChar=lastChar
        tokens[-1] = tokens[-1][:(len(tokens[-1]) -1)]

    tokens = check_with_dict(tokens)

    tokens = list(preprocess_prefixes(tokens))
    tokens = list(preprocess_postfixes(tokens))

    output_fl.write(" ".join(tokens))
    output_fl.write("%s\n"%removedChar)
