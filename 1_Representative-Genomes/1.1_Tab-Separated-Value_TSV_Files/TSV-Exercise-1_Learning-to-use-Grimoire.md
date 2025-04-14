# TSV Exercise 1 - Learning to use Grimoire

Objective: Become familiar with using ChatGPT, and learn about basic bioinformatics, common data-formats, and use of command-line tools.
 
ChatGPT is an AI model that can instruct you on the basics of many topics without needing to look up the information online. ChatGPT can also help you to write computer-programs without first needing to learn a computer-language yourself, merely by expressing what you need your computer to do using either "natural language", or, when a more precise problem-specification is needed, using a more formally-structured language intermediate between "natural" language and a computer-language called "Pseudocode".
Finally, ChatGPT can often explain to you what went wrong with a program and how to fix it. ChatGPT comes in many specialized versions, but the version that we will be using in these exercises is a "Code-Wizard" called ["Grimoire"](https://chat.openai.com/g/g-n7Rs0IK86-grimoire/).

ChatGPT applications such as Grimoire are very powerful and convenient --- however, do please note that sometimes it will "make things up" because it has been trained to be "helpful" even when it doesn't actually know the answer!
(Such "made-up" answers are often called "hallucinations".)
It's worth noting that ChatGPT will become considerably more cautious in its answers and less likely to "hallucinate" if you simply begin each session
by saying "Please answer all questions accurately, and if you don't know
the answer, please say 'I don't know' instead of making something up".

Thus, you should be cautious about assuming that what ChatGPT variants tell you is always "100% accurate", and you should "fact-check" claims that it makes that are "mission-critical" or that seem implausible to you, particularly with regard
to non-programming or non-science-related issues that are outside of Grimoire's
primary areas of expertise.<br>
Or in other words, "Trust, but verify"! ;-)<br>

For this course, we have fact-checked Grimoire's answers to the questions
that we will be asking you to ask it, and the code that it generates
in response to problem-specifications.
Also, one of the skills that you will learn during this course will be
how to test and debug the software that Grimoire generates for you,
in the event that it does make an error.
We will also provide a `Solutions/` directory in each exercise module
that you can check your own results against. And if you find yourself
completely wedged, please feel free to contact the course-developers via the Discord Channel.

The following exercises are intended to get you used to interacting with "Grimoire" using both "natural language" and "pseudocode", while also introducing some basic types and formats of bioinformatic data.

## Materials: 

"Grimoire", at <https://chat.openai.com/g/g-n7Rs0IK86-grimoire>

Below is a visual schematic representation of the "Directory tree" for this section of the course. (See the first exercise below if you are unfamiliar with the concept of a "Directory Tree".) Indentation is used to represent subdirectory-levels, and items that end in `/` mean "directory that has this name"; otherwise, the item is a program or data file. In addition to the file you are currently reading, you will also need the files `bindict.tbl` and `tsv_headers.py`,
which are respectively in the `Data/` and `Code/` directories underneath the main directory `FIG-Bioinformatics-Course/`:

```
FIG-Bioinformatics-Course/
├── Templates/
│   └── tsv_headers.py
├── Data/
│   └── bindict.tbl
└── 1_Representative-Genomes/
    └── 1.1_Tab-Separated-Value_(TSV)_Files/
        ├── TSV-Exercise-1_Learning-to-use-Grimoire.md  (you are here)
        └── Solutions/
            └── tsv_headers_solution.py
```

## Exercises: 

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. Ask Grimoire to explain the concepts of "Directories", "Directory Trees", and "File Paths" to you. In particular, ask it to explain the concept of the directories "dot" and "double-dot" if it did not already do so.

2. It is conventional to end a filename with a "extension" that indicates to the user what kind of file it is and what programs can open it. Ask Grimoire to explain the concept of a "file extension" to you.

NOTE: In this course, most files will have extensions of either `.py` indicating that they are Python-language programs, or `.tbl` indicating that they are a "data table" of some type, although later in the course we will introduce some special-purpose file-extensions that are specific to files containing bioinformatic data. 

3. Ask Grimoire to explain what the terms `STDIN` (Standard Input), `STDOUT` (Standard Output), and `STDERR` (Standard Error) mean within the context of a command-line tool. If you are unfamiliar with the concept of a "command line", have Grimoire explain that as well.

4. Ask Grimoire to explain the concept of "pseudocode" to you, and why one would want to use "pseudocode" to specify a program rather than natural language.

5. Ask Grimoire to explain what a "tab-separated value (TSV) file" with a header-line is.

6. Ask Grimoire to write a Python program that will read a tab-separated-value data-file with header-line from `STDIN`, print the field-names in that TSV-file's header-line columns to `STDOUT`, and then exit; any error-messages should be printed to `STDERR`. Then ask Grimoire to explain to you how this program works "line-by-line".

    * Note: Make sure that you explicitly use the term "line-by-line", as Grimoire may not give a detailed explanation of everything within the program without it.

    * Similarly, if Grimoire's explanation of a particular line of code
    still confuses you, ask it to break down that line "step-by-step".

The key-phrases "line-by-line" and "step-by-step" trigger a particular mode of reasoning that "Large Language Models" (LLMs) have been extensively trained for; in "line-by-line" or "step-by-step" mode, an LLM is likely to reason more clearly, and is less likely to jump to conclusions, make mistakes, or "hallucinate".

7. In the terminal-window, enter the following command:

```
cp Templates/tsv_headers.py Code/
```

You should read the command `cp` as "copy", because it copies
its first argument (in this case the file `Templates/tsv_headers.py`)
to its second argument (in this case into the Code-directory `Code/`).
When the second arument is a filename the new copy will have that name,
for example, `cp file1 file2` will make a copy of `file1` that is named `file2`,
whereas when the second argumant is a directory, the copy will have
the same filename as the original file.

8. Use Grimoire's "clipboard" icon at the upper-right of its code-window to copy the program to your clipboard. Then go to "File Explorer",
which is the icon in the left toolbar that looks like two overlapping
pieces of paper.
Scroll down to the directory named `Code/`.
If it is preceeded by a symbol that looks like a `>`,
then click on `Code/` to expand this directory-listing.
Within the `Code/` directory, you will see a number of files; scroll down to the file named `tsv_headers.py` and click on it, which will open that file in the file-editor. You will see that  `tsv_headers.py` is empty except for the following series of "comments":
```
########################################################################
# This file has been created to contain the code
# that Grimoire generated for the exercise `tsv_headers.py`.
# Each line that begins with a '#' character is called a "comment";
# "comments" are intended for human readers, 
# and will not be interpreted as "code".
#
# Please paste the code that Grimoire generated below,
# and then select and click "Save" under the "File" menu
# to save the code.
```
Paste Grimoire's code that you saved to your clipboard into the file `tsv_headers.py` below the comment, then click on "Save" under the "File" menu as instructed, which saves your program to disk. 

9. You are now in a position to run your program.
Grimoire has probably already shown you an example of how to run this program during its summary-discussion of the program, but since Grimoire is ignorant of the details of your operating-system, directory-structure, and the fact that you are using the VScode development-environment (unless it has explicitly been told these things),   its example probably will not work verbatim. So, to run the program in your environment, please follow the steps below: 

* Click on "New Terminal" under the VScode "Terminal" menu to open a terminal-window within VScode. VScode should respond by opeing a window
that contains something similar to the following:

```
✅ COURSE_HOME is: /Users/yourUsername/Projects/FIG-Bioinformatics-Course
🔁 Use the command 'cdcourse' anytime to return to this root.

yourMachineName:FIG-Bioinformatics-Course yourUsername$ 
```

* Click on the "Terminal" window that VScode just opened,
which will switch VScode's "focus" to that window.
You can confirm that you are in the correct directory by entering `pwd` (short for "print working-directory") and hitting the `return` key;
your computer should respond with a directory-path ending in `FIG-Bioinformatics-Course`.

* To run `tsv_headers.py` on the file `Data/bindict.tbl` under `macOS` or `LINUX`,
first make sure that title-bar of your terminal window shows
that it is set to the `bash` environment.
If you do not see the word `bash` in the title-bar,
look for the `+` icon in the title-bar that is followed by a
"dropdown menu" icon, which looks a bit like a `v`.
Click on the `v` and select `bash`, which will set your default
terminal envionment to the `bash` environment.

If you are working on a `Windows` machine, you should instead select
`Git bash`.
We have included instructions on how to install `gitbash` within the `0_Getting-Started` module.


* To run your program, enter the following command and hit the `Return` key:

```
    python3 Code/tsv_headers.py < Data/bindict.tbl
```

The above command asks the `python3` program-interpreter to run the program `Code/tsv_headers.py`, reading its data from the file `Data/bindict.tbl`.

**NOTE:** The above command should be entered as a single line,
even if your browser might have wrapped it onto two lines.

* The result of the above command should match the text in the
`Solution Check` section below.

If you come across any problems that you do not know how to fix,
please feel free to ask Grimoire for help by describing the steps
that you have taken to create the problem and what error messages
that you are receiving. It can be surprisingly helpful!


## Solution Check instructions:
If you are successful, the program should return output that matches the 5 column-headings in the data file.

```genome_id	genome_name	RepGen.200	RepGen.100	RepGen.50```

In the `Solutions/` subdirectory of this module, we have included the program `tsv_headers_solution.py` that Grimoire wrote for us;
this program may perhaps differ in precise detail from the program
that Grimoire wrote for you, but it should be functionally equivalent.

To test out the Solution program, run the following command:

```
python3 1_Representative-Genomes/1.1_Tab-Separated-Value_TSV_Files/Solutions/tsv_headers_Ex1_solution.py < Data/bindict.tbl
```

If you experience the following error:

```
$ python3 1_Representative-Genomes/1.1_Tab-Separated-Value_TSV_Files/Solutions/tsv_headers_solution.py < Data/bindict.tbl
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Manage App Execution Aliases.
```
You can fix it by changing `python3` to `python` in the command.
python 1_Representative-Genomes/1.1_Tab-Separated-Value_TSV_Files/Solutions/tsv_headers_solution.py < Data/bindict.tbl

If you experience the following error:

```
C:\Users\parre\AppData\Local\Programs\Python\Python312\python.exe: can't open file 'C:\\Users\\parre\\OneDrive\\Documents\\Projects\\FIG-Bioinformatics-Course\\1_Representative-Genomes\\1.1_Tab-Separated-Value_TSV_Files\\Solutions\\tsv_headers_solution.py': [Errno 2] No such file or directory
```

It means that the spelling of one of your file paths is incorrect.
Be sure to check your spelling of the files. Using the tab in the commmand line to navigate through the file paths can help you to avoid this error.
