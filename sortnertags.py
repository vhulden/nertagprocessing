# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 20:07:15 2015

@author: Vilja Hulden

A script for further processing of NER output. 

Input is a csv file created by process-ner.py; it looks like this:
Named entity , ENTITY-TAG , filename 
e.g.
American Federation of Labor , ORGANIZATION , 2012_ocr_10.2307_41410719.txt.out

Output is a series of text files, each containing the entities belonging to a specific tag (ORGANIZATION.txt, etc.)

"""
import os
from collections import defaultdict

workdir = "/Users/miki/work/research/digital/scriptsforgithub/nertagprocessing/"
inputfile = "nertags.csv"
outputdir = "nerentitieslists/"
if not os.path.exists(outputdir):
    os.makedirs(outputdir)


print "Reading and processing file ..."

with open(workdir+inputfile) as f:
    nertagslist = [line.strip().split(',') for line in f.readlines()]

print "Creating tagset..."

tagset = {line[1].strip() for line in nertagslist}


tagsdict = defaultdict(list)


for tag in tagset:
    print "Working on tag %s" %tag
    for entity,thistag,_ in nertagslist:
        if thistag.strip() == tag:
            tagsdict[tag].append(entity)


for tag in tagsdict:
    fname = tag + ".txt"
    entities = "\n".join(tagsdict[tag])
    with open(workdir+outputdir+fname,'w') as f:
        f.write(entities)
            
print "Done."
