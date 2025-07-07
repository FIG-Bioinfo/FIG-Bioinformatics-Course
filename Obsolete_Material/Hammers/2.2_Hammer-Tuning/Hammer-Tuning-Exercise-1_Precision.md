# Hammer Precision Exercise 1

Objective: Understand the concept of hammer precision and learn how to evaluate the effectiveness of genetic barcodes (hammers) in identifying specific genomes.

Hammers are unique k-mers that occur exactly once in exactly one representative genome. The precision of a hammer refers to how specific its sequence is to the genomes with a representative genome's "peer group", which is the set of genomes that are closer to that representative by the similarity-measure being used than to any other representative. (Recall that the measure we are using in this course is the number of protein K-mers in common for the `PheS` gene.)
A highly specific hammer will only match a single peer-genome or two, while a less specific hammer may match all of the genomes within a representative's peer-group.

This exercise will help you understand how to evaluate and improve the precision of your hammers by comparing them to the other hammers inside of the hammer set. 

## Materials:

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 2_Hammers
│   └── 2.2_Hammer-Tuning/
│       └── Hammer-Tuning-Exercise-1_Precision.md (you are here)
├── Data/
│   ├── myrep10.PheS.hammers.tbl (from Hammer-Exercise-1)
│   ├── myrep10.seqs.tbl
│   └── test_genomes.fna (new file with multiple test genomes)
└── Code/
    ├── find_duplicate_hammers.py
    └── hammer_precision.py
```

## Exercises:

1. Hammers have multiple functions. One of their most important applications is that they allow us to identify the nearest representative of a genome. We can make such an identification by noting that if a genome is a peer of a representative genome, then it is likely that it will also have hammers in common with that representive (or as we often say if it is "hit" by hammers from its representative), and the more hammers that a genome has in common with a representative, the more likely it is to be a peer of that representative.
However, the converse is not true: If a genome is hit by a hammer from a representative, it is not neccessarily true that it is a peer, as we saw in `Hammer-Exercise-2`
and `Hammer-Exercise-3`, where `MysteryGenome1` also received low-scoring hits
from more distant representatives in addition to being strongly hit by its nearest representative. 

In this case, we need to know if this occurs since it can skew our data to multiple genomes inside the hammer set. Ask Grimoire how it would determine if duplicate hammers exist in the `rep10.hammers.tbl` file.

2. We need to evaluate the precision of our hammers. Ask Grimoire to write a Python script named `hammer_precision.py` that does the following:
   - Reads the `rep10.hammers.tbl` file
   - For each hammer, create a counter of how many times it appears in the `rep10.hammers.tbl` file
   - Iterates through each hammer and deletes any hammers that have a counter of 1.
   - Outputs a table with columns: hammer, genome_id, counter

3. Run your `hammer_precision.py` script and analyze the results. Are there any genomes that show up more often than others? Ask Grimoire to explain to you why a genome might have more duplicate hammers than others and what it means for the accuracy of the genome inference.

4. Having more precise hammers means that you can more accurately determine where in genome space your sample is from. However, as you take hammers out of your set, you are decreasing the possibilities of finding a matching hammer for your sample. Making our hammer set more like a chisel than a sledgehammer. Ask Grimoire to give you a use case of when you would want to have more precise hammers vs when you would want to have more hammers in your set.

5. We need to create a new set of hammers that are more precise. Ask Grimoire to write a modify the Python script named `hammer_precision.py` that does the following:
   - Reads the `rep10.hammers.tbl` file
   - For each hammer, create a counter of how many times it appears in the `rep10.hammers.tbl` file
   - Iterates through each hammer and outputs any hammer that has a counter of 1 to a new file called `rep10.precise.hammers.tbl`
   - Outputs a table with columns: hammer, genome_id, counter
   - Takes a command line argument for how many duplicates of a hammer are allowed before it is removed from the set.

6. Run your `hammer_precision.py` script on the 'rep10.hammers.tbl' file with a command line argument of 5. Look at the difference in size between the original 'rep10.hammers.tbl' file and the new 'rep10.precise.hammers.tbl' file. Giving some leeway to the number of duplicates allowed, can sometimes help to improve the performance of your hammers for different use cases. Ask Grimoire to explain to you how this might work.

7. Bonus: Test out different values for the number of duplicates allowed in the `rep10.precise.hammers.tbl` file and use the different hammer sets to identify the genomes in the `test_genomes.fna` file. See if there is a relationship between the number of duplicates allowed and the performance of the hammers.

In the next exercise, we will explore additional factors that contribute to hammer performance and how to incorporate them into our hammer selection process.

## Self-Check

Result of running:
```
python 2_Hammers/2.1_Hammer-Creation-and-Application/Solutions/hammer_creator_solution.py -K 20 < 2_Hammers/2.2_Hammer-Tuning/Solutions/myrep10.five_roles.dna-sequences.solution.fna > 2_Hammers/2.2_Hammer-Tuning/Solutions/myrep10.five_roles.hammers.solution.tbl

Number of sequences read: 705
Number of K-mers processed: 1265411
Number of hammers: 1259711
```
(Insert comparison of number of Kmers read vs eliminated in this exercise vs the single-role exercise here)


Result of running:
```
time python 2_Hammers/2.1_Hammer-Creation-and-Application/Solutions/hammer_creator_solution.py -K 20 < 2_Hammers/2.2_Hammer-Tuning/Solutions/myrep50.five_roles.dna-sequences.solution.fna >  2_Hammers/2.2_Hammer-Tuning/Solutions/myrep50.five_roles.hammers.solution.tbl
Number of sequences read: 4600
Number of K-mers processed: 8083245
Number of hammers: 7923293
```

(Again, insert comparison of number of Kmers read vs eliminated in this exercise vs the single-role exercise here)

We have included solution-files in the `Solutions/` directory
for this module, but because they are quite large,
we have included them in "gzip compressed"
rather than plaintext format.
To uncompress them, it should be sufficient
to double-click on them in your operating system's 
file-browser. (NOTE: VScode cannot read gzipped files!)

Alternatively, you can uncompress them from the command-line
using the following example command:

```
gunzip pathToCompressedFile
```

where you should replace `pathToCompressedFile`
with the actual path to the file that you want to decompress,
e.g. to decompress a file named `bar.gz` in directory `Foo`,
you would type:

```
gunzip Foo/bar.gz
```


## TODO

Major rewite still needed, since the definition of "hammers" and the hammer-building process used in the current version of course has diverged from the defintions that Tory and Bruce used when they wrote the draft for this module.

Also need to verify that the hammers do not occur more than once in the RepGen contigs as opposed to just the RepGen SOURs.