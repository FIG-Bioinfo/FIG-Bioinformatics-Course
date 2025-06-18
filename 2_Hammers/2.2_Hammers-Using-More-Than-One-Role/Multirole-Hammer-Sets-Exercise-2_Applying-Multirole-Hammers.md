# Multirole Hammers - Applying Multirole Hammers

**Obejective:** Using the set of multirole hammers created in
`Multirole Hammer Exercise 1` to obtain more reliable RepGen assignments
by requiring a "consensus" among the sets of assignemnts made by each SOUR.

In this excercise, we will see that the "noise hits"
can be largely or even completely eliminated by requiring
a "consensus" on which genomes are present within a sample
based on hammer evidence from more than one SOUR. 
You may think of this consensus-building process as being analogous
to forming a "jury" composed of several different SOURs,
and considering their scores to represent "votes"
on which RepGens are closest to the genome or genomes within a sample.
For example, suppose that we have built hammers using sequences
implementing 5 different Singly-Occuring Universal Roles;
we can require that in order for a RepGen to be asserted
to be "close" to some genome within the sample, it must have support
from at least 4 out of the 5 SOURs. Such a requirement of support
from multiple lines of evidence is fundamental to the scientific process;
for example, we do not consider an experiment to be valid unless
it can be reproduced.

## Materials

```
FIG-Bioinformatics-Course/
├── 2_Hammers
│   └── 2.2_Hammers-Using-More-Than_One-Role/
│       └── Multirole-Hammer-Sets-Exercise-2_Applying-Multirole-Hammers.md (you are here)
├── Code/
└── Data/
    ├── myrep10.genomes.tbl
    ├── myrep50.genomes.tbl
    ├── myrep10.five_roles_hammers.tbl
    ├── myrep50.five_roles_hammers.tbl
    ├── MysteryGenome1.fna
    └── MysterySample1.fna
```

## Programs to be Generated

* hammer-compare_multirole.py

## Using the Hammers

1. The hammer-application program also needs revision to support multiple roles;
the following prompt will do it:

```
Please write a program named `hammer_compare_multirole.py` that will:

* Accept a mandatory TSV "hammers" filename argument,
short name `-H`, long name `--hammers`.

* Accept a mandatory TSV genome-names filename argument,
short name `-G`, long name `--genome-names`.

* Accept an optional "minimum fraction of roles required" argument,
short name `-F`, long name `--role-fraction`, default-value 0.8.

* Open the hammer-file and perform the following:
    
    - Read the header-line and extract the column-names
    
    - Foreach subsequent line, read the "hammer" and "fid"
    columns as `hammer` and `feature_id` variables,
    respectively, and built a dictionary mapping
    hammers to feature_ids.

    - If a "role" column exists, read it as the `role` variable,
    else the role should default to "Unknown",
    and build a dictionary mapping feature_ids to roles.

    - A `feature_id` has the format 'fig|x.y.peg.z',
    where 'x', 'y', and 'z' are integers, and 'fig|' and '.peg.'
    are literal substrings; the portion 'x.y' is the `genome_id`
    for that 'feature_id'. Extract the `genome_id` from the `feature_id`
    using a regex, and build a dictionary mapping feature_id to its genome_id.

    - Determine the Kmer-length `K` of the hammers.
    (NOTE: all the hammers in the file will have the same length.)

    - Return the hammer-length `K`, the list of roles,
    the hammer-to-feature_id dictionary,
    the feature_id-to-genome_id dictionary,
    and the feature_id-to-role dictionary

* Open the 'genome-names' file, skip the header-line,
and for subsequent lines read the first and second columns
into a dictionary as a `genome_id` and `genome_name`, respectively;
then return the genome_id-to-genome_names dictionary.

* Create an empty directory whose keys will be genome-IDs,
and values will be an integer count of the number of hammers
found for that genome.

* Create an empty "dictionary of dictionaries" whose outer-keys will be genome_ids,
inner-keys will be roles, and inner-values will be the integer count
for the number of hammers found for that role in that genome.

* Use BioPython to read the sequences of the genome from `STDIN`;
the sequence should then be converted to lower-case.

* For each sequence, extract all possible Kmers, and if a Kmer
is a hammer, increment the hammer-count for its associated `genome_id`
in the genome-counts dictionary, and also the hammer-count for that role
in the genome-to-role-to-counts directory-of-directories;
then repeat this operation on the reverse-complement of that sequence,
since a gene can face in either direction.

* Once all the sequences have been processed,
foreach genome_id in the genome-to-roles-to-counts directory
of directories, if the number of roles for that genome
is greater than or equal to the total number of roles
times the minimum fraction of roles,
print to STDOUT a TSV file of the genome_ids found
and their associated genome_name and score,
sorted by decreasing genome-to-counts score.
If the total number of roles exceeds 1,
also add a column for the number of roles for the genome.
Please handle missing genome-names gracefully;
if a genome_id does not have an associated genome-name,
display the genome_name as 'Unknown sp.' in the output TSV file,
and send a warning to STDERR that the name of genome_id was not in 
the genome-names file.
```

Upload the `Definitions.html` file to Grimoire as in previous exercises, and the ask Grimoire to generate code and pseudocode for the above prompt.
Then using VScode, paste the prompt, pseudocode, and code into the code-template for `hammer_compare_multirole.py` and save it as usual.


2. To run the program on `MysteryGenome1.fna`, enter the following:

```
python Code/hammer_compare_multirole.py -H Data/myrep10.five_roles.hammers.tbl -G Data/myrep10.genome.tbl < Data/MysteryGenome1.fna > Data/MysteryGenome1.myrep10.five-role-hammers-hits.tbl
```

The resulting output table is:

| Genome_ID | Genome_Name | Score | Roles_Found |
| --- | --- | --- | --- |
| 511145.12 | Escherichia coli str. K-12 substr. MG1655 | 8257 | 5 |

Recall that in `Hammer-Exercise_1`, the program `hammer_compare.py` found several low-scoring "noise genomes" in addition to the correct RepGen `511145.12`, and that in order to remove the "noise hits" we had to "filter" the hammers to remove candidates that had additional occurances outside the SOUR sequences. However, using multirole hammers and requiring at least 4 out of 5 roles to be found before we will accept a RepGen hit, the program returns only correct RepGen and no "noise genomes" even without filtering!
So requiring multiple confirming-evidences for a RepGen does appear to eliminate the "noise problem", even without "filtering". 

3. We can confirm the above claim by rerunning the program
with the minimum role-fraction set to 0
so that all hits will be accepted:

```
python Code/hammer_compare_multirole.py -H Data/myrep10.five_roles.hammers.tbl -G Data/myrep10.genome.tbl -F 0.0 < Data/MysteryGenome1.fna > Data/MysteryGenome1.myrep10.five-role-hammers-hits.no-threshold.tbl
```

The output-file contains 35 lines (34 hits plus the header-line);
the top 5 hits are:

| Genome_ID | Genome_Name | Score | Roles_Found |
| --- | --- | --- | --- |
| 511145.12 | Escherichia coli str. K-12 substr. MG1655 | 8257 | 5 |
| 1637999.4 | Verrucomicrobia bacterium IMCC26134 | 4 | 1 |
| 2024963.9 | Caldimicrobium sp. strain SpSt-122 | 3 | 1 |
| 1062.102 | Rhodobacter sp. strain HK-STAS-PROT-59 | 3 | 2 |
| 309798.4 | Coprothermobacter proteolyticus DSM 5265 | 3 | 1 |

Note that the low-scoring "noise genomes" only had hits for 1 or 2 roles, confirming that requiring a "4 out of 5 jury" eliminates the "noise hits", even without "filtering". The lower-ranking hits are all score 3 hits or lower and only score against a single role, so they have been eliminated by the "4 out of 5" jury-mechanism.


## Self-Check

2. Since the hammer-hits table only contains a single entry
that was displayed in full within the exercise,
no solution-file has been provided.

3. The solution-file for the `-F 0.0` test is named:
`MysteryGenome1.myrep10.five-role-hammer-hits.no-threshold.solution.tbl`
