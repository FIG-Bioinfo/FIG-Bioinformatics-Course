# RepGen Exercise 2 - Finding the nearest RepGen

Objective: Fetch the PheS for a "Mystery Genome" from the [Bacterial and Viral Bioinformatic Resource-Center (BV-BRC)](https://www.bv-brc.org/), and find out which Representative Genome it is closest to.

## Materials

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

[The BV-BRC Toolkit](https://www.bv-brc.org/docs/cli_tutorial/index.html)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── 1.4_Building-Representative-Sets/
│       └── RepGen-Exercise-2_Finding-the-nearest-RepGen.md (you are here)
├── Code/
│   └── find_nearest_reference.py 
└── Data/
    └── myrep10.faa
```

## Overview:

In research and medicine, we will often be confronted with a genetic sample that contains one or more unidentified genomes.
We can gain knowledge about which genomes are present within a sample by comparing the sample to a "Set of Representative Genomes" (RepGen Set).
The set `rep200` is our highest-resolution "production" RepGenSet; it allows identification of genomes down to the "species" level. Similarly, `rep100` allows identification down to the "Genus" level.
Our coarsest set of "production" representatives is `rep10`, which allows identification to within broad families of genomes.

The "production" RepGenSets generated by FIG were built from the BV-BRC collection of nearly a million genomes, which represent far too much data to be distributed in this course. Hence, for this and subsequent exercises, you will instead be using the `myrep10` and `myrep50`
that you built from `Universe.fasta` in the previous exercise 
instead of the "production" versions generated by FIG.

In this exercise, you will also be using the `BV-BRC Command-Line Interface` application (`BV-BRC CLI`, also referred to as the "P3 Commands" for historical reasons), which will allow you to fetch the data and metadata for nearly a million sequenced genomes.
You will use the CLI to fetch the PheS sequence from a "Mystery Genome" and then compare it to the `rep200` data using the tool `find_nearest_reference.py` that you constructed in Kmer-Exercise-3. You will then fetch the actual biological name of the "Mystery Genome" from BV-BRC and compare it to the biological name of nearest representative genomne that your tool selected.

## Exercises:

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then go to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. Please install the `BV-BRC Command-Line Interface` application if you have not already done so.
Instuctions for installing the BV-BRC app are located in `O_Getting-Stated/0_Installing-the-BV-BRC-app`.


2. Get the PheS sequence for "Mystery Genome-ID 562.66554" using the following incantation inside of the BV-BRC CLI. If installed correctly, you should be able to also run the command in the Gitbash terminal in VSCode in your normal root directory:
```
    p3-echo PheS | p3-find-features --attr patric_id,product --eq genome_id,562.66554 gene | p3-get-feature-sequence --col feature.patric_id > Data/mystery_PheS.faa
```
(Again, remember that the above command should be pasted in as a single line, even though it may appear to wrap around onto several lines on the screen.) We will break down this complex command later in this exercise.

3. Use your command `find_nearest_reference.py` to compare the sequence you just fetched to `myrep10`:
```
    python Code/find_nearest_reference.py -K 8 -R Data/myrep10.faa < Data/mystery_PheS.faa
```
Which representative genome was reported in the RepSet-description column?

4. Now let's find out the true identity of the "Mystery Genome":
```
    p3-echo 562.66554 | p3-get-genome-data --attr genome_name
```
Does the "Mystery Genome" have the same genus and species (first and second name) as the RepGen genome that `find_nearest_reference.py` found?<br>
Congratulations! You have correctly identified the genus and species of the "Mystery Genome"!

The above is a greatly simplified "cartoon version" of how one may go about identifying a completely new genome using a RepGen Set. The actual real-world procedure is more involved; one would first need to sequence and "assemble" the mystery-genome, annotate its genes, extract the sequence for the "Mystery PheS", and then perform the sequence comparison, but the basic concept is the same.

In a later exercise, you will learn about a type of "Genetic Barcode" called a "Hammer", which allows one to skip the intermediate steps and go directly from raw sequencer-data to a genome identification.

## Breaking down the steps in the "P3 incantation"

Earlier, we used the following "incantation":
```
p3-echo PheS | p3-find-features --attr patric_id,product --eq genome_id,562.66554 gene | p3-get-feature-sequence --col feature.patric_id > Data/mystery_PheS.faa
```
The above complex command is an example of a "command pipeline".
A "command pipeline" is a sequence of commands plus modifying arguments that are separated by the symbol `|`; this symbol is pronounced as "pipe" because it connects (or "pipes") the `STDOUT` from one command to the `STDIN` of the following command.
You can use a "pipeline" to construct an arbitrarily complex command or filter operation out of simple commands.
Let's break the above incantation down step-by-step to see what it does.

1. The first step is `p3-echo PheS`. If you type this command by itself, you will see the following output:
```
id
PheS
```
The above illustrates three points:
* P3-commands all generate "Tab-separated output with a header-line", which is sent to `STDOUT`. 

* the `p3-echo` command accepts one or more values as arguments,
and "echoes" them one after the other following the column-name.
The utility of `p3-echo` is to create TSV data that will be sent
to subsequent P3-commands

* In the absence of an argument, `p3-echo` uses a "default" column-name of `id`. In cases where a different column-name is required, it can be specified using the `-t` argument (which you may think of as short for "column-title"), so for example:
```
p3-echo -t feature_id 'fig|562.66554.peg.2184'
```
will generate:
```
feature_id
fig|562.66554.peg.2184
```
It is possible (but cumbersome) to generate multiple-column TSV files using `p3-echo`, but this capability is rarely needed. Most often, you will use `p3-echo` to create single-column output as follows:
```
p3-echo -t columnName value1 value2 value3
```
which results in:
```
columnName
value1
value2
value3
```

2. The next step is to "pipe" the output of `p3-echo` to the input of `p3-find-features` as follows:
```
p3-echo PheS | p3-find-features --attr patric_id,product --eq genome_id,562.66554 gene
```
which produces:
```
id	feature.patric_id	feature.product
PheS	fig|562.66554.peg.2184	Phenylalanyl-tRNA synthetase alpha chain (EC 6.1.1.20)
```
Note that the output has acquired two new columns named `feature.patric_id`	and `feature.product`; the portion of the column-heading in front of the dot specifies the `type` of the data-column (which in this case is `feature`), while the portion after the dot specifies an "attribute" of the data-type that was selected within the command using the argument `--attr patric_id,product`. Note that more than one attribute of a data-type can be selected by using a comma-delimited list of attributes.

The above mechanism of appending new columns to the end of each line of an input file allows us to incrementally build up arbitrarly complex data-tables using a sequence of P3-commands. 

3. The final step is:
```
p3-echo PheS | p3-find-features --attr patric_id,product --eq genome_id,562.66554 gene | p3-get-feature-sequence --col feature.patric_id
```
which yields:
```
>fig|562.66554.peg.2184 Phenylalanyl-tRNA synthetase alpha chain (EC 6.1.1.20)
MRQKLEDIKNSAINELKTTLSKDQLEAIRVKYLGKKGELTQILRGMGALSQEERPIVGKVANEVRSYIEETIKEAFSDIKNKEKSIRLENETIDITMPGKKQAVGKRHPLDLTLESMKDIFISMGFTIEEGPEVELDKYNFEALNIPKNHPARGEQDTFYINDNLVLRTQTSPIQIRTMENQKPPIKMIAPGKVYRSDSVDATHSPIFYQMEGLVVDKGITFSDLKGTLELFAKRMFGDKVKTKFRPHHFPFTEPSAEMDATCFVCNGEGCKVCKGSGWIELLGCGMVHPQVLRNCNIDPEVYSGFAFGFGVDRMVMMKYGIDDIRLLYESDMRFLNQF
```
The above step illustrates a final point, which is that in general
most P3-commands will select one of the columns (and by default, usually the last column) to use as the "key" to look up the specified set of data-values, and the "key" column-name
can be explicitly specied using the `--col` (short for "column") command-argument. In this case, we used `--col feature.patric_id` to specify that the
`feature.patric_id` column-value should be used as the data lookup-key
that will be used by `p3-get-feature-sequence`.

As previously noted, in the absence of a `--col` argument, P3-commands default to using
the _last_ column of their input-table as their current "key", which often simplifies incrementally building up an arbitrarily complex table by using the last attribute looked up as the "key" to look up the next data-item.

Finally, note that every P3-command accepts a `--help` argument
that will list and describe the arguments that the command accepts,
and that most commands also accept a `--fields` argument that lists
the data-attributes that they can access.

A detailed tutorial on how to use P3-commands can be found at:<br>
https://www.bv-brc.org/docs/cli_tutorial/cli_getting_started.html

A catalogue of the P3-commands may be found at:<br>
https://www.bv-brc.org/docs/cli_tutorial/command_list/index.html<br>
Clicking on a command-name will go to the `--help` output for that command.

