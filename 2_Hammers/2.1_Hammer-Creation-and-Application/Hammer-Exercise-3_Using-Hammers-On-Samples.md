# Hammers Exercise 3 - Using Hammers on a Metagenomic Sample

**Objective:** Use Hammers to estimate which genomes are present in a metagenomic sample by finding which representatives contributed hammers that hit the sample,
and how many hits each representative contibuted.

In the last lesson, we use a set of hammers to determine which representative an unknown "Mystery Genome" was closest to.

In this exercise, we will give you a sample containing multiple genomes.
Such mixed samples are often called "metagenomes".
By tabulating which representatives contributed hammers that hit this mixture of genomes, you will be able to estimate which genomes are present in the sample, in a process analagous to taking a "poll" or "survey" of the members of a population.


## Materials

```
FIG-Bioinformatics-Course/
├── 2_Hammers
│   └── 2.1_Hammer-Creation-and-Application/
│       └── Hammer-Exercise-3_Using-Hammers-on-Samples.md (you are here)
└── Data/
    ├── MysterySample1.fna
    ├── myrep10.hammers.tbl   (output from Hammer-Exercise-1)
    └── myrep10.genomes.tbl   (output from RepGen-Exercise-1)
```

## Exercises

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-windown if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. If necessary, please review your `Code/hammer_creator.py` tool
for its inputs and usage.
If you'd like, you can run it on `Data/MysteryGenome2.fasta`
to help review the workflow covered in the the previous lesson;
you can find the expected results below in the `Self-Check` section.

2. Next we will use this same process to find the hammer counts
for a "Mystery Sample" containing 3 genomes.
Run your `Code/hammer_compare.py` using the hammers from `myrep10`:

```
python Code/hammer_compare.py -H Data/myrep10.hammers.tbl -G Data/myrep10.genomes.tbl < Data/MysterySample1.fna > Data/MysterySample1.rep10.hammer-hits.tbl
```
* NOTE: The data-file for this exercise is about twice as large as `MysteryGenom1.fna`,
so it will take significantly longer to run.

To check your results, 11 RepGens should be returned;
see the `Self-Check` for a table of the Top 5 hits.

Note that 3 of the RepGens yielded more than 100 hits,
as expected for a sample
known to contain 3 genomes. However, also please note that 8 other representatives were reported (out of 141 genomes total within the RepGenSet),
albeit each with only a small number of hits.
We briefly discussed why such weak hits might exist in the previous exercise;
the existence of such hits illustrates the need for a minimum score-threshold
before we can be confident that a relative of a representative is present in a sample.

* BONUS:
Repeat exercise 2 using `myrep50`.

3. Currently you have only seen a few instances of how many hammers hit
a single genome or a sample containing multiple genomes.
You have seen that some representives hit a given genome or sample
with many hammers, while others hit only a few times,
and we have argued that the representatives that yield the largest number
of hits are most likely to be close relatives of a single genome
or a sample-member.
However, without the experience acquired by performing hammer-analyses
on hundreds of genomes or samples, it may be hard for one to form an accurate
picture of how many hammer-hits are needed to reliably infer that a close relative
of a representative is present in a sample.
Please upload the `Definitions.html` file to Grimoire as usual,
and then ask it to explain to you why a 20-character genetic-signature
such as a hammer might yield inaccurate or inconclusive evidence
for the presence of a close relative of a representative within a sample,
and how one might refine using signatures such as hammers to yield
more reliable inferences.

4. Tuning our hammers so that they only hit their intended targets is crucial
to having a useful tool. Without this, we might be casting a wider net
than necessary, resulting in hits from representatives that are not close,
or failing to find enough genomes to accurately analyze a sample.
Ask Grimoire to describe some ways
that we can tune our hammers to accurately characterize our genome space.

In the next unit, we will explore tuning the hammers to be more precise
and accurate by determining how "worthy" a hammer is,
i.e. how often it finds genomes that are close to its RepGen.
We will also discuss how to obtain supporting evidence for the presence
of a genome by requiring that the sample contain hits by hammers
from more than one SOUR from the same representative.

### Self Check

1. The refresher exercise of analyzing `MysteryGenome2.fna` using `myrep10`
should have returned 10 RepGens, with `29523.365 [Bacteroides sp. cpbc052018]`
as the top-scoring RepGen.

2. `MysterySample1.fna` using `myrep10` should also return 11 genomes;
here are the top 5 and their scores:

| genome_id | genome_name | score |
| --- | --- | ---: |
| 390333.7   | Lactobacillus delbrueckii subsp. bulgaricus ATCC 11842 | 1030 |
| 511145.12  | Escherichia coli str. K-12 substr. MG1655 | 840 |
| 206672.9   | Bifidobacterium longum NCC2705 | 691 |
| 1637999.4  | Verrucomicrobia bacterium IMCC26134 | 6 |
| 174633.135 | Candidatus Kuenenia stuttgartiensis GH-07nov19-223 | 5 |

Note that the top 3 RepGens received scores in the several-hundreds range,
while all the lower-ranking RepGens received scores that are less than 10.

* The Bonus exercise should have returned 55 RepGens;
here are the top 5:

| genome_id | genome_name | score |
| --- | --- | ---: |
| 390333.7  | Lactobacillus delbrueckii subsp. bulgaricus ATCC 11842 | 989 |
| 511145.12 | Escherichia coli str. K-12 substr. MG1655 | 789 |
| 206672.9  | Bifidobacterium longum NCC2705 | 632 |
| 1637999.4 | Verrucomicrobia bacterium IMCC26134 | 6 |
| 1314958.3 | Parachlamydiaceae bacterium HS-T3 | 6 |


Again, the same 3 RepGens received scores in the several hundreds,
while all the lower-ranking RepGens received scores of 10 or less.
