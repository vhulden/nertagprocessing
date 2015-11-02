# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 13:13:27 2015

@author: Vilja Hulden

This script takes as input DATE.txt, created by the script sortnertags.py, and 
processes it to produce another text file where only lines that contain a four-digit year are preserved (e.g. 1921, 1920s, 1920-1929). This is not perfect, of course; e.g. four-digit page numbers will be included. But it is reasonably useful for word cloud creation, for example, if you want to quickly look at which years are mentioned frequently.
"""


import re

inputfile = "nerentitieslists/DATE.txt"
outputfile = "nerentitieslists/DATE-YEARONLY.txt"


with open(inputfile) as f:
    yearlines = [line.strip() for line in f.readlines() if re.search('[0-9][0-9][0-9][0-9]',line,flags=0)]
    
yeartext = "\n".join(yearlines)

with open(outputfile,'w') as f:
    f.write(yeartext)