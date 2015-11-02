This provides a number of Python scripts for dealing with the output of the Stanford CoreNLP toolkit`s named entity recognition (NER) portions.

##process_ner.py

The basic script is `process_ner.py`, which does the following:

* Read a directory  NER-tagged files
* Output a .csv file with entity, tag, filename as in
* John Lennon , PERSON , beatlesfile.txt

You need to run this first, as all the other scripts use its output. You can then use the other scripts included here to further process your NER data.

##sortnertags.py

`sortnertags.py` takes as input the .csv file created by `process_ner.py` and produces a set of files with all the entities in that tagset. For example, `PERSON.txt` will contain all entities tagged as PERSON.

##dateyearextract.py

`dateyearextract.py` is just a super-simple script that takes the `DATE.txt` produced by `sortnertags.py` and extracts those dates that look like years, including e.g. 1921, 1920s, 1920-1929.

##combineandcountpersons.py
`combineandcountpersons.py` takes as input the .csv file created by `process_ner.py` and processes the PERSON-tagged entities further. First, it collapses names, so that the longest version of each name is made the standard for that name. That is, it collapses "Gompers" and "Samuel Gompers" and "President Samuel Gompers" into one entity, "President Samuel Gompers".

The assumption is that if "Gompers" and "Samuel Gompers" occur in the same document, the "Gompers" in each refers to the same person and these two entities can therefore be collapsed into one.

This is done by creating a dictionary of the format:

```
{'lastname': [['namevariant1'], ['namevariant2'], ...]}
```, e.g.

```
{'gompers': ['gompers'], ['samuel', 'gompers'], ['president', 'gompers']}
```

and then selecting the longest list for each key as the "canonical" representation.

Only names longer than one word are saved; other are ignored. This get rid of lots of entities mistakenly identified as persons.

It produces two files: `frequentpersons.txt` and `frequentpersonsindocs.txt`. 

The first, `frequentpersons.txt` contains a count of how many times each name appears across the documents; each occurrence is counted, including multiple per document. It looks like this:

`samuel gompers: 51`

The second, `frequentpersonsindocs.txt`, contains a count of how many documents each person appears in.
It looks the same as `frequentpersons.txt` but the count should of course be lower:

`samuel gompers: 3`

Both scripts undercount because there can be several longest versions of a name, e.g. 

* president samuel gompers
* president gompers
* samuel gompers

## Auxiliary files

For reference, I have provided the files `nertags.csv` (produced by `process_ner.py`) as well as `frequentpersons.txt` and `frequentpersonsindocs.txt` (produced by `combineandcountpersons.py`).

In addition, the directory `samplenertagged` contains a few NER-tagged files on which the scripts can be run for testing purposes, and the directory  `nerentitieslists` contains the entity lists (ORGANIZATION.txt, etc.) produced by the `sortnertags.py` script when these scripts are run on the files in the `samplenertagged` directory.
