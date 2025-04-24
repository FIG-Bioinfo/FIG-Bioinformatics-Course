# FASTA Exercise 1 - What is FASTA Format?

Objective: Become familiar with the FASTA file-format. 

FASTA is one of the most basic file-formats for storage and exchange of biological sequences. We use FASTA files constantly when looking at data in the bioinformatics space. In order to use FASTA format, we first need to understand how it came to be, and what information is available within it. A sample FASTA file has been put into the Data folder for you to explore.

You will not be creating any code in this exercise, you will just be asking Grimoire questions. 

## Materials: 

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── 1.2_FASTA-Files/
│       └── FASTA-Exercise-1_What-is-FASTA-format.md
└── Data/
    └── Sample1.fasta
    
```

#### Exercise: 

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then go to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

The FASTA file-format is defined as follows:

* A FASTA-file consists of one or more "records".

* A record has the following format:
    - Each record must begin with a "record header" whose first character is a "greater-than" sign `>` and is immediately followed by a sequence-identifer. Sequence-identifiers must not contain spaces.

    - Any text on the record-header that follows the first space-character through the end of the line is considered to be a "sequence description" or "comment". "Sequence descriptions" are optional, and their contents are unrestricted beyond consisting of "Plain Text".
Two common uses of the "Sequence description" are to describe the function of a sequence, and/or to indicate which genome the sequence came from.

    - The lines following the "record header" contain sequence-data.
Sequence-data may be entered all on one line, or may be broken into multiple lines; however the sequence-data must not contain blanks, and a blank line is only allowable if it is the last line of a record.

1. Ask Grimoire to explain the three important types of biological sequences: DNA, RNA, and protein.
(If Grimoire uses any words or terms that you are not familiar with, please ask it to explain these terms.)

2. Ask Grimoire to explain the various "alphabets" that are used to represent DNA, RNA, and protein sequences.

4. Ask Grimoire to tell you the history of the FASTA format. 

5. Bioinformaticians have evolved a set of conventional file-extensions that are used to inform a researcher of what type of sequence-data that a FASTA file contains. Ask Grimoire to list the set of commonly-used FASTA file-extensions, and explain which type of sequence-data is associated with each of these commonly-used file-extensions.

6. Ask Grimoire to display a example of a protein sequence, a DNA sequence, and an RNA sequence FASTA-record. Notice the differences between each type of data.

7. Ask Grimoire to list some use-cases for each of protein, DNA, and RNA sequence-data.
