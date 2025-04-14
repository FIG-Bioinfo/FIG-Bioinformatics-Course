# TSV File Exercise 5 - Fixing Syntax Errors

Objective: Find and eliminate syntax errors inside of your code

In almost every program that is written by a human, there will usually be an error or two that will be accidentally incorporated, such as spelling or minor syntax errors. VSCode (and other IDEs) may be able to detect and signal the program-developer that there are potential errors within their code based on the syntax rules of the programming language. It is important to not only recognize these signals, but to also understand the error messages that you might receive while writing or running code. 

## Materials: 
[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── TSV-Exercise-5_Fixing-Syntax-Errors.md   (you are here)
├── Code/
│   ├── error_message1.py
│   ├── error_message2.py
│   ├── error_message3.py
│   ├── error_message4.py
│   ├── error_message5.py
│   └── error_message_final.py
└── Data/
    ├── bindict.tbl
    ├── data.tbl
    └── rep200.list.tbl   
```

## Exercise: 

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.


1. Ask Grimoire to describe to you each of the following errors. Make sure that you ask follow up questions and request examples for each type of error that you think would be hard to identify.
* Syntax errors
* Runtime errors
    * Index errors
    * Name errors
    * Attribute errors
    * Type errors

2. Inside the Code directory, we have include a set of files that are designed to throw specific error-messages. Each filename has the form `error_messageN.py` where `N` is a number. Open up the first file `error_message1.py`, which contains 3 syntax errors; run this program to see which error messages are reported. 

3. Open up the first file `error_message1.py`, which contains 3 syntax errors. Notice that when you open this file in VSCode, it will highlight the 3 lines that contain errors in red with a squiggly line under the text. Look for the squiggly lines and see if you can identify which lines they are on.

4. Computing languages are very strict about syntax. If you forget to add a colon at the end of a line, or forget to add a quotation mark around a string, the program will not run. Go ahead and run `error_message1.py` and notice the following error message that gets printed in the command line: 

    ```
    python3 Code/error_message1.py
    ```
You will see a message that looks like this:

    ```   
    File "C:\Users\Directory\FIG-Bioinformatics-Course\Code\error_message1.py", line 5
        if len(sys.argv) != 2
                         ^
    SyntaxError: expected ':'
    ```
This is Python's way of trying to help you figure out what went wrong. The first part of the message tells you the name of the file that contains the error. That is pretty self-explanatory for us right now because we are only using one program. But once you start using more programs and having them talk to each other, this part of the message will become more important. The end of that same line tells you what line number inside of the file that contains the error. And then it prints that line out for you and puts an arrow in the exact location of where the program stopped running. The last part of the message is the actual error message that you need to fix. In this case, Python is telling you that you forgot to add a colon at the end of line 5. Thankfully, this means that the error is easy to fix! As all we have to do is add a colon to the end of line 5 to fix the error. Go ahead and do this and run the program again. 


5. If you remember there were 3 syntax errors in the file. Therefore if you got the following output, you have found the second syntax error effecting your program.
    
    ```
    File "C:\Users\Directory\FIG-Bioinformatics-Course\Code\error_message1.py", line 12
        with open(filename, newline='') as file
                                           ^
    SyntaxError: expected ':'
    ```
This error message is telling you almost the exact same thing as the first error message. The difference here is that the error is on a different line of the file. Notice that there was already a red squiggly line at the end of line 12 before you ran your program. This is VSCode's way of highlighting the error for you. Now go ahead and add a colon to the end of line 12 to fix the error. If you feel confident enough, you can go ahead and fix the last syntax error as well. You will know you have fixed all the errors when you run the program and get one of the following outputs:

    ```
    Usage: python tsv_headers.py <filename>
    ```
    ***Note: This next printout was created using Data/bindict.tbl as the input file.***
    ```
    Field names in the TSV file are:
    genome_id
    genome_name
    RepGen.200
    RepGen.100
    RepGen.50
    ```

6. Each `error_messageN.py` file has been constructed to throw a different error. Most of them require a data file argument when being called from the command line. If you get a message that looks like:
```
Usage: python tsv_headers.py <filename>
```
then add `Data/bindict.tbl` to the end of your command to see if the program now works. Use the table below to keep track of which errors appeared and how to fix them. You can use this table as "quick reference" when debugging future programs.

Use Grimoire and the printed messages in the command line to help you identify and fix the errors in each file. If you get stuck, use `error_message1.py` as a template to help you fix the errors in the other files.

** NOTE: If you are getting an error that says "[Errno 2] No such file or directory" for the error_message.py file you are working on. Try killing your terminal and opening a new one to ensure the error is coming from the program and not from your operating system.

| Error Type      | File Name | Possible Fix |
| :-------------- | --------- | ------------ |
| Index Error     |           |              |
| Name Error      |           |              |
| Attribute Error |           |              |
| Type Error      |           |              |
| Syntax Error    |           |              |


## Solution Check instructions:
If you are successful, you should see the following output for each associated command:

* error_message1.py: Add a colon to the end of lines 5, 12, and 16
* error_message2.py: Add `filename = sys.argv[1]` to line 10
* error_message3.py: Remove line 11 `y='5'`
* error_message4.py: Remove the `counter = 1` and `Next Up` message (Lines 10, 21, 22)
* error_message5.py: Remove Line 20 `header.reverse()`
* error_message_final.py: Put line 12 after line 14.
    * remove `reverse()` from line 12
    * Add a `"` to line 20 just before the closing paranthesis near the end
    * Add a `:` to the end of line 4