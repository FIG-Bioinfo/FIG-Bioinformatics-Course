# Sample Set Creation Sorting Data 

Objective: Sort your gathered data into diseased and control groups, then gather more samples.

Now that we have gathered all the data we need, it's time to make the data useable for our machine learning model. In order to create an accurate (can't remember the word), the machine learning model will need to know what data is from diseaed patients and what data is a control.

## Materials
[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)
[NCBI](https://www.ncbi.nlm.nih.gov/)
[SRAToolkit Download FASTA Documentation](https://www.ncbi.nlm.nih.gov/books/NBK242621/)

```
FIG-Bioinformatics-Course/
    ├── 3_Projections
        └── 3.1_Sample-Set-Creation/
            └── Sample-Set-Creation Exercise-2_Sorting_Data.md (you are here)
    Data/
```
In previous lessons, we have used FastQ and FastA files when it comes to our data. You might have been wondering what the difference is between the two! In previous excercises, we read files in FastA format. For sequencing data, we use FastQ format, which contains information about sequence quality in addition to sequence data.

In preperation for this exercise, you will need to check the storage space on your computer. If you are working on Mac, you can click on the Apple incon in the top left of your screen and bring up the "About This Mac" window. If you are working on Windows, (incude windows instructions). To have room for all the samples, you will need approximately 10 GB.
In addition to the space on your computer, your reading of the FASTQ files will be much eaiser with an extension called Rainbow CSV. If you don't have it already installed, search it up in the extensions tab in your VSCode.

*Another helpful tool for viewing this course and the files is Word Wrap, which can be toggled under the View setting at the top of your screen.

## Exercise

*ALWAYS RESET YOUR PATH* 

Type `source ~/.bashrc` into your command line to reset your path to the Course directory before starting each exercise.

1. In this lesson, you will be downloading more data, then sorting it into two categories. You will need places to put all that data you will sort, so you will be creating two folders in the data directory of your course: one folder for 'Diseased' and one folder for 'Controls'. This classification is based on the metadata of the samples, which you will be using to sort the data.

2. To create these directories, click on the Data directory so you can see all the files and subdirectpries within (the Data directory should also be highlighted). At the top of the menu, there are two buttons for adding something to your directory: new file and new folder.

3. You will click on the button for New Folder and name it 'Diseased', then create another folder and name it 'Control'. Make sure these two folders are under the Data directory! Wherever your highlight is, that is where the new folder will go under!

Another way to create your folders is using the command line, which you have been learning about throughout this course! If you'd like to try out this option, delete one or both of your folders and give it a shot!

1. Open your terminal within VSCode.

2. Next, use the command "cd" and write the path to your Data directory.

3. Once you are in the Data directory, use the "mkdir" command, followed by the name if your file (Diseased, and Controls).

4. To make sure the files are there, use the command "ls" and look for your "Diseased" and "Control" files.

## Sorting the Data

1. Now that you have created the folders, you need to start sorting it! We will be practicing sorting by using the example sample SRR11575976.

2. Open https://www.ncbi.nlm.nih.gov/. We will be using this website to find the metadata of each of the samples to try and determine which samples are diseased and which are controls. 

3. Find one of the samples in the Data folder and copy the SRA run accession number. Paste it into the search bar of the NCBI website. It will give you a Results Found page. Click on the name of the sample to go to the sample page. Usually it is a larger bold heading inside the Results Found box.

4. This next page shows you all of the information that was used in processing the sample. Who submitted it, what type of process was used, and what organism was sequenced. We are looking for how the sample was classified and unfortunately that information is not available here. However do take note that the information on this page should be consistent for most of your data. 

5. While looking at the sample page for SRR11575976, you will notice that there is a heading called "Sample: SpHC". Underneath that heading there are a few links. We need to get to the SRA Run Selector by clicking on the "All runs" link. 

6. Once you are on the SRA Run Selector page, you will see a list of all the runs that were used to process with that sample.Basically it is all the data used during that experiment or study. Notice in the "Select" box that there is a Download column with a "Metadata" button. Click that button to download the needed metadata.

**Something important to note is that not every run will have a metadata button. Some studies do not submit a paper or metadata with their data. Therefore if you do not see this button, it will be significantly harder to classify your data** 

7. The data will download into a file called "SraRunTable.csv" in your downloads folder. Open this file to see all of the metadata we know about the sample. If you cannot find the downloaded file mentioned, look in the Data directory to find the SraRunTable.csv file for SRR11575976.

**WARNING: The SraRunTable.csv file ALWAYS DOWNLOADS WITH THE SAME NAME. This means that if you download another sample, you will overwrite the SraRunTable.csv file for the previous sample. This is why you should always rename your files as soon as you download them!**

8. There are 37 columns in this file. Each describing a different detail about our data. But we only are interested in one thing: disease or control status of this sameple. Not every table is the same. Some will have hundreds of columns, some will have a few, and none of the data that is kept inside the metadata table is consistent. Therefore, it is ENTIRELY POSSIBLE that you will get to this point and not be able to determine disease status. Thankfully, SRR11575976 has a column called "host_disease", so we can use that to determine disease status.

9. The column "host_disease" says that it is a Healthy Control sample. Therefore, SRR11575976 would be sorted into the Control folder.

10. Note that this sample was a FASTA file for a Parkinson's research model. Therefore unless your topic is Parkinson's, you might not want to include it in your Diseased and Control folders for your model. Also, you will want to have high quality samples moving forward. Therefore, we are going to switch our focus from FASTA to FASTQ files.

FASTQ files have the same data as FASTA files but also include more metadata about the sample. It tells how well each of the reads were sequenced and how much of the sample is of high quality. Considering the better the quality of the sample, the more accurate your model will be, you will want to use FASTQ files moving forward. These files are found in the same SRA Run Selector page as the FASTA files and are labeled as the "FASTQ" button.

11. Sort through your data and try to determine the control or disease status of your data. If you are unsure what the status is of a specific sample, remove it from your data and find a new sample. This is a tedious part of the work, but neglecting this step means that your model will not be accurate.


 Open each sample and mark it as either Diseased or Control, then put it in the corresponding folder.

6. Once you have sorted your 10 FASTQ files, your task will be to find more samples related to your topic. The goal is to have 100 samples toal, 50 for Diseased and 50 for Controls.


