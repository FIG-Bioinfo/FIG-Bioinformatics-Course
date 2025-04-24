# Hammer Exercise 4 - Hammer Quality-Control

**Objective:** Filter out candidate hammers that also occur elsewhere within the complete sequences of a RepGen genome
besides the SOUR that the candidate came from.

So far, we have looked for hammer candidates only within the PheS SOUR sequences from our set of Representative Genomes.
However, PheS is just one gene, about 1000 base pairs long,
while a typical bacterial genome contains thousands of genes
and spans millions of base pairs.
A Kmer found only once in one representative genome when analyzing
just the PheS SOUR sequences might appear more than once
when considering the complete contig sequences for the same set.
Since a hammer must be unique to a single RepGen and occur only once within it,
we must recheck the hammer candidates to eliminate any that occur
more than once within the set of representative genomes.
We may view removing these multiply-occuring candidates
as a "filtering operation" on the set of candidate hammers.

## Materials

(Insert directory-tree here)

## Exercises

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then go to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

### Generating the filter program

By definition, a hammer must occur exactly once
in a single representative genome,
and that occurrence must be within a SOUR gene.
Since we identified hammer candidates using only the selected SOUR sequences,
we need to verify them against the complete set of contig sequences
for the RepGen set.
If a hammer candidate is still unique after checking all the contigs,
it is a valid hammer.
However, if additional occurrences are found,
it fails to meet the hammer definition and must be discarded.
This process of verification can be thought of as "filtering."

To verify the hammer candidates, we first load them into a dictionary.
For each genome in the RepGen set, we scan the Kmers in its contigs
and check if they match any candidate in the dictionary.
If a Kmer within the dictionary is found more than once within the contigs,
then it fails to satisfy the definition of a hammer and should be removed.
After scanning all contigs, the remaining entries within the dictionary
are valid hammers, which we then save to an output file.

Each genome's contigs are stored as a FASTA file
with name-format `genome_id.fna` within a designated directory.
Hammer candidates are input from `STDIN` and stored in a dictionary.
We then iterate through the genomes in the directory,
checking their Kmers against the dictionary and discarding any candidates
that appear more than once within the contigs.
Once all genomes are processed,
the valid hammers remaining in the dictionary are output to `STDOUT`.

(It may be helpful at this point to go back and review the interactive exercise on adding and deleting dictionary entries 
in `TSV-Exercise-2_Python-Datatypes` before continuing with this exercise.)

Here is a prompt that will generate the algorithm we described above:

```
Please write a python program named 'filter_hammer_candidates.py' that:

* Accepts a mandatory directory-name argument for a directory
containing a set of FASTA contig files, short name '-D',
long name '--contigs-directory'.

* Reads a hammer-candidate file as a tab-separated-value file from STDIN,
saves the header-line, and loads the remainder of the file into
a dictionary called the "hammer dictionary",
with the first field as the key, and the entire line as the value.
The keys are named "hammer candidates"; note that all hammers have the same length.
The hammer read-function should return the number of candidates read,
the hammer-length, the header-line, and the hammer-dictionary.

* Reads the contents of the contigs directory.

* Foreach file in the contigs directory,
print the progress-message f"Processing '{filename}'" to STDERR,
where 'filename' is the name of the file, 
and then use BioPython to read the file as a set of 
FASTA-formatted DNA contigs.

* Foreach contig, convert the contig-sequence to lower-case,
and find all Kmers with length equal to the hammer-length
on both the forward and reverse-complement sequences.

* For each Kmer extracted from the contig and its reverse-complement:
  - Check the hammer-dictionary to see if that Kmer is a hammer candidate,
  
  - If the Kmer is a hammer candidate, increment the count for that Kmer
    in the candidate-count dictionary.
    
  - If the count for a candidate exceeds '1', delete that candidate's entry
    from the hammer dictionary, and increment a count of the number
    of candidates eliminated.

* Print the saved header-line to STDOUT, sort the remaining keys
in the hammer-dictionary (now called "Accepted hammers"),
and then foreach accepted candidate in the hammer-dictionary,
print its value to STDOUT.

* Finally, print a blank line to STDERR,
then the number of candidates read,
the number of candidates eliminated,
and the number of hammers accepted, and exit.
```

Ask Grimoire to generate code from this prompt, and then use VScode to save it as usual.

### Generating the Contig-Fetching Program

Before we can run the filter, we will need to fetch the contigs for your RepGen from BV-BRC. While it is possible to do this task
directly from the command-line, doing so would require more
knowledge of the command-line syntax than you may currently have.
Fortunately, we can sidestep this problem by asking Grimoire
to code the task for us! :-)<br>
The following prompt will do the job:

```
Please write a python program named 'get_contigs_for_genomes.py' that:

* Accepts the following two named arguments
  - Filename of a tab-separated-value list containing genome-IDs
    short name '-G', long name '--genome-list'

  - Name of an output directory, short name '-D',
    long-name '--output-data'

* Reads the genome-ID file, skips the header-line,
and loads the remainder of the first column into a list.

* Creates the output directory if it does not already exist,
  else warns the user and exits.

* Foreach genome-ID in the genome-list, prints a progress-message to STDERR,
and then executes the command described by the following format:

   f"p3-genome-fasta --contig {genome_ID} > {Output_Directory}/{genome_ID}.fna"

If the command fails, print an error-message to STDERR, and then exit.
```

Please ask Grimoire to also generate code from this prompt,
and then again use VScode to save it as usual.
We are now in a position to fetch your genome contigs.

### Fetching the Contig-Data

To fetch the contigs, you will need to run the contig-fetching program
that Grimoire generated for you from within the BV-BRC app's window,
not VScode.
Also, please remember that the BV-BRC app
opens its window within your home-directory,
so you will first need to change directory
to the course directory.

```
python3 Code/get_contigs_for_genomes.py -G Data/myrep10.genomes.tab -D Data/Myrep10_Genomes
```

(Again, remember that all of the above should be entered on a single line, even if it looks like it's wrapped across multiple lines on your screen.
also, please note that inside the BV-BRC app, it is necessary to specify
the `python3` interpretor, because the BV-BRC app defaults to `python version 2`,
not `python version 3`.)

The genome-fetching process will take some time,
but every few seconds or so you should see a progress message
indicating which genome is currently being fetched.


### Filtering the Hammers

Once you have your set of genome contigs,
it's time to run the filtering program:

```
python3 Code/filter_hammer_candidates.py -D Data/Myrep10_Genomes < Data/myrep10.PheS.hammers.tbl > Data/myrep10.PheS.hammers.filtered.tbl
```
(Again, beware line-wrapping!)

The filtering program will once again take some time,
but it should print a progress-message every few seconds
to let you know that it's running.

Congratulations! You should now have a guaranteed-valid set of hammers!<br>
(See the "Self-Check" for how to confirm your results.)


### How Filtering has Improved the Hammers

To see how filtering the hammers has improved their quality,
let's repeat the tests in `Hammer-Exercise-2` and `Hammer-Exercise-3` using the filtered hammers.

#### Reanalysis of MysteryGenome1

```
python Code/hammer_compare.py -H Data/myrep10.PheS.hammers.filtered.tbl -G Data/myrep10.genomes.tbl < Data/MysteryGenome1.fna > Data/MysteryGenome1.myrep10.filtered_PheS_hammer_report.tbl
```

You will find upon opening the hammer-report that
the hits from the three low-scoring "noise" genomes
have been completely eliminated,
leaving only the hit against the correct genome, 511145.12 *E. coli*. The score for *E. coli* has decreased slightly,
from 898 to 878, but now its signal has become completely clear.

Similarly, producing a hammer-report for `MysterySample1.fna`
using the filtered `MyRep10` hammers reduces the number of "noise" hits
from 8 genomes to 3, while only slightly decreasing the score for the real genomes.


### Bonus Exercises

Repeat the contig-fetching process and filtering process
for the `myrep50` RepGen set. 
Note that `myrep50` is about 10 times larger that `myrep10`,
so everything is going to take longer.
Then apply the filtered `myrep50` hammers to `MysteryGenome1`
and `MysterySample1` to see how their reports have changed
compared to Exercises 2 and 3.


## Self-Check

To make a quick check that the genome-fetching process ran correctly,
you can execute the following command:

```
ls -1 Data/Myrep10_Genomes/ | wc -l
```

`ls -1` means "List the contents of the directory in single-column format";<br>
we then pipe the results to `wc -l`, which means "Count the number of lines".<br>
The directory for `myrep10` should contain 141 genomes,
while the directory for `myrep50` should contain 921 genomes.

Filtering the `myrep10` hammers should print the following last three lines to `STDERR`:

```
Candidates read: 148751
Candidates eliminated: 1522
Hammers accepted: 147229
```

Note that only about 1% of the candidates were rejected,
because the `myrep10` genomes are fairly far apart
and therefore have few Kmers in common to begin with.
Nevertheless, we see a dramatic improvement in reported results
after filtering, since all of the non-*E. coli* hits for `MysteryGenome1`
have now been eliminated, with only a 2% decrease in the score for *E. coli*.

Filtering the `myrep50` hammers should print the following last three lines to `STDERR`:

```
Candidates read: 903835
Candidates eliminated: 40286
Hammers accepted: 863549
```

Note that this time nearly 4.5% of the candidates have been eliminated;
this is because the `myrep50` genomes are closer together than the `myrep10` genomes,
and therefore have a greater chance of having Kmers in common.
But again, eliminating the few candidates with occurrences
outside the SOUR has dramatically decreased the number of "noise"
hits---from 51  down to just 15 in the case of `MysterySample1`.

