# Kmer Exercise 2 - Jaccard Similarities

Objective: Learn about the concept of "Jaccard similarities", and how they are used to compare sequences.

Comparing and contrasting sequences is the main way that scientists find patterns within DNA and protein sequences. The Jaccard Similarity is a formula that we can use to determine how similar two sets (or groups of Kmers) are from each other. If two sequences that perform then same role are very similar, there is good chance that they from two closely-related species or genera. But if they are very different, the chances are high that they they are from two distantly-related species or genera. This lesson allows you to explore using the Jaccard Similarities Formula to estimate sequence-similarity using kmers.

## Materials: 

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── Definitions.html
└── 1_Representative-Genomes/
    ├── Code/
    │   └── kmer_jaccard_similarities.py
    ├── Data/
    │   └── Sample1.fasta
    └── 1.3_Kmers-and-Jaccard-Similarities/
        ├── Kmer-Exercise-2_Jaccard-similarities.md  (you are here)
        └── Solutions/
            └── kmer_jaccard_similarities_solution.py
```

## Exercises:

*ALWAYS RESET YOUR PATH* 

Type `source ~/.bashrc` into your command line to reset your path to the Course directory before starting each exercise.

1. Prepare Grimoire for this session as in the previous exercise by once again entering the prompt:

```
I am going to give you some definitions in an attached file;
you don't need to respond to them, just learn them.
I'm then going to ask you some questions.
```

and again attaching the file `Definitions.html` using the "paperclip" icon before clicking the "Send message" ("Up-arrow") icon.

2. Ask Grimoire "What is a 'Jaccard Similarity', and how is it used?"

3. Ask Grimoire "How would I compute the jaccard-similarity of two sequences using Kmers?"

4. Ask Grimoire to write a program that:

    * Takes a Kmer-length as a command-line argument,

    * Uses BioPython to read a FASTA-formatted file from STDIN or as a command-line argument,

    * Computes the number of Kmers in common and the jaccard-similarities for all pairs of sequences in the FASTA file

    * Prints the sequence-IDs, number of Kmers in common, and the jaccard-similarities to STDOUT in tab-separated format if the number of Kmers in common is not zero.

    * Prints the number of pairs and the number of pairs with nonzero similarity to STDERR.

5. Ask Grimoire to translate the program into pseudocode.

6. Use VScode to save the generated pseudocode and code into the stub-program `Code/kmer_jaccard_similarities.py`,

7. Use VScode to open a "terminal" window and run the program on the data-file `Sample1.fasta` using '20' as the value of `k`:

```
python Code/kmer_jaccard_similarities.py -k 20 -f Data/Sample1.fasta > Data/Sample1_jaccard_output.tsv
```
* Note: Sometimes Grimoire will generate code that uses a module of python that might not be installed on your system. If you get an error that has the last line `ModuleNotFoundError: No module named 'matplotlib'` , you can try to install it using `pip install matplotlib`. Notice that matplotlib is not the only module that you might need to install, but as long as you write the name of the module as the third argument to the `pip install` command, it should fix the error.

The output file in `1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Data/Sample1_jaccard_output_solution.tsv` should contain the output of your program. Use the `diff` command to compare your program's output to the solution-program's output.

* Notice that the number of pairs with nonzero similarity is less than the number of pairs of sequences; this is not an error, it means that many of the sequences do not have even a single 20-mer in common, which implies that our sample is diverse.

8. Repeat the exercise with `k=10`, and note that now most of the jaccard-similarities are non-zero.

```
python Code/kmer_jaccard_similarities.py -K 10 -f Data/Sample1.fasta > Data/Sample1_10mers_jaccard_output.tsv
```

This exercise illustrates that there is a tradeoff between "sensitivity" and "specificity": Larger values of `k` yield results that are far more specific (i.e., fewer "hits" will be found, and that the pairs that are found will be "closer" to each other, i.e. "more similar"), but the price to be paid for a more "specific" value of `k` is that it is also less "sensitive", so that if `k` is too large, the search may not find anything at all.

Output solution file for this step can be found in `1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_10mers_jaccard_output_solution.tsv`. 

9. Ask Grimoire to explain the difference between the concepts of "sensitivity" and "specificity", and how they are relevant in bioinformatics and in medicine.

10. In bioinformatics, we will often specify similarity-thresholds in terms of the number of Kmers that two sequences must have in common rather than in terms of their Jaccard-similarity.

11. Ask Grimoire to write a program `num_kmers_vs_jaccard.py` that takes a Kmer-length and a FASTA filename as command-line arguments. Be sure to mention for Grimoire to use the module `argparse` to parse the command-line arguments. Then for all pairs of sequences, plots the number of Kmers in common between them vs their jaccard-similarity. This will allow you to see how the number of Kmers in common and the jaccard-similarities vary with `k`.

Call the program with `k=20` and `Data/Sample1.fasta` as the FASTA file.
```
python Code/num_kmers_vs_jaccard.py -k 20 -f Data/Sample1.fasta
```
Output solution file for this step can be found in `1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_20mers_num_kmers_vs_jaccard_solution.png`. Notice that it is a picture file of a scatter-plot. Therefore do not be surprised if a new window opens up when you run your program with a picture of a scatter-plot.

12. Save this program as in exercise (5.), and then run it for various values of `k` to get a feel for how the number of Kmers in common and the jaccard-similarities vary with `k`. As in the previous exercise, you should see that larger `k` will result in fewer pairs of sequences with Kmers in common (also referred to as fewer "hits"), and also that fewer Kmers in common correlates with a smaller jaccard-similarity, so that larger `k` means smaller sensitivity (smaller scores) but also larger specificity (fewer hits).

## Solution Check instructions:

The `Solutions` subdirectory for this module contains three files for solution-checking the outputs of your programs:

* `1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_jaccard_output_solution.tsv`

* `1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_10mers_jaccard_output_solution.tsv`

* `1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_20mers_num_kmers_vs_jaccard_solution.png` (This one is a picture file of a scatter-plot)

As a reminder, the `diff` command has the following syntax to check the output of your program against the solution-program's output:

```
diff file1 file2
```

The following commands will create solution outputs from the solution programs:

```
python3 1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/kmer_jaccard_similarities_solution.py -K 20 -f Data/Sample1.fasta > 1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_jaccard_output_solution2.tsv

python3 1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/kmer_jaccard_similarities_solution.py -K 10 -f Data/Sample1.fasta > 1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_10mers_jaccard_output_solution2.tsv

python3 1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/num_kmers_vs_jaccard_solution.py -k 20 -f Data/Sample1.fasta > 1_Representative-Genomes/1.3_Kmers-and-Jaccard-Similarities/Solutions/Sample1_20mers_compare_solution2.tsv
```
 
