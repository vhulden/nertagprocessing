# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:42:43 2015

@author: Vilja Hulden

Extract NER tags from output of Stanford CoreNLP

Read a directory  NER-tagged files
Output a .csv file with entity, tag, filename as in
John Lennon , PERSON , beatlesfile.txt

Set workdir, readdir, outputdir to appropriate values below

"""

import re,os

"""SECTION FOR LOCAL DEFINITIONS -- YOU NEED TO CHANGE THESE"""

workdir =  "/Users/miki/work/research/digital/scriptsforgithub/nertagprocessing/"
readdir = "samplenertagged/" #this is where your NER-tagged files are
outputdir = workdir
outputfile = "nertags.csv" #this is the file created by this script

"""END SECTION FOR LOCAL DEFINITIONS, CODE FOLLOWS"""

nertaglist = []
nametagtexts = []

for nerfile in os.listdir(workdir+readdir):
    print "Processing file %s" % nerfile
    with open(workdir+readdir+nerfile) as f:
        nerprocessed = f.readlines()
        
    
    nerprocessedenum = enumerate(nerprocessed)
    
    namesandtags = []
    
    for index, line in nerprocessedenum:
        skipindex = 0 #to avoid going over list boundary due to old skipindex value
        if 'NamedEntityTag' in line: #if it's a tagged line
            thisline = line.split()
            # if line has a non-null tag
            if thisline[5] != 'NamedEntityTag=O]' and index < len(nerprocessed):
                newtag = thisline[5]
                newname = [thisline[0]]
                myindex = index+1
                try:
                    nextline = nerprocessed[myindex]
                except IndexError:
                    break
                # as long as the same tag continues, assume same entity
                while nextline.strip().endswith(thisline[5]):
                    nextlinelist = nextline.split()
                    nextlinename = nextlinelist[0]
                    newname.append(nextlinename)                   
                    myindex += 1
                    try:
                        nextline = nerprocessed[myindex]
                    except IndexError:
                        myindex -= 1
                        break
                skipindex = myindex - index
                # now we need to skip ahead so we don't reprocess name parts 
                # already included under a tag
                for i in range(0,skipindex):
                    next(nerprocessedenum)
                # clean up so we only have names and tags              
                newname[:] = [re.sub('\[Text=','',namepart,count=0, flags=0) for namepart in newname]
                thistag = re.sub('NamedEntityTag=([A-Z]+)\]*','\g<1>',newtag,count=0, flags=0)
                newnamestring = " ".join(newname)
                #remove commas in named entity so they don't mess up the csv
                newnamestring = re.sub(',','',newnamestring,count=0,flags=0)
                # add tag and filename to line
                newline = [newnamestring]
                newline.append(thistag) 
                newline.append(nerfile)
                nameplustagplusfile = " , ".join(newline)
                namesandtags.append(nameplustagplusfile)
    
    nametagtext = "\n".join(namesandtags) #from a single file
    nametagtexts.append(nametagtext) #add tags from single file to list 

fulltext = "\n".join(nametagtexts) # tags from all files into text
with open(outputdir+outputfile, 'w') as f:
  f.write(fulltext)

    
    
