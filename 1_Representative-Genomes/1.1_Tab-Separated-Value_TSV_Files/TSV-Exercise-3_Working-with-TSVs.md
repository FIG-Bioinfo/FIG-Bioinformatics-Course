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
└── Templates/
    ├── command_line_kung.py
    └── command_line_fu.py
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

1. Execute the following two commands to copy the file-templates
for this exercise into the `Code/` directory:

```
cp Templates/command_line_kung.py Code/
cp Templates/command_line_fu.py   Code/
```

2. Ask Grimoire to explain what the phrase "arguments of a command-line program" means.

3. Ask Grimoire to write an example-program that will accept a list of keywords as its command-line arguments. Then ask Grimoire to explain its code to you "line-by-line" if it did not do so.

4. You will now ask Grimoire (or "prompt" Grimoire, as it is also called)  to create a custom Python program to accomplish a specific set of tasks. Below is a list of program requirements, features, and functionalities that we would like Grimoire to implement; create your own prompt asking Grimoire to implement this list of features and functions for you:

    * The program should be written in python.
    * The program should read a tab-separated file from STDIN with a header-line as the first line.
    * The program should accept a list of keywords as command-line arguments.
    * The program should extract the columns whose headers match the keywords, and write those columns to STDOUT in the same order that they were listed within the command-line arguments
    * The program should warn the user (via STDERR so as not to pollute STDOUT) if any keyword does not match the header-line, and then exit.
    * Otherwise, if there are no keyword mismatches, then the program should execute its function, and then print a message to STDERR before exiting that lets you know that it has sucessfully completed its task.

5. Now we need to save the program that Grimoire has just generated:

    * Go to the File-Explorer and click on `Code/command_line_kung.py`
to open this file.

    * Go back to your Grimoire web-browser session,
copy the pseudocode that Grimoire returned,
and paste it into the "Pseudocode" section of `command_line_kung.py`.
(If Grimoire skips the step of describing the program using pseudocode,
you can explicitly ask Grimoire to translate the code it generated into pseudocode, which will be more "human-readable" and will help you to better understand what the real code is doing.)

    * Next go back to your Grimoire browser-session,
copy the code that it generated,
and paste it into the "Code" section of `command_line_kung.py`.

    * Finally, click on the VScode `File` menu,
then click on the `Save` menu-item to save your program.

6. Now it's time to run the program `command_line_kung.py` to check whether it performs its intended function, and confirm that no errors are reported.

    In order to run the program, go to the Terminal Window
that you opened earlier, and type the following to run your command:

    ```
    python3 Code/command_line_kung.py genome_id genome_name domain genus species rep_id score distance < Data/rep200.list.tbl > Data/kung.out
    ```

    (**NOTE:** The above should all be typed as a single line, even though your browser may have wrapped it around onto multiple lines on the screen.)

    If the program completes without errors, use the "File Explorer" to open `Data/kung.out`, and verify that it has extracted the selected columns in the selected order.

7. If there is an error, copy the error-message into your "Paste" buffer, then tell Grimoire that the code reported an error, paste in the error-message preceeded and followed by "triple quotes", and ask it to suggest possible fixes for the problem. (There is a good chance that if you ask Grimoire to implement its suggested fixes, it will be able to do so, in which case copy the new code, replace the old code with the new code, and go back to step 6.)

8. Once you can get your `command_line_kung.py` program to run without throwing error-messages, try it again with the following command. This invocation should throw a warning message that you've asked for a nonexistent data-field, and then exit.
    
    ```
    python3 Code/command_line_kung.py genome genome_name representative_id score distance < Data/rep200.list.tbl 
    ```

9. Grimoire understands the concept of an "unordered" (or "bulleted") list, within which (in most cases) the order of the list-items (usually) doesn't matter (unless there are item-dependencies), and it generates its answers to your prompts by examining all of the preceeding prompts and answers within a "Context Window" that is roughly 8000 words long. Hence, you should be able to shuffle the items within the "bulleted list" prompt you entered in exercise (3.) above, and Grimoire will (usually) still generate functionally-equivalent code. Please try this experiment, to see how (if at all) Grimoire changes its generated pseudocode and code after shuffling the "bullet points", and then paste the pseudocode and code into the template-file `command_line_fu.py`.

10. Finally, try executing the second program, but do not worry if this version does not succeed:

    ```
    python3 Code/command_line_fu.py genome_id genome_name domain genus species rep_id score distance < Data/rep200.list.tbl > Data/fu.out
    ```
    
* Bonus: Can you write your own similar tests for `command_line_fu.py`? 

11. Once you have verified that the first program succeeded in both 7 and 8,
go to the File-Explorer and select `Code/command_line_kung.py`.
Click on the File-menu,  select "Save As",
and in the file-saver popup enter the new name `cmd_tsv_select_columns.py`
to remind you that this program uses the ComManD line, since you will be using this program to prepare data in later exercises.
Finally, hit the `Save` button on the popup.
Congratulations!
You have just created your own program using Grimoire!

12. BONUS: Write down any refinements that you needed to make to your Grimoire prompt before the code it generated ran correctly and satisfied all of the features, and functionalities listed in the program requirements. You can use such tricks in future prompts to obtain your desired solution more easily.
    * What problems or error-conditions should you tell Grimoire to look out for in the future?
    (HINT: you might want to check for missing or invalid arguments, nonexistent data-files, etc.)
    * Were any of your instructions confusing to Grimoire? 
    * Did any of your instructions made the pseudocode more understandable?


## Solution Check instructions:

If you are successful, you will have an output-file that matches the following set of columns:
* Step 6: ``` genome_id genome_name domain genus species rep_id score distance```
* Step 8: a warning message like: ```Warning: genome is not in the list of column names```

## Process - Step: 
Use this structure to help guide you through the programming process for future prompts
* Pseudo Code - Step 4
* Draft - Step 4 & 5
* Edits - Step 6
* Review - Step 7 & 8
* Publish - Step 11