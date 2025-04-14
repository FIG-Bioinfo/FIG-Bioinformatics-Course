# Hammers Exercise 1 - What are "Hammers", why do we need them, and how do we build them?

Objective: Define and Describe the idea behind the "Genetic Barcode" that we call a "Hammer".

At the end of the last unit, you were able to successfully create a "Representative Genome Set" or "RepGenSet". A "RepGenSet" provides you with a broad overview of your "Universe of Genomes". Suppose that you wanted to add a new genome to your Universe. How would you know which genome is the new genome's nearest representative? How would you find it? This is where the idea of a "Genetic Barcode" comes in. 

You are probably familiar with the use of "barcodes" to identify a product or to encode a device's serial-number. In bioinformatics, we use readily identifiable short sequences of DNA to serve as a "set of barcodes" that identify each representative genome. The more "barcodes" that some genome has in common with a given representative genome, the more likely it is that the genome in question is related to that representative genome. In this course, we will be particularly interested in a set of DNA 20-mers that we call "Hammers".

"Hammers" allow us to quickly determine which representative genomes are most similar to an unknown genome or the members of a population of genomes in a sample. Historically, when working with bioinformatics data, we are given a sample containing one or more genomes that have been annotated. By "annotated", we mean that the sequence-data within the sample has been compared to the rest of the known universe of genomes, the data may have been been sorted into "bins" based on a set of representative genomes or a smaller set of genomes that the user is interested in, the sequence-data may have been "assembled" into longer sequences called "contigs", and the gene-containing regions on these contigs may have been located and had roles assigned to them. However, complete annotation of a sample can be an expensive and time-consuming process. Often, we are only interested in performing a "census" of which genera are present in a sample. We shall see that a set of "Hammers" will allow us to quickly perform such a "census", sidestepping the more complex and expensive complete annotation process.

## Materials

```
FIG-Bioinformatics-Course/
├── 2_Hammers
│   └── 2.1_Hammers-Creation-and-Application/
│       └── Hammers-Exercise-1_Creating-Hammers.md (you are here)
└── Data/
    ├── myrep10.genomes-and-lengths.txt
    └── myrep50.genomes-and-lengths.txt
```

In the Kmer exercises, we used protein and DNA jaccard similarities to compare sequences
and to find which sequence was "closest" ("most similar") to a query sequence.
In those exercises, we computed the jaccard similarity betwen two sequences using the complete sets of Kmers from each sequence. An exhaustive comparison of the full set of Kmers is quite feasible if we are looking at the few hundred Kmers in a pair of individual proteins or gene-sequences, but it becomes prohibitively expensive when looking at entire genomes that contain millions of characters.

Recall that the jaccard similarity is defined as the ratio of the number of members in the interesection of two sets divided by the number of members in the union of the two sets. 
Note that there is nothing in the definition of jaccard similarity that requires us to use the full set of Kmers present in the two sequences; we could use any defined smaller subset of Kmers and still get approximately the same numerical ratio as long as the method used to define the subset yields an "unbiased sample" of Kmers in the statistical sense. In this module,
we will introduce a particular subset of Kmers we call "Hammers" that will allow us to rapidly identify which representative genome is most similar to a sample genome without requiring an exhaustive comparison that uses every Kmer in the genome.

A "Hammer" is a 20-character DNA sequence that satisfies the following properties:

* It occurs exactly once in exactly one genome that is a member of a set of special genomes that we are calling "Representative Genomes" ("RepGen Set" for short).

* It is found within a particular class of genes that encode what we call "Singly-Occuring Universal Roles" ("SOURs" for short). A SOUR is characterized as follows:

    *  It is "Singly Occurring", which means that a genome contains exactly one gene that implements this function.

    * It implements a "Universal Role", that is, it can be expected to occur within every genome.

The SOURs are often part of the "Central Machinery" of a cell. Ask Grimoire to tell you what is meant by "Central Machinery of a Cell", with particular emphasis on Bacteria and Archaea.

We can estimate the similarity of two genomes by computing the jaccard similarity between the sets of hammers that are found in the two genomes. The jaccard similarity computed using just the sets of hammers will be less numerically precise than the jaccard similarity using the full genome because the sets of hammers are smaller than the sets of all Kmers, but it will be close enough to the more precise value to be useful, and it can be computed much faster.

The observation of a "Hammer" within a genome serves as strong evidence that it is closely related to the Representative genome from which that hammer was derived. The more hammers from a given representative that a genome contains, the more likely it is that that genome is closely related to that representative.

## Exercises

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

In this exercise, we will work through a simplified "toy problem" that will illustrate the steps involved in constructing a set of hammers.
You will first fetch the set of `PheS` DNA sequences from BV-BRC, for the RepGenSet `myrep10` that you constructed in `RepGen-Exercise-1`. (Recall that `PheS`, the gene for "Phenylalanine tRNA Synthase", is an instance of a SOUR.)
We will then walk you through a simplified version of the steps required to find the hammers associated with that single SOUR, and write those hammers to a tab-separated output file.
In future exercises, we will use these hammers to identify a "Mystery Genome",
and to identify which genomes are present in a "Metagenomic Sample" (sample containing more than one genome).

1. To fetch the DNA sequences for your RepGenSet `myrep10`, please open the BV-BRC app and enter the following pipeline. (Remember that you must enter the entire pipeline as a single command-line, even though as displayed below it wraps across multiple lines on your screen.):

```
p3-get-genome-features --selective --input Data/myrep10.genomes.tbl --col genome_id --eq product,'Phenylalanyl-tRNA synthetase alpha chain (EC 6.1.1.20)' --attr patric_id | p3-get-feature-sequence --dna --col feature.patric_id > Data/myrep10.PheS.dna_sequences.fna
```
2. To make a set of hammers for the selected SOUR, we extract all of the DNA 20-mers that occur exactly once in exactly one genome. How do you think one might do that?
* Hint: Can you remember which datatype would be appropriate for associating a string with the number of times that it occurs?

    Load in the file `Definitions.html` as in previous exercises. Then, ask Grimoire to write a python program named `hammer_creator.py` that will:

```
    * Accept as '-K' a mandatory integer Kmer-length command-line argument;
        
    * Read a FASTA-formatted DNA file from 'STDIN' using BioPython;
    
    * The portion of the FASTA header up to the first whitespace-character is the "feature-ID" ('fid'). Please extract the feature-ID and build a dictionary mapping feature-IDs to sequences, after first converting the sequences to lower-case.

    * Each feature-ID has the format 'fig|x.y.peg.z', where 'x', 'y', and 'z' are integers, and the 'fig|' and '.peg' portions are literal strings, not variables. The substring 'x.y' is the 'genome_id' for the sequence; please use a regular expression to extract the genome-ID from the feature-ID. 
    
    * Find all of the Kmers that occur exactly once in exactly one genome; these Kmers are the "Hammers"

    * Print a two column tab-separated table to 'STDOUT' of the hammers and the feature-ID that each hammer was found in, with column-headers of "hammer" and "fid".

    * Finally, please print to 'STDERR' the number of sequences that were read, the number of Kmers that were processed, and the number of Kmers that were hammers, and then exit.
```

Paste Grimoire's program into the code-template `Code/hammer_creator.py`.
Note that the template includes a "block comment" section reserved for the program's pseudocode, so paste in Grimoire's pseudocode if it generated it, else ask it to generate pseudocode for the program if it didn't. Once you are done copying and pasting, save the code using the "Save" menu-item under the "File" menu.

3. To build the set of hammers, invoke the code that Grimoire created as follows:

```
python Code/hammer_creator.py -K 20 < Data/myrep10.PheS.dna_sequences.fna
> Data/myrep10.PheS.hammers.tbl
```

4. BONUS: Build hammers for `myrep50`.
How do the number of hammers found in `myrep50` compare to the number found in `myrep10` ?

## Self-Check

For `myrep10`, your `hammer_creator.py` program should print the following summary-report to STDERR:

```
Number of sequences read: 141
Number of K-mers processed: 149195
Number of hammers: 148751
```

For `myrep50`, your `hammer_creator.py` program should print the following summary-report to STDERR:

```
Number of sequences read: 921
Number of K-mers processed: 923907
Number of hammers: 903835
```

A few points to note:

* In both cases, nearly every Kmer in the input data turned out to be a "hammer".
The reason for this is that the sequences in `myrep10` and `myrep50`
are all very far apart. Recall that the '10' in `myrep10` means that
none of the PheS protein sequences in `myrep10` have more
than 10 protein 8-mers out of roughly 350 in common.
A similar result occurs at the DNA level: Since the PheS DNA sequences
are very far apart, they have few DNA 20-mers in common,
and hence few of the DNA 20-mers get eliminated during the hammer-building process.

* By contrast, the sequences in `myrep50` are closer together,
since they are allowed to have up to 50 protein 8-mers in common,
and there are many more of them. More similarity at the protein level
means a higher chance of similarity at the DNA level, and more genomes
means more opportunities for a DNA 20-mer to be eliminated
because it was found in more than one genome.
Both of these factors imply that when constructing hammers
for a higher similarity-threshold RepGen,
a larger fraction of Kmers will be eliminated because
they will not satisfy the hammer condition,
but the remaining hammers will be more "specific",
i.e. they will identify a more closely-related subset of genomes.

