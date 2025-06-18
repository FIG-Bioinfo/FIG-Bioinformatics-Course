#### Tab-Separated Value File Exercise 2

 Objective: Use Chatgpt to create a program that reads Tab Separated Files from the Command Line.

 This exercise focuses on creating a program that takes in the header of a TSV file and some command line arguments and compares them against each other. You will be going through the normal development process of a programmer which is similar to the process of a writer. They start like Outline, Draft, edit, review, and then publish. We start with pseudo code, Create the program, Debug for errors, Test output quality, and then Publish. See if you can tell what step you are in as you follow the exercise.

#### Materials: 

[chat.openai.com](https://chat.openai.com/)
command_line_kung.py
command_line_fu.py
Data/rep200.list.tbl 

#### Exercise: 

1. Ask Grimoire to explain what key word arguments are in terms of the command line.

2. Ask Grimoire to write a program that accepts a list of keywords as command-line arguments.

3. You will now prompt Grimoire to create a custom Python program to accomplish the following tasks. Create your own prompt to make Grimoire tell you this list of items specifically, then you can accept the code that it creates and paste it into the file "command_line_kung.py". This time also grab the pseudo code Grimoire gives you.

    * The program should read a tab separated file called "Data\rep200.list.tbl" with headers from keywords in the command line. 
    * The program should be written in python.
    * The program should extract the columns that match the keywords and write those columns to the standard output in the same order that they were listed.
    * The program should warn the user and stop if any keyword does not match the header-line.
    * The program should print something specific to let you know it has completed it's task.

4. Take your prompt from above and reorder the steps you gave Grimoire. See how Grimoire changes the code and pseudo code. Paste both into the file "command_line_fu.py"

5. Run one of the programs and check to see no errors come up. If there is an error, type the error message into Grimoire and see what solution it can come up with to help you.
    * Note: Grimoire does not know your file system so it might not catch every detail. If you come across a "File Not Found" error, that is because it cannot find the data file. You would need to use the "Absolute Path" of the file. Grimoire can teach you how to find the Absolute Path of the file. You got this!!

6. In order to run the program, go to the Terminal Menu at the top of VS code and click on New Terminal to open a new terminal underneath your code. Then you want to type in the following to run your command:
    'python command_line_kung genome_id genome_name domain genus species rep_id score distance
Also try it with the second program but do not worry if this one does not succeed:
    'python command_line_fu genome_id genome_name domain genus species rep_id score distance

7. If your command_line_kung program did not succeed, go back to step 3. If it did, then try it again with this command. This one should throw a warning message and then stop the program completely
    'python command_line_kung genome genome_name representative_id score distance
    * Bonus: Can you write your own similar test for command_line_fu? 

8. Once you have verified that the program succeeded in both 6 and 7, go ahead and save it as "cmd_tsv_header.py" to remind you that this one uses the ComManD line. Congratulations on making your own program using Grimoire!

9. BONUS: Write down the adjustments that you made to your Grimoire prompt to make it more successful.You can use these tricks in future prompts to get to your solution more easily.
    * What problems should you ask Grimoire to take into account in the future? 
    * What words were confusing to Grimoire? 
    * What words made the pseudo code more understandable?

## Solution Check instructions:
If you are successful, you will have the output that matches the following:
Step 5: genome_id genome_name domain genus species rep_id score distance
Step 6: a warning message like: "Warning: genome is not in the list of column names"

## Process - Step: 
Use this structure to help guide you through the programming process for future prompts
pseudo Code - Step 3
Draft - Step 3 & 4
Edits - Step 5
Review - Step 6 & 7
Publish - Step 8