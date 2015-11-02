# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:39:22 2015

@author: Vilja Hulden

This script takes in a csv file created by the script process_ner.py,
with entity, tag, filename as in:
John Lennon , PERSON , beatlesfile.txt

It processes the PERSON-tagged entities so that the longest version of each name
is made the standar for that name. That is, it collapses "Gompers" and "Samuel Gompers" and "President Samuel Gompers" into one entity, "President Samuel Gompers".

The assumption is that if "Gompers" and "Samuel Gompers" occur in the same document, the "Gompers" in each refers to the same person and these two entities can therefore be collapsed into one.

This is done by creating a dictionary of the format:
{'lastname': [['namevariant1'], ['namevariant2'], ...]}, e.g.
{'gompers': ['gompers'], ['samuel', 'gompers'], ['president', 'gompers']}
and then selecting the longest list for each key as the "canonical" representation.

Only names longer than one word are saved; other are ignored. This get rid of lots of entities mistakenly identified as persons.

It produces two files: frequentpersons.txt and frequentpersonsindocs.txt. 

The first, frequentpersons.txt contains a count of how many times each name appears across the documents; each occurrence is counted, including multiple per document. It looks like this:
samuel gompers: 51

The second, frequentpersonsindocs.txt, contains a count of how many documents each person appears in.
It looks the same as frequentpersons.txt but the count should of course be lower:
samuel gompers: 3
It undercounts, because there can be several longest versions of a name, e.g. president samuel gompers
president gompers
samuel gompers

"""
import re
from collections import defaultdict
from collections import Counter

workdir = "/Users/miki/work/research/digital/scriptsforgithub/nertagprocessing/"
inputfile_ner = "nertags.csv"
outputdir = workdir
outputfilepersons = "frequentpersons.txt"
outputfiledocs = "frequentpersonsindocs.txt"

with open(workdir+inputfile_ner) as f:
    nerlist = [line.strip().split(',') for line in f.readlines()]

fileset = {line[2].strip() for line in nerlist}


personsdict = defaultdict(list)
orgsdict = defaultdict(list)


for f in fileset:
    print "Entering filename %s in dictionary" %f
    for entity,tag,filename in nerlist:
        if filename.strip() == f:
            if tag.strip() == 'PERSON':
                personsdict[f].append(entity.lower().strip())
                

personsonly = []
accept = 0
newpersonsdict = defaultdict(list)
for fn in personsdict:
    print "Processing names in filename %s" %fn
    entdict = defaultdict(list)   
    for person in personsdict[fn]:
        plist = person.split()
        # if person's last name is in the dictionary as key, 
        # enter this name variant into the dictionary
        if plist[-1] in entdict:
            entdict[plist[-1]].append(plist)
        # otherwise make the last name a new key in the dictionary
        else:
            entdict[plist[-1]] = [plist]

    for entity in entdict:
        thisentnames = entdict[entity]
        for name in thisentnames:
            if len(name) > 1:
                selectname = max(thisentnames,key=len)
                namestring = " ".join(selectname)
                namestring = re.sub(',','',namestring)
                # add this filename to list of files containing this namestring
                # unless it s already there
                if namestring in newpersonsdict and fn not in newpersonsdict[namestring]:
                    newpersonsdict[namestring].append(fn)                
                else:
                    newpersonsdict[namestring] = [fn]
                # also add namestring to list of namestrings
                # this is for counting how many times a person is mentiond
                # regardless of name variant   
                personsonly.append(namestring)

# count how many documents each person appears in

frequentindocslist = []
for key in newpersonsdict:
    if len(newpersonsdict[key]) > 1:
        frequentindocstring = key + ":" + str(len(newpersonsdict[key]))
        frequentindocslist.append(frequentindocstring)

#this counts how many time a name has appeared, regardless of in how many docs
countpersons = Counter(personsonly)

frequentpersonslist = []
for key in countpersons:
	if countpersons[key] > 1:
         frequencystring = key + ":" + str(countpersons[key])
         frequentpersonslist.append(frequencystring)

frequentpersonstext = "\n".join(frequentpersonslist)         
with open(outputfilepersons,'w') as f:
    f.write(frequentpersonstext)
    
frequentindocstext = "\n".join(frequentindocslist)         
with open(outputfiledocs,'w') as f:
    f.write(frequentindocstext)