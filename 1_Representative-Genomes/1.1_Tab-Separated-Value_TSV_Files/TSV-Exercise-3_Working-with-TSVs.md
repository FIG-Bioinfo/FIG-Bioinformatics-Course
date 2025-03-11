# TSV Exercise 3 - Working with TSV Files

Objective: Use Grimoire to create a command-line program that reads and operates on Tab-Separated Files.

This exercise focuses on creating a program that accepts a list of column-names as command-line arguments, reads a TSV-file from STDIN, extracts the columns whose header-names match the argument list, and writes those columns to STDOUT. (For example, suppose that we have a TSV-file that has 15 columns, but we only care about the data contained in 3 of these columns.)

You will be going through the normal development process of a programmer, which is similar to the process of a writer, namely, Outline, Draft, Edit, Review, and then Publish. We will start with a description of the program, express that description as "Pseudo-code", Create the program, Debug for errors, Test output quality, and then Publish. See if you can tell which step you are in as you do the exercise.

## Materials: 

"Grimoire" at <https://chat.openai.com/g/g-n7Rs0IK86-grimoire>

You will also need the files "rep200.list.tbl",
"command_line_kung.py" and "command_line_fu.py";
indentation is again used to represent directory-levels:

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── 1.1_Tab-Separated-Value_(TSV)_Files
│       └── TSV-Exercise-3_Working-with-TSVs.md   (You are here)
├── Data/
│   └── rep200.list.tbl
└── Code/
    ├── command_line_kung.py
    └── command_line_fu.py
```

## Exercises:

*ALWAYS RESET YOUR PATH* 

Type `source ~/.bashrc` into your command line to reset your path to the Course directory before starting each exercise.

1. Ask Grimoire to explain what the phrase "arguments of a command-line program" means.

2. Ask Grimoire to write an example-program that will accept a list of keywords as its command-line arguments. Then ask Grimoire to explain its code to you "line-by-line" if it did not do so.

3. You will now ask Grimoire (or "prompt" Grimoire, as it is also called)  to create a custom Python program to accomplish a specific set of tasks. Below is a list of program requirements, features, and functionalities that we would like Grimoire to implement; create your own prompt asking Grimoire to implement this list of features and functions for you, then copy the pseudocode and code that Griomoire returns, and paste them into the template-file `command_line_kung.py`.
(If Grimoire skips the step of describing the program in pseudocode, you can explicitly ask Grimoire to translate the code it generated into pseudocode, which will be more "human-readable" and will help you to better understand what the real code is doing.)

    * The program should be written in python.
    * The program should read a tab-separated file from STDIN with a header-line as the first line.
    * The program should accept a list of keywords as command-line arguments.
    * The program should extract the columns whose headers match the keywords, and write those columns to STDOUT in the same order that they were listed within the command-line arguments
    * The program should warn the user (via STDERR so as not to pollute STDOUT) if any keyword does not match the header-line, and then exit.
    * Otherwise, if there are no keyword mismatches, then the program should execute its function, and then print a message to STDERR before exiting that lets you know that it has sucessfully completed its task.

4. Grimoire understands the concept of an "unordered" (or "bulleted") list, within which (in most cases) the order of the list-items (usually) doesn't matter (unless there are item-dependencies), and it generates its answers to your prompts by examining all of the preceeding prompts and answers within a "Context Window" that is roughly 8000 words long. Hence, you should be able to shuffle the items within the "bulleted list" prompt you entered in exercise (3.) above, and Grimoire will (usually) still generate functionally-equivalent code. Please try this experiment, to see how (if at all) Grimoire changes its generated pseudocode and code after shuffling the "bullet points", and then paste the pseudocode and code into the template-file `command_line_fu.py`.

5. Now it's time to run the program `command_line_kung.py` to check whether it performs its intended function, and confirm that no errors are reported.

    In order to run the program, first make sure you are in the "main directory" for the course by clicking the "File" menu, selecting `Open Folder`, selecting the folder `FIG-Bioinformatics-Course`,
    and then clicking the `Open` button. Then go to the Terminal Menu at the top of VScode and click on "New Terminal" to open a new terminal window underneath your code. You can verify that you are in the correct directory by typing `pwd` (short for "print working directory") to see whether the absolute path does indeed end in `FIG-Bioinformatics-Course`.

    Once you have verified that you are in the correct directory, type the following to run your command:

    ```
    python3 Code/command_line_kung.py genome_id genome_name domain genus species rep_id score distance < Data/rep200.list.tbl > Data/kung.out
    ```

    (NOTE: The above should all be typed as a single line, even though your browser may have wrapped it around onto multiple lines on the screen.)

    If the program completes without errors, use the "File Explorer" to open `Data/kung.out`, and verify that it has extracted the selected columns in the selected order.

* NOTE: Grimoire does not know your operating-system and file-system unless you have told it in advance _"I am using macOS"_ or _"I am using Windows"_, so it might not catch every detail regarding generating and running your program. (For example, under Windows, the file-path separator is `\` instead of `/`.) If your program reports a "File Not Found" error, it means that your computer did not know where to look for the data file; in such cases you may need to use the "Full Path" to the file. Grimoire can teach you how to find the Full Path of the file, it can instruct you on what any error-messages that you receive mean, and it can suggest possible fixes. You got this!!

6. If there is an error, copy the error-message into your "Paste" buffer, then tell Grimoire that the code reported an error, paste in the error-message preceeded and followed by "triple quotes", and ask it to suggest possible fixes for the problem. (There is a good chance that if you ask Grimoire to implement its suggested fixes, it will be able to do so, in which case copy the new code, replace the old code with the new code, and go back to step 5.)

7. Once you can get your `command_line_kung.py` program to run without throwing error-messages, try it again with the following command. This invocation should throw a warning message that you've asked for a nonexistent data-field, and then exit.
    
    ```
    python3 Code/command_line_kung.py genome genome_name representative_id score distance < Data/rep200.list.tbl 
    ```

 8. Finally, try executing the second program, but do not worry if this version does not succeed:

    ```
    python3 Code/command_line_fu.py genome_id genome_name domain genus species rep_id score distance < Data/rep200.list.tbl > Data/fu.out
    ```
    
* Bonus: Can you write your own similar tests for `command_line_fu.py`? 

9. Once you have verified that the program succeeded in both 6 and 7, go ahead and save it in `Code/` as `cmd_tsv_select_columns.py`, to remind you that this one uses the ComManD line, since you will be using this program to prepare data in later exercises. Congratulations on making your own program using Grimoire!

9. BONUS: Write down any refinements that you needed to make to your Grimoire prompt before the code it generated ran correctly and satisfied all of the features, and functionalities listed in the program requirements. You can use such tricks in future prompts to obtain your desired solution more easily.
    * What problems or error-conditions should you tell Grimoire to look out for in the future?
    (HINT: you might want to check for missing or invalid arguments, nonexistent data-files, etc.)
    * Were any of your instructions confusing to Grimoire? 
    * Did any of your instructions made the pseudocode more understandable?

## Solution Check instructions:
If you are successful, you will have an output-file that matches the following set of columns:
* Step 5: ``` genome_id genome_name domain genus species rep_id score distance```
* Step 6: a warning message like: ```Warning: genome is not in the list of column names```

## Process - Step: 
Use this structure to help guide you through the programming process for future prompts
* Pseudo Code - Step 3
* Draft - Step 3 & 4
* Edits - Step 5
* Review - Step 6 & 7
* Publish - Step 8