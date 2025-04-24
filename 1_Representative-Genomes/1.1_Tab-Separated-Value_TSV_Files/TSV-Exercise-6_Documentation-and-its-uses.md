# TSV File Exercise 6 - Documentation and its uses

Objective: Create documentation for your program for reference

Now that we have created our program, we will need to prepare it for outside users.  This means making sure that it doesn't break due to incorrect inputs, and adding "help" features to make sure that anyone who uses the program can easily understand how to invoke it. We can accomplish these goal by adding validation tests that will catch incorrect use of the program and send the user warning messages, and by creating documentation that shows the user how to invoke the program. This exercise walks you through the error-checking and documentation processes, and also adds a new capability that the user may be expecting.


## Materials: 

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── TSV-Exercise-6_Documentation-and-its-uses.md (you are here)
├── Code/
│   └── tsv_headers.py
└── Data/
    ├── bindict.tbl
    ├── data.tbl
    ├── rep200.list.tbl
    └── TSVReaderDocumentation.txt 
```

## Exercise: 

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then go to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. Before we work on documentation for our code, we must figure out how to make sure that the user does not break it.  This means giving careful consideration to possible incorrect invocations that you did not intend. Tell Grimoire that you are attaching program `tsv_headers.py` (for instruction on how to "attach" a file, see TSV-Exercise-3, "Modifying Code"), and that you wish to protect users against possible invocation errors such as missing mandatory arguments, nonexistent data-files, etc. Ask Grimoire to recommend revisions to the program that will protect against each of the possible error-producing scenarios that it finds within the program, and remind it that warning and error messages should go to `STDERR`, not `STDOUT`. Be sure to ask it to explain how it has protected against each possible problem "line-by-line" to ensure that you understand all of its suggested improvements. 

2. Once your program has been revised to protect against invocation errors, we now need to document what your program does and how people can use it. There are three places to add documentation:
    * Inside the code, by inserting comments at strategic points to make sure that people reading, editing, or working on the code can understand it easily.
    * Inside the usage or "help message" for the code. Think of this as being like the "help menu" in an application. We need to build a menu of command options that the user can request via the command line.
    * In a completely separate document. This is the instruction manual on how the code works, what it is expected to do, and the possible use cases of the code.

4. Grimoire already has your code. Ask it to insert detailed comments into your code to clarify and explain what each section of the code does. You can also attempt to do this by hand to increase your understanding or how to edit and comment a program.

5. Ask Grimoire to insert a "help block" for your code that will be returned if the code is invoked with a `-h` or `--help` argument.

6. Lastly we need to write up our own documentation of the program inside its own file. Ask Grimoire to write  documentation for the code that describes the following things:

    * Purpose of the program
    * Functions of the different variables
    * Troubleshooting recommendations
    * Author credits

Copy the documentation into your clipboard, then go to VScode. Click on `New text file` under the `File` menu, and paste in the documentation. There will be slots in the "Author Credits" section for your name, etc., that you should fill in. Once you are done editing the documentation file, click on `Save as...` under the `File` menu, navigate to the `Data` directory underneath `1_Representative-Genomes`, enter `tsv_reader_documentation.txt` in the "Save as" box at the top of the file-saving popup, and hit "Save". Congratulations! You have just written and saved a new file using VScode!

## Solution Check instructions:
If you are successful, you will have documentation of your program in `tsv_reader_documentation.txt`, and your code will have an added `--help` option that when invoked will explain to a user what the program does and how to use it, plus a set of comments that were inserted into your code which will explain to another programmer what each section of the code does.
