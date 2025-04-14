# Hammer Exercise 2 - Using Hammers to find the Nearest Representative

Objective: Given a set of representative genomes,  a set of associated "Hammers", and an unknown genome, determine which representative the unkonwn genome is most similar to.

In this exercise we will generate code that will search a "Mystery Genome" to see if it contains any "hammers". If the "Mystery Genome" contains many of the same "hammer" barcodes as one of the representative genomes, and very few "hammers" for any other representative genome, then this indicates that there is a high probability that the "Mystery Genome" and the representative genome that contributed the largest number of "hammer hits" are related.

## Materials

```
FIG-Bioinformatics-Course/
├── 2_Hammers 
│   └── 2.1_Hammer-Creation-and_Application/
│       └── Hammer-Exercise-2_Using-Hammers-on-Genomes.md (you are here)
└── Data/
    ├── MysteryGenome1.fna
    ├── myrep10.PheS.hammers.tbl
    └── myrep10.genomes.tbl
```

## Exercises

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. We need to compare the DNA sequences in `MysteryGenome1.fna`
to the set of hammers that you generated in the previous exercise.
Ask Grimoire to write a program named `hammer_compare.py` that will:

    * Accept a mandatory TSV "hammers" filename argument,
    short name `-H`, long name `--hammers`.

    * Accept a mandatory TSV genome-names filename argument,
    short name `-G`, long name `--genome-names`.

    * Skip the header-line of the hammer-file and then read
    the first and second columns as a `hammer` and `feature_id`,
    respectively. A `feature_id` has the format 'fig|x.y.peg.z',
    where 'x', 'y', and 'z' are integers, and 'fig|' and '.peg.'
    are literal substrings. The portion 'x.y' is the `genome_id`
    for the 'feature_id'; extract the `genome_id` using a regex,
    and build a dictionary mapping each hammer to its genome_id.

    * Skip the header-line of the genome-names file and then read
    the first and second columns into a dictionary as a `genome_id`
    and `genome_name`, respectively.

    * Determine the Kmer-length `K` of the hammers from the hammers dictionary.
    (NOTE: all the hammers in the file will have the same length.)

    * Use BioPython to read the sequences of the genome from `STDIN`.

    * For each sequence, extract all possible Kmers, and if a Kmer is a hammer,
    increment the score for its associated `genome_id`; then repeat this operation on the reverse-complement of that sequence, since a gene can face in either direction.

    * Print to STDOUT a TSV file of the genome_ids found
    and their associated genome_name and score
    sorted by decreasing score.
    Please handle missing genome-names gracefully;
    if a genome_id does not have an associated genome-name,
    display the genome_name as 'Unknown sp.' in the output TSV file,
    and send a warning to STDERR that the name of genome_id was not in
    the genome-names file.
    
Finally, please ask Grimoire to translate the python code into pseudocode.

2. Once Grimoire is done, please paste its pseudocode and code into `Code/hammer_compare.py` and save it as usual.

3. Run your script on the `MysteryGenome1.fna`:

```
python Code/hammer_compare.py -H Data/myrep10.PheS.hammers.tbl -G Data/myrep10.genomes.tbl < Data/MysteryGenome1.fna > Data/MysteryGenome1.hammer_report.tbl
```

The result should be a table of representative genome-IDs and their names followed by how many hammers from that representative hit the "Mystery Genome". Take the genome-ID with the top number of hits as the most probable representative for the "Mystery Genome".


Congratulations! You have used the set of hammers you constructed for the PheS SOURs in the `myrep10` set of representative genomes to identify the `myrep10` genome `511145.12` as the most likely representative for your "Mystery Genome"!

## Caveats

In this exercise we have presented a greatly simplified "toy version" of the the hammer-creation process to illustrate the basic concepts behind hammers. The "production" version of the code is significantly more complex; we use the sequences for the 20 SOURs that we have found to yield the most reliably informative hammers, and we also cross-check the entire genome in addition to the SOUR sequences to make certain that the hammer does not occur somewhere else within the genome, since by definition a hammer can only occur once within one representative genome and must be contained within a SOUR. We have avoided these additional complexities within this exercise in order to keep this exercise simple, but in a later exercise, you will refine your prompt to take these additional complexities into account.

## Bonus Exercise

Run `hammer_compare.py` on `MysteryGenome1.fna` using the `myrep50` hammers. How does the output table change?

# Self Check

The `MysterGenome1.fna` should have `511145.12` "Escherichia coli str. K-12 substr. MG1655" as its highest-scoring representative genome:

## Scores using 'myrep10'

| genome_id | genome_name | score |
| --- | --- | ---: |
| 511145.12 | Escherichia coli str. K-12 substr. MG1655 | 959 |
| 1637999.4 | Verrucomicrobia bacterium IMCC26134 | 4 |
| 113566.3 | Actinoplanes humidus strain NBRC 14915 | 1 |

Note that while genome `511145.12` has by far the largest score,
there are very low scores against two other representative genomes.
There are two reasons for this:

* The farther a genome gets from a representative,
the more likely it is that it will be hit by a hammer from another representative.

* Because we are using a simplified version of hammer construction,
we only eliminated Kmers that occured in the `PheS` of another representative. In the "production" version of the hammer code,
we impose the stricter requirement that a hammer cannot occur **anywhere** in another representative genome, but checking for this
stricter condition would not only require more time and bookkeeping,
but would require that you have the complete sequence
for every representative genome, not just the sequences for
some set of SOURs --- and that would involve fetching more data
than we want to impose on you in this introductory course.

## Top 5 scores using 'myrep50'

If you did the bonus exercise, you should have found that
19 representative genomes were returned instead of 3 representativeas, 
and that `511145.12` is still the highest-scoring RepGen.
Here are the top 5 RepGens:

| genome_id | genome_name | score |
| --- | --- | ---: |
| 511145.12 | Escherichia coli str. K-12 substr. MG1655 | 898 |
| 1637999.4 | Verrucomicrobia bacterium IMCC26134 | 4 |
| 1008392.4 | Chitinispirillum alkaliphilum strain ACht6-1 | 2 |
| 476281.3 | Candidatus Ishikawaella capsulata Mpkobe | 2 |
| 2864219.3 | Hymenobacter sp. KCTC 23674 | 2 |

Note that the score for `511145.12` has dropped from 948 to 855;
this is because the larger the similarity-threshold for the RepGenSet,
the more representatives will be found (because allowing a higher maximum similarity means allowing a smaller distance between representatives), and the more likely it is that two representatives will have a Kmer in common, 
and hence the more Kmers will be eliminated from becoming "Hammers", because they were found in some other representative during the hammer-construction process (see the discussion at the end of `Hammer-Exercise-1`).