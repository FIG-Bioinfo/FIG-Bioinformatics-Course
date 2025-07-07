# Sample Set Creation Sorting Data 

**Objective:** Sort your gathered data into diseased and control groups,
then gather more samples.

Now that we have gathered all the data we need,
it's time to make the data useable for our machine learning model.
In order to create an accurate classifier,
the machine learning model will need to know which data are
from disease subjects and which data are from control subjects.

## Materials
[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)
[NCBI](https://www.ncbi.nlm.nih.gov/)
[SRAToolkit Download FASTA Documentation](https://www.ncbi.nlm.nih.gov/books/NBK242621/)

```
FIG-Bioinformatics-Course/
├── 3_Projections/
│   └── 3.1_Sample-Set-Creation/
│       └── Sample-Set-Creation-Exercise-2_Sorting_Data.md (you are here)
└── Data/
    └── (Data you downloaded from SRA in previous exercise)
```

In previous lessons, we have used FastQ and FastA files when it comes to our data. You might have been wondering what the difference is between the two! In previous excercises, we read files in FastA format. For sequencing data, we use FastQ format, which contains information about sequence quality in addition to sequence data.

In preperation for this exercise, you will need to check the storage space on your computer. If you are working on Mac, you can click on the Apple incon in the top left of your screen and bring up the
"About This Mac" window, click on "Info", and then enter "Storage"
in the search-box. If you are working on Windows, (incude windows instructions). To have room for all the samples, you will need approximately 10 GB.
In addition to the space on your computer, your reading of the FASTQ files will be much easier with an extension called Rainbow CSV. If you don't have it already installed, search it up in the extensions tab in your VSCode.

* Another helpful tool for viewing this course and the files is Word Wrap, which can be toggled under the View setting at the top of your screen.

## Exercise

*ALWAYS RESET YOUR PATH* 

Type `cd $COURSE_DIR` into your command line to reset your path to the Course directory before starting each exercise.

1. In this lesson, you will be downloading more data, then sorting it into two categories. You will need places to put all that data you will sort, so you will be creating two folders in the data directory of your course: one folder for 'Diseased' and one folder for 'Controls'. 

2. To create these directories, click on the data directory
if it is not already open, so that you can see all the files and subdirectories within (the data directory should also be highlighted).
At the top of the menu, there are two buttons for adding something to your directory: new file and new folder. "New file" looks like
a sheet of paper with a `+` in the lower-right corner,
while "New folder" looks like a file-folder with a `+` in the
lower-right corner. 

3. You will click on the button for New Folder and name it 'Diseased', then create another folder and name it 'Control'. Make sure these two folders are under the Data directory! Wherever your highlight is, that is where the new folder will go under!

4. Double check that your two folders went under the Data directory.

Another way to create your folders is using the command line, which you have been learning about throughout this course! If you'd like to try out this option, delete one or both of your folders and give it a shot!

1. Open your terminal within VSCode.

2. Next, use the command `cd` and write the path to your Data directory.

3. Once you are in the Data directory, use the `mkdir` command, followed by the name if your file (Diseased, and Controls).

4. To make sure the files are there, use the command `ls` and look for your `Diseased` and `Control` folders.

5. Now that you have created the folders, you need to start sorting them! By now, there should be 10 samples stored in the Data folder of this course. Open each sample and mark it as either Diseased or Control, then put it in the corresponding folder.

6. Once you have sorted your 10 FASTQ files into the "Diseased"
and "Control" folders, your task will be to find more samples
related to your topic. The goal is to have 100 samples total,
50 for Diseased and 50 for Controls.


# TODO
* Separate into control and diseased groups
    - Tag samples from the metadata
    - Also could be in the name when doing the search
    - Look inside PRJDB9292(BioProject) • DRP008133(SRA Study) • All experiments • All runs( This is what we want)
        - COMMENT: PRJDB9292 is an amplicon project, whereas we've told
            the students to look for WGS?
        - MetaData button in here - Consistent data for most projects
        - Side Note: They all get the same name when downloaded. Rename them ASAP so that you don't lose your data from ambiguous names. MENTION IT AGAIN
* Mention word wrap in the view menu and rainbow CSV extension 
* Roughly 1 GB per 10 samples (Have students check their space on their computer)
* Need minimum of 100 samples, 50 from each group. (Can we do this from one paper?)


