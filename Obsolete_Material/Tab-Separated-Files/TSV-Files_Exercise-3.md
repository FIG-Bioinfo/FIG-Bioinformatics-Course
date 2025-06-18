#### TSV File Exercise 3

 Objective: Adjust former programs for new use cases and inputs

 Editing your tools/programs into different use cases makes your own code more versitile and efficient. It also helps you to edit your own work and help you apply what you have learned to your own work. This exercise focuses on adjusting your first program to apply some of the concepts of the command line as well as those for prompting Grimoire (Chatgpt). This exercise is more hands off to help you apply the review process to your own code.

#### Materials: 

[chat.openai.com](https://chat.openai.com/)
Data/bindict.tbl
Data/data.tbl
Data/rep200.list.tbl
tsv_header.py

#### Exercise: 

1. Ask Grimoire to tell you how tsv_header.py works by inserting it as a file. If that does not work, try copying and pasting the contents of the file into the chat bot and have it explain it to you "line-by-line". Insert the most important topics into the beginning of the file as a comment (use #) for future reference. 

2. You need to adjust this program for a new use case. Use what you learned about Command Line Arguments and Grimoire prompts to make the following improvements on your code. 
    * The program needs to take the input file from a command line argument -i
    * The program needs to fetch the header-names from the sample tsv file in the Data directory
    * The program can take the argument -n to specify how many of the first columns will be printed to standard output. If this is not specified, then the program prints all columns
    * The program can take the -m argument to see by what factor it will skip the columns.This is optional (print every 4th, 8th, or every other column as examples)
    
3. Once you have finished, it should be able to take this prompt from the terminal:
    ' python tsv_header -i data.tbl -n 8 -m 4 
    And come back with 
    1042156.4 1121445.4
This data file has over 2000 columns and can take a long time to load in applications. Bonus points if you can do this entire program without opening the file yourself.

## Solution Check instructions:
If you are successful, you will have the following output for the related commands

' python tsv_header -i data.tbl -n 7 
* sample	1033731.3	1034345.3	1042156.4	1105031.3	1118060.3	1121370.3
' python tsv_header -i data.tbl -n 4 -m 20
* 1496.3893 203120.7 40545.1270 563192.3
' python tsv_header -i rep200.list.tbl -n 5 -m 2
* genome_name genus rep_id distance
' python tsv_header -i bindict.tbl 
* genome_id	genome_name	RepGen.200	RepGen.100	RepGen.50