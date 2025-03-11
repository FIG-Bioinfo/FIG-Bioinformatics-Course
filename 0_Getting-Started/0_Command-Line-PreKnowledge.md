# Command Line Pre-Knowledge

This will be your hub for basics of the command line that you will need to know as you traverse this course. Use this as your "cheat sheet" when working with the command line. If this is your first interaction with such a thing, make sure you keep this handy!

## Basics to know when working in a command line
1. There is no spell check in the command line; this means if there is anything misspelled, the terminal will not catch it and your command will likely throw an error!

2. Commands are case-sensitive; your commands will throw an error if the wrong case is used.

3. Much like spelling and capitals, spaces are also sensitive when using the command line. A missed space or an added space will likely mess up your command.

4. Within the bash shell, or "Git-Bash" shells, you only use the forward slash (/) within file or directory paths, even on a Windows machine where one would normally use the backslash in a filename or directory path. The backslash is reserved for "escaping" (protecting) spaces or "special characters".
    For example: the file name "My File" would need to be written as "My\ File" to prevent the space from being interpreted as a seperator.

5. VSCode will open the course exercises in the editing mode, which can be hard to read. To change the viewing of a lesson to "reading mode", use the shortcut `shift + command + v` on Mac and `shift + control + v` on Windows. This only works in MarkDown files, or .md files.

6. If there is a command you don't understand, just ask Grimoire! Many times Grimoire will give you a very long explanation of a command, but the first couple paragraphs will be the most helpful.

7. Any command that does not have a file path (we will explain what a file path is later in this document) will assume that you are already in the directory you need to be in. If the file or files you need for your command are in a different directory, your command will need a file path to get there.


# Basic commands to use
While practice is important, some examples of these commands contain real files and paths. If you want to practice commands, create your own testing files; this is to keep you from removing or losing important files. 

## File and Directory Commands
1. List files and directories in the current directory in "long format" ('-l' option), including "hidden" files ('-a' option, which you can remember as 'a' for 'all').
```
ls
```

```
-l
```
```
ls -la
```
*Example use of this command:*
```
ls 1_Representative-Genomes/1.1_Tab-Separated-Value_TSV_Files/Solutions
```
Note that command-options can often be combined as in the above example, where 'ls -la' is equivalent to 'ls -l -a'.

List files and directories in the current directory in "long format" (`-l` option), including "hidden" files (`-a` option, which you can remember as `'a' for 'all'`)
```
ls -la
```
Note that command-options can often be combined as in the above example, where `ls -la` is equivalent to `ls -l -a`.

2. Navigate to the named folder
```
cd path/to/directory
```
*Example:*
```
cd FIG-Bioinformatics-Course/0_Getting-Started
```

3. Show the full path to the current (working) directory, which can be remembered as 'pwd' means 'print working directory'.
```
pwd
```

4. Move one or more files to a different directory
```
mv file1 file2 file3 directory/destination
```
*Example:*
```
mv 0_Course-Syllabus.md 0_Download-Instructions.md FIG-Bioinformatics-Course
```
5. Rename a file or directory
```
mv oldname newname
```
*Example:*
```
mv data.tbl dataNew.tbl
``` 
6. Clear all text in the terminal
```
clear
```
7. Copy a file
```
cp filename duplicatefilename
```
*Example:*
```
cp data.tbl datacopy.tbl
```
To copy a file to another directory
```
cp filename path/to/directory
```
*Example:*
```
cp data.tbl FIG-Bioinformatics-Course/Data/
```

8. Delete (remove) a file
```
rm filename
```
*Example:*
```
rm data.tbl
```

9. List all commands entered during a session
```
history
```

## File Viewing and Manipulation
1. Display the contents of a file
```
cat filename
```
*Example:*
```
cat data.tbl
```
2. View file content one screen at a time
```
less filename
```
*Example:*
```
less data.tbl
```
3. View the first 10 lines of a file
```
head -n 10 filename
```
*Example:*
```
head -n 10 data.tbl
```

4. View the last 10 line of a file
```
tail -n 10 filename
```
*Example:*
```
tail -n 10 data.tbl
```

## Disk and System Monitoring
1. Display how much diskspace is in use, in "human-readable" form ('h' option)
```
df -h
```
You can remember this command as `diskspace free`

2. Display the size of a file or directory, as a 'summary' (`-s`) and in "human-readable" form (`-h`)
```
du -sh path/or/directory
```
You can remember this command as 'disk usage'. Note that once again we have combined the above options; the above command is equivalent to 'du -s -h'.

*Example:*
```
du -sh FIG-Bioinformatics-Course/0_Getting-Started
```


## Archiving and Compression
1. Compress a file and convert to a '.gz' file
```
gzip filename
```
*Example:*
```
gzip data.tbl
```
Note this will result in a smaller file renamed 'data.tbl.gz'.
2. Decompress a file and convert to a different kind of file
```
gunzip filename.gz
```
*Example:*
```
gunzip data.tbl.gz
```

3. Decompress a file to STDOUT
```
gunzip -c filename.gz
```
*Example:*
```
gunzip -c data.tbl.gz
```
The '-c' command-option is most often used when "piping" the contents of the decompresssed file to another command; for example, to view the first 10 lines of a compressed file, you could type:
```
gunzip -c data.tbl.gz | head -n 10
```
We will explain what it means to "pipe" the output of a command to the input of another command in a later lesson.

## Advanced Commands
1. Make a new directory
```
mkdir directory_name
```
*Example:*
```
mkdir FIG-Bioinformatics-Course
```

2. Remove an empty directory (directories containing files cannot be removed until emptied)
```
rmdir directory_name
```
*Example:*
```
rmdir FIG-Bioinformatics-Course
```