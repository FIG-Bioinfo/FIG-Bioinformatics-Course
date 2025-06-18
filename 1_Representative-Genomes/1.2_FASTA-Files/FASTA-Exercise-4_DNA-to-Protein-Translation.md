# FASTA Exercise 4 - DNA to Protein Translation

Objective: Learn how to translate DNA sequences into protein sequences.

We have mention that there are three fundamental types of biological sequences (DNA, RNA, and protein), and that each type of sequence has its own "alphabet". We will now learn how cells translate genes encoded in DNA to proteins that are composed of amino-acids.


## Materials: 

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   ├── 1.2_FASTA-Files/
│   │   └── FASTA-Exercise-4_DNA-to-Protein-Translation.md (you are here)
│   └── Solutions/
│       ├── translate-DNA_simple.solution.py
│       ├── translate-DNA_intermediate.solution.py       
│       ├── translate-DNA_biopython.solution.py
│       ├── Result1.simple.faa
│       ├── Result1.intermediate.faa
│       └── Result1.biopython.faa
├── Code/
│   └── translate-DNA.py
└── Data/
    └── Sample1.fasta
```

## Exercises:

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then go to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.


1. With only a few exceptions (most notably during the replication of "retroviruses" such as HIV), information in cells flows in one direction: From DNA, to RNA, to Proteins. This one-way flow of molecular information has become known as the "Fundamental Dogma of Molecular Biology". Ask Grimoire to explain this "Fundamental Dogma" to you in more detail. If Grimoire uses terms that are unfamiliar to you, ask it to explain those terms as well.

2. A protein-encoding DNA sequence is structured as a sequence of 3-character groups known as "codons". Each codon encodes a single amino-acid. Since DNA uses a 4-character alphabet, there are 4x4x4 = 64 possible codons, which map into 20 possible amino-acids plus a "STOP" signal indicating the end of the gene. Ask Grimoire to show you the mapping from DNA to amino-acids in Bacteria.

3. Ask Grimoire to explain in pseudocode how to translate from a DNA sequence into a protein sequence.

4. Ask Grimoire to write a program named `translate-DNA_simple.py` that reads a set of FASTA-encoded DNA sequences from STDIN, standardizes each sequence to uppercase, translates each sequence from DNA to protein, and writes the translated sequences in FASTA format to STDOUT.
Invalid codons should be translated as 'X'.

You will notice that there are several subsidiary conditions
in this prompt; why is that?

    * Computers are very "literal-minded"; they do not, for example,
    automatically recognize that an uppercase and lowercase sequence
    contain the same information. There is no guarantee that a given
    DNA file will be in uppercase rather than lowercase, and indeed
    your data-file `Sample1.fasta` is indeed in lowercase. Without
    standardizing the case, it is likely that the code will translate
    every codon as 'X' for "Unknown".

    * We specified that invalid codons should be translated as 'X',
    because that is the character that has been selected by the
    "Interntional Union of Pure and Applied Chemistry" (IUPAC),
    which sets standards for chemical and biochemical nomenclature
    so that chemists and biochemists all over the world will be
    "speaking the same language".

5. Use VScode to save the program to the `Code/` directory for this exercise.

6. Run the program on the file `Data/Sample1.fasta`:
    ```
    python Code/translate-DNA_simple.py < Data/Sample1.fasta > Data/Result1.faa
    ```
Note that we are recommending a file-extension of `.faa` to remind you that the translation is an Amino-Acid FASTA file.

Normally, there is something that outputs into the terminal when you run a program. In this case, the program outputs into a file. That means that if your program is working correctly, you should see the contents of `Data/Result1.faa` in the `Data/` directory and not in your terminal. Instead, the terminal should just show your mouse cursor blinking next to an empty line. If you want your program to output something into the terminal to tell you that it is done, add the following line of code to the end of your program.
```
print("Done!")
```
Feel free to customize this message to your liking. Half the fun is getting the computer to talk to you!


7. Check your output translation against the file `Solutions/Result1.simple.faa`.
We have also included the code that Grimoire generated as `Solutions/translate-DNA_simple.solution.py`.

8. Bonus 1: Real biology and bioinformatics contains many complications; here are two of them:

    * In bacteria and archaea, there are 3 different "START codons"
    that can begin a "genetic sentence" --- `ATG`, `GTG`, and `TTG`.
    Of these three, `ATG` is most common, and in eukaryotic lifeforms,
    `ATG` is the only "START codon" used.
    At the beginning of a protein, all three of these codons are
    translated as `M`, but in the "main body" of the protein
    they are translated as `M`, `L`, and `V` respectively.
    Grimoire exhibits a strong "eukaryotic bias", and tends to forget
    about the other two START codons, so we must remind it.

    * The 3 "STOP codons" are represented as `*`, but are not actually
    translated, they form the "period" that ends a "genetic sentence",
    and so by convention we do not include them in a translation.
    However the code that Grimoire wrote does indeed translate the
    STOP codons as `*`, and so we must instruct it not to.

    The following prompt will handle these compexities,
    and the code that it generated has been included as
    `Solutions/translate-DNA_intermediate.solution.py`:
    ```
    Please write a program named `translate-DNA_intermediate.py`
    that reads a set of FASTA-encoded DNA sequences from STDIN,
    standardizes their case, translates each sequence from DNA to protein
    using the "Bacterial" genetic code (NCBI transl_table=11),
    and writes the translated sequences in FASTA format to STDOUT.
    Please be careful to ensure that all three possible START codons
    are translated as 'M' when they are in the initial position.
    STOP codons should terminate translation.
    Invalid codons should be translated to 'X'.
    ```

    The output of this program has been included as
    `Solutions/Result1.intermediate.faa`;
    we encourage you to use the `diff` command to compare them:
    ```
    diff Solutions/Result1.simple.faa Solutions/Result1.intermediate.faa
    ```

9. Bonus 2: Real biology contains many other complications, and one of them is that some lifeforms use slightly different versions of the genetic code, and slightly different methods of transcription and translation. The "National Center for Biotechnology Information"
has standardized each of these 30-odd variant genetic codes and [assigned them
code-numbers,](https://en.wikipedia.org/wiki/List_of_genetic_codes) which is where the mysterious `transl_table=11` (translation-table 11) within the "Bonus 1" exercise's prompt came from.

    * Ask Grimoire how transcription differs in Bacteria, Archaea, and Eukaryotes.

    * Ask Grimoire how translation differs in Bacteria, Archaea, and Eukaryotes.

    * Ask Grimoire to explain the differences between the various different genetic codes.

To save you from needing to learn and handle 30-odd slightly different
codes, the translation-tables for these codes have been encoded into a BioPython module, as has the code
for reading, writing, and translating DNA sequences.
The following prompt will generate code using BioPython to handle all of the complexities of the variant genetic-codes and their translations:

```
Please write a program named `translate-DNA_biopython.py` that:

* Does not make use of any deprecated modules,

* Accepts an optional translation-table-number argument, with default-value '11',

* Reads a set of FASTA-encoded DNA sequences from STDIN using BioPython SeqIO
 and standardizes their case,

* Uses BioPython's Seq.translate() method to translate the entire DNA sequence
 to protein using the specified translation table, stopping at the first STOP codon,

* Uses SeqIO to write each translated sequence in nicely-formatted FASTA to STDOUT,
 with exactly the same sequence-description as in the input record.

Please also get the list of valid START codons for the specified translation-table
from BioPython, and ensure that these START-codons are correctly translated to 'M'
when they are in the initial position.
```

We have included the code that the above prompt generates as `Solutions/translate-DNA_biopython.py`,
and its output as `Solutions/Result1.biopython.faa`.
You can run this code as follows,
assuming that your `bash` or `gitbash` shell starts out from the main directory, `FIG-Bioinformatics-Course`
```
cd 1_Representative-Genomes/1.2_FASTA-Files/

python python Solutions/translate-DNA_biopython.solution.py --table 11 < ../../Data/Sample1.fasta > ../../Data/Result1.biopython.faa
```

