Objective: Learn what files paths are, when they are used, and how to create them.

# Creating File Paths
Within this course, you will eventually be asked to create your own file paths, and this could cause some confusion. In this section, we will go over what file paths are and how they are created.

## What are file paths
File paths function as a road map to a specific folder or file. In the same way directions on a map might show you landmarks on the way to your destination, a file path will lead you through each landmark in your file system.

File paths are structured like this:

```
home/user/Documents/file
```

Each forward slash acts as a seperator between landmarks. These are the stops on the way to your destination. In this template, 'home' would be the first jump, 'user' the next jump, 'Documents' the third jump, and 'file' being the destination. Let's see what a real file path looks like using the directory tree you are working with.

```
FIG-Bioinformatics-Course/1_Representative-Genomes/TSV-Exercise-0_Understanding-File-Paths.md
```

This would be the file path to get to this document. In the next section, how we made this file path will be explained.

## How to use file paths
In order to get to the course syllabus, you have to drop down the menu of the course, then the `0_Getting-Started directory`, then the course syllabus is right in there! This is how we reach it in the Explorer section of VSCode. Reaching it through the terminal is very similar.

**In this next section, follow along with the commands in your own terminal!**

To get somewhere, you have to know where you are starting. To know exactly where you are, you can use this command:

```
pwd
```

This will tell you where you are starting. Since this is where you are at, there is no need to include it in your file path; you will start then with the next landmark. In the case of the syllabus, if we're starting in 'FIG-Bioinformatics-Course', we need to go down into '0_Getting-Started'. The map part of your file path would look like this:

```
0_Getting-Started

```
That's it! Depending on your command, this is all you need! If you want to move down into the '0_Getting-Started directory', we use this command:

```
cd 0_Getting-Started
```

This will change your starting place to the directory of '0_Getting-Started'. You'll notice this reflected at the beginning of your command line. Now you can freely access the course syllabus (or any other file in this directory) by using commands like 'cat' which shows the contents of a file.

Now, using this method of step by step is fool-proof, but tedious. The way to include all these landmarks in the same command is to use forward slashes between jumps. In the step by step, our starting place was `FIG-Bioinformatics-Course`, then we went to `0_Getting-Started`, and finally landed on our destination of `0_Course-Syllabus.md`. This is all the information we need to complete a file path which looks like this:

```
0_Getting-Started/0_Course-Syllabus.md
```

Now you can stick this file path onto a command like this, which will show the contents of the syllabus in your terminal:

```
cat 0_Getting-Started/0_Course-Syllabus.md
```

Remember that you can move into other directories, but you cannot move into files. You can view files, create files, remove files, and many other commands!

## Errors
A very common error messages you might see while following along is:

```
No such file or directory
```

The first way to trouble shoot this error is to check your spelling. Many mistakes can come from misspelled words, forgotten punctuation, wrong capitalization, etc.

Another common error you might see is:

```
bash: command not found
```

This could also be a result of a misspelled command, or wrong command. Check that your command is correct and the punctuation around it is also correct. You can look back on the command cheat sheet at the beginning of this document.

If you've run into any unknown error while following along in your terminal, retrace your steps; if you still don't know what went wrong, ask Grimoire!