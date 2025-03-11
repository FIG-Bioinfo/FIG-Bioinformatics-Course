# TSV File Exercise 4 - Modifying Code

Objective: Revise an existing program to incorporate new use-cases and inputs

Editing your tools/programs to support various different use-cases makes your own code more versatile and effective. It also helps you to improve your own work and to apply what you have learned to your own work. This exercise focuses on revising your program from TSV Exercise 1.1 to incorporate some of the concepts you have learned regarding use of the command-line interface, as well as those for prompting Grimoire (ChatGPT). This exercise is more "hands off" in that you will mostly be applying a "Review" process to your own code.

## Materials: 
[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── 1.1_Tab-Separated-Value_\(TSV\)_Files/
│       ├── TSV-Exercise-4_Modifying-code.md   (you are here)
│       └── Solutions/
│           └── tsv_headers_Ex4_solution.py
├── Code/
│   └── tsv_headers.py
└── Data/
    ├── bindict.tbl
    ├── data.tbl
    └── rep200.list.tbl
```

## Exercises:

*ALWAYS RESET YOUR PATH* 

Type `source ~/.bashrc` into your command line to reset your path to the Course directory before starting each exercise.

1. Ask Grimoire to tell you how `tsv_headers.py` works by "attaching" the file to your question regarding how the code works before submitting it. (You "attach" a file to a prompt by saying _"I am going to attach a program that I would like to work on with you",_ then click on the "paperclip" icon at the left of the "Messages" box (AKA the "prompt"), select the program to upload, and finally click the "enter" icon at the right of the prompt.) If attaching the file does not work, try copying and pasting the contents of the file into the "Messages" box. Then, ask Grimoire to translate the attached code into "pseudocode", and explain the program to you "line-by-line". Insert the pseudocode and Grimoire's explanation into the beginning of `tsv_headers.py` as a "block-comment" for future reference.
* NOTE: "single-line comments" consist of anything that follows a `#` character through the end of the current line.
* Multiline "block-comments" are most easily constructed by placing three single-quotes or double-quotes by themselves on the lines preceding and following the text of the "block-comment", like this:
```
        """
        Comment-line 1
        Comment-line 2
        [...]
        Comment-line N
        """
```

2. In your previous exercises, your program used what are known as "positional arguments", which work like this:

    ``` python3 program_name arg1 arg2 arg3 ... ```

    Python programs also support "named arguments", which work like this:

    ``` python3 program_name -a argA -b argB -c argC ... ```

    Named arguments have the advantage over positional arguments that they can be either optional or mandatory, and unlike positional arguments, their order doesn't matter.

    Named arguments can have a "long form" as well as a short form; "long form" arguments look like this:
    
    ``` python3 program_name --nameA argA --nameB argB --nameC argC ... ```

    Ask Grimoire to tell you more about "short form" and "long form" named arguments, and ask it to give you some examples; then ask it any questions that you might have about named arguments.

    Then create a copy of `tsv_headers.py` and save it as `tsv_headers_OLD.py` by using the following command in your terminal.
    
    ``` cp Code/tsv_headers.py Code/tsv_headers_OLD.py ```

    This will act as a "backup" of the original program, in case you need to revert to it.


3. In this exercise you are going to revise the `tsv_headers.py` program to add named arguments and a new use-case. Use what you learned about Command Line Arguments and Grimoire prompts to make the following improvements to your code.

```
I have uploaded a program that I'd like you to modify. Please make the following revisions to the tsvheaders program:

* The program should accept its input datafile-namevia the command-line argument '-i' (short for "Input"), e.g. '-i datafilename'.

* The program should extract the header-names from the first line of the input datafile.

* The program can accept an optional '-s' argument to specify a keyword to search for in the header-names. This keyword will be used to select the columns that contain the keyword. It can be all inclusive or be just a partial match and case-insensitive. 

* The program can accept an optional argument '-n' to specify the "total number of selected data-columns that will be printed to STDOUT", e.g. -n 4 means "Print a TOTAL of 4 selected columns to STDOUT". Please note that this argument specifies the TOTAL number of columns to be printed to STDOUT --- it does _NOT_ specify the maximum column-number to be printed! If this optional argument is not specified, then the program should print all of the  elected columns in the input datafile.
```
    
4. Save the modified program as in previous exercises. 

5. Once you have finished with these revisions, the program should be able to take the following prompt from the terminal:
    
    ``` python3 Code/tsv_headers.py -i Data/data.tbl -n 3 ```
    
    and it should return the output:
    ``` sample  1033731.3       1034345.3```
* NOTE: The file `data.tbl` has over 2000 columns, and so can take a long time to load in applications. Bonus points if you can perform the entire program-revision without opening up the program file to edit it yourself.

## Solution Check instructions:

If you are successful at revising your program, you should see the following output from each of the following commands. (NOTE: once again, commands should be entered as a single line, even if they appear to wrap over multiple lines of the screen):

* ``` python3 Code/tsv_headers.py -i Data/data.tbl -n 4 -s 20 ```

    ``` 1423720.3       203120.7        2049039.65      206672.9```

* ``` python3 Code/tsv_headers.py -i Data/rep200.list.tbl -n 5 -s i ```

    ```genome_id       domain  species rep_id  distance```

* ``` python3 Code/tsv_headers.py -i Data/bindict.tbl ```

    ``` genome_id	genome_name	RepGen.200	RepGen.100	RepGen.50 ```
