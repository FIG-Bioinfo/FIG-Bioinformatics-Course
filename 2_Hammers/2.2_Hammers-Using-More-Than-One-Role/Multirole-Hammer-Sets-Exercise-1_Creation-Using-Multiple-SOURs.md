# Multirole Hammer Sets Exercise 1 - Building Hammers Using More Than One SOUR

**Objective:** Build a set of hammers starting from a set of sequences that represent more than one SOUR,
to support more reliable RepGen assignments to a sample
by requiring a "consensus" among the assignemnts made 
by each SOUR.

So far, we have built hammers for a RepGenSet
using only the PheS SOUR sequences from its RepGens.
However, we found that in addition to the reliably-identified
highest-scoring hits against RepGens that were found within the sample,
there were also a number of low-scoring "noise hits".

In this set of exercises, we will demonstrate how the
"noise hits" can be significantly reduced—or even completely eliminated—by constructing a "consensus" for which RepGens are probably related
to a genome within the sample based on the "hammer-hits" that are found
within the sample.
This consensus is built by requiring hammer-evidence from more than one SOUR before we declare that a RepGen has sufficient support to be related
to a genome within the sample.
You can think of this "consensus process" as analogous to assembling
a "jury" made up of multiple SOURs,
with the set of scores for each role acting as "votes" to determine 
which RepGens provide the strongest evidence
for the presence of a related genome within the sample.
For instance, if we have hammers derived from sequences implementing 5 different SOURs, we can stipulate
that a RepGen must have support from at least
4 out of the 5 SOURs to be considered related to a genome within the sample.
This requirement for multiple lines of supporting evidence
mirrors the scientific process, where experiments are not deemed valid unless their results can be reproduced.

You may perhaps be wondering why we have specified "4 out of 5 roles".
The "4 out of 5" criterion is closely related to how we originally determined the set of SOURs that we use.
When we first introduced the concept of a "SOUR" in `RepGen-Exercise-1`,
we defined a "Singly-Occuring Universal Role" in the abstract as a role that can be _expected_ to be implemented
by exactly one gene in every genome, but we did not discuss how we
constructed this set of roles in practice.
During the actual construction of the SOURs, we found that it was
necessary to slightly weaken the concept of a "Universal role"
to "Role that is found in 80% of the members
of our Universe of Genomes". This weakening was required because
the technologies of genome-sequencing, genecalling, and gene-annotation
all have low but nonzero error-rates, and so some of the members
of the Universe of Genomes appear to be "missing" roles
that we expect to be there merely because of the nonzero error-rate
of our sequencing and annotation technology.
We have found that in practice, requiring a role to be present
in at least 80% of the members of our "Universe of Genomes"
appears to be a reasonable compromise for defining "Universality",
and therefore it is reasonable to require that before a RepGen is asserted
to have a close relative within a sample, the sample must have
hammer-hits from that RepGen for at least 80% of the roles in our list of SOURs.



## Materials

```
FIG-Bioinformatics-Course/
├── 2_Hammers
│   └── 2.2_Hammers-Using-More-Than-One-Role/
│       └── Multirole-Hammer-Sets-Exercise-1_Using-Multiple-SOURs.md (you are here)
├── Code/
│   ├── fasta_reader.py
│   └── filter_hammer_candidates.py
└── Data/
    ├── five_roles.tbl
    ├── myrep10.genomes.tbl
    ├── myrep50.genomes.tbl
    ├── Myrep10_Genomes/
    │   └── (141 genome contig-FASTAs)
    └── Myrep50_Genomes/
        └── (921 genome contig-FASTAs)
```

## Programs to be Generated

* get_seqs_for_roles_and_genomes.py

* hammer_creator_multirole.py


## Exercises

### 1. Getting the SOUR sequences

In this set of exercises you will be building hammers
based on the set of 5 roles contained in file `Data/five_roles.tbl`.
Your first task will be to fetch the sequences for these roles
from `BV-BRC`.

In `2_Hammers/2.1_Hammer-Creation-and-Application/Hammer-Exercise-1_Creating-Hammers.md`, you fetched the sequences for the PheS SOUR using a command-line pipeline.
While one could in principle just repeat this procedure
4 more times to get the sequences for the other 4 SOURs
used within this excercise, such a process
would be tedious and error-prone;
hence, it is better to ask Grimoire to automate fetching
the sequences that implement the specified set of roles
within the RepGens that you will be building hammers for.
As in previous exercises, you should first upload the file `Definitions.html` to Grimoire and ask it to learn the definitions
in the file without commenting on them.
Then, enter the following prompt to generate the automated sequence-fetcher:

```
Please write a python program named 'get_seqs_for_roles_and_genomes.py'
that accepts 3 mandatory named arguments.
The output from the '--help' argument should clearly indicate
that the program writes FASTA sequence-data to STDOUT.

* The three mandatory named arguments are:
  - A Type-flag, short name '-T', long name '--type',
    with allowed values of 'dna' or 'protein'.
    
  - The filename of a tab-separated-value list containing genome-IDs,
    short name '-G', long name '--genome-list'.

  - The filename of a tab-separated-value list of roles,
    short name '-R', long-name '--role-list'.

* The program should read the header-line of the role-name file,
and load the values in its 'role_name' column into a list.

* Foreach role in the role-list, print a progress-message to STDERR,
and then execute the following two commands, piping the output of 'cmd1'
to the input of 'cmd2', trapping any errors thrown by either command,
and printing the output of 'cmd2' to STDOUT;
note that the role can contain whitespace, and so this argument must be quoted:

   cmd1 = f"p3-get-genome-features --selective --input {genomes_filename} --col genome_id --eq product,'{role}' --attr patric_id"

   cmd2 = f"p3-get-feature-sequence --col feature.patric_id --{type}"

If either command fails, print the trapped error-message to STDERR, and then exit.
```

Ask Grimoire to generate pseudocode for its script if it has not done so,
then use VScode to paste the pseudocode and code into the template
`Code/get_seqs_for_roles_and_genomes.py` and save it as usual.

Because the sequence-fetching script calls two "P3 commands",
it will need to be run from within the BV-BRC app's command-window.
To run the command for your `myrep10` genomes, 
launch the BV-BRC app using the method appropriate
for your computer's operating-system as discussed in
earlier exercises such as `RepGen-Exercise-1`.
Recall that the BV-BRC app opens its command-line window
to your home-directory, so you will first need to switch
to the course-directory using the `cd` command.
(For example, if you installed the course-material
in your `Documents` directory, you would enter
`cd ~/Documents/FIG-Bioinformatics-Course`.)
Next, enter the following command into the BV-BRC window:

```
python Code/get_seqs_for_roles_and_genomes.py -T dna -G Data/myrep10.genome.tbl -R Data/five_roles.tbl > Data/myrep10.five_roles.dna-sequences.fna
```

This program will take some time to run,
but it should quickly start printing progress-messages
to the BV-BRC window to let you know that it's working.

### 2. Building the Hammers

Building hammers for a set of roles rather than a single role
will require a slight modification to the prompt you used in Hammer-Exercise-1;
the following revised prompt will generate the desired code:

```
Please write a python program named 'hammer_creator_multirole.py' that will:

* Accept as '-K' a mandatory integer Kmer-length command-line argument;
        
* Read a FASTA-formatted file from 'STDIN' using BioPython,
and foreach FASTA entry extract the following:

  - The portion of the FASTA header up to the first whitespace-character is the
  "feature-ID" ('fid') for the FASTA entry;
  the remainder of the FASTA header starting with the first non-whitespace character
  after the whitespace is that feature's "role".
  There may be more than one whitespace-character separating the feature-ID from its role.
  Please extract the feature-ID and the role frome the FASTA header,
  then convert the sequence to lower-case,
  and build dictionaries mapping feature-IDs to sequences,
  and feature-IDs to their roles.

  - Each feature-ID has the format 'fig|x.y.peg.z', where 'x', 'y', and 'z' are integers,
  and the 'fig|' and '.peg' portions are literal strings, not variables.
  The substring 'x.y' is the 'genome_id' for the feature;
  please use a regular expression to extract the genome-ID from the feature-ID,
  and build a dictionary mapping feature-IDs to genome-IDs. 

  - Return the dictionary mapping feature-IDs to genomes,
  the dictionary mapping feature-IDs to roles,
  and the dictionary mapping feature-IDs to sequences.

* Print a tab-separated header-line to STDOUT, whose column-names are
  "hammer", "fid", and "role".

* Create an empty "dictionary of dictionaries" whose outer-keys will be Kmers,
  inner-keys will be feature-IDs, and inner-values will be integer counts.

* Foreach sequence, find all of its Kmers, and foreach Kmer
  increment the count for that sequence's feature-ID
  in the dictionary-of-dictionaries.

* A "hammer" is defined as a Kmer that occur exactly once in exactly one genome-ID.
  Each feature-ID can only occur in one genome.
  So if a Kmer occurs with a count of '1' in exactly one feature, 
  then it must be a "hammer".
  Find all of the "hammers" in the dictionary-of-dictionaries,
  and print to STDOUT a three-column table table of "hammer", "feature-ID",
  and "role" for that feature-ID, sorted by hammer.

* Finally, please print to 'STDERR' the number of sequences that were read,
  the number of Kmers that were processed, and the number of Kmers that were hammers,
  then exit.
```

Again use VScode to paste the pseudocode and code into the template
`Code/hammer_creator_multirole.py` and save it.

To run the command for your 'myrep10' genomes, enter the following:

```
    python Code/hammer_creator_multirole.py -K 20 < Data/myrep10.five_roles.dna-sequences.fna > Data/myrep10.five_roles.hammers.tbl
```


## Self-Check

### Exercise 1.

To do a quick check that the correct set of DNA sequences
have been fetched from BV-BRC, run them through the program
`fasta_reader.py` that you created in `FASTA-Exercise-3`:

```
python Code/fasta_reader.py < Data/myrep10.five_roles.dna-sequences.solution.fna > /dev/null
```

The result printed to `STDERR` should be:

```
Number of sequences: 705
Average sequence length: 1823.90
```

Note that "705 sequences" is consistent with fetching
5 roles each for 141 genomes.

**NOTE:** In the above command, you are redirecting the data sent to `STDOUT` to a special "device" called `/dev/null`.
`/dev/null` is a program that silently "eats" any input
that isa sent to it;
if you had left off the `> /dev/null` portion of the command,
you would have seen the names and lengths of all 705 sequences in the FASTA file
before seeing the summary-statistics sent to `STDERR`.
`/dev/null` is useful when you do *not* want to see or save
output from a program for some reason.



### Exercise 2.

The number of lines in the file `Data/myrep10.five_roles.hammers.tbl` should be 1259712;
you can check this as follows:

```
wc -l Data/myrep10.five_roles.hammers.tbl
```

Recal that `wc` (short for "word count") is the command
that counts the number of characters, words, and lines in a file,
and that including the `-l` option tells the program
to only returns the number of lines, not the number of characters and words.

For completeness, we have included solutions-files
for the fetched sequences, the sets of hammers,
and the sets of filtered hammers
in the `Solutions/` subdirectory for this module,
however they are in `gzip-compressed form`
because they were too large to upload to GitHub,
so in order to look at them you will need to "uncompress" them.
gzip-compressed files can be uncompressed from the command-line
by using the `gunzip` command;
however most operating-systems support uncompressing
a commpressed file simply by "double-clicking" on them
in your file-browser.

We have also included solution "hammer-hits" files
for each of the test-cases in this exercise.
