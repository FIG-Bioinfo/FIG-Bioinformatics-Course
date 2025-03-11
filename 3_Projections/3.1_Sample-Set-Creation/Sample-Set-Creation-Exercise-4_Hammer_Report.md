# Sample Set Creation: Generating Hammer Reports

Objective: Create a report of the genomes present inside of a sample to insert into your data set. 

Now that you have a set of samples to work with, you need to create a Hammer Report for each sample. This report will contain a list of all the genomes that are present in the sample based on the hammers that are comtained within that sample. Keep in mind that depending on how well tuned your hammers are, you may get some genomes that are not actually present in the sample, but are instead fragments that create "noise". Feel free to adjust your hammer set to improve the quality of your data at any point from here on out based on accuracy, worthiness, and precision. 

Optimally, we will want to create a Hammer Report for each of our samples. Make sure that while you are creating your hammer reports, you are keeping them organized by diseased and healthy samples. This will make it easier for you to insert them into your model later on.

## Materials
[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)
[NCBI](https://www.ncbi.nlm.nih.gov/)
[SRAToolkit Download FASTA Documentation](https://www.ncbi.nlm.nih.gov/books/NBK242621/)
[BV-BRC](https://bv-brc.org/)
[BV-BRC CLI Reference Documentation](https://www.bv-brc.org/docs/cli_tutorial/command_list/index.html)

```
FIG-Bioinformatics-Course/
├── 3_Projections
    └── 3.1_Sample-Set-Creation/
        └── Sample-Set-Creation Exercise-4_Hammer_Report.md (you are here)
```

## Exercise

*ALWAYS RESET YOUR PATH* 

Type `source ~/.bashrc` into your command line to reset your path to the Course directory before starting each exercise.

1. From the data set that you sorted from the previous exercises, choose one control sample that you want to look into. We will be referring to this sample as "Control Sample A" for the purposes of this exercise. It is recommended that you do not change the name of this sample file to Control Sample A, as it will be used in your model and keeping the SRA ID number in tact will allow you to more easily keep track of its metadata and origins for the model. To help you keep track of this sample, you can search for every instance of "Control Sample A" through VSCode. To do this, go to the left hand navigation bar and click on the search icon below the file explorer icon. You can then replace each instance of "Control Sample A" with the SRA ID of the sample you have chosen using the two text boxes that appear in the search menu. Feel free to do this for every instance of "Control Sample A" in the course as it will be the same sample that you use for all exercises.

2. Open up your `hammer_compare.py` program and look at its input and output requirements. We will be using our "Control Sample A" FASTA file as our input and the output will still be a list of genomes that are present in our sample to a tsv file. Give your program to Grimoire and ask it to adjust the program to take a FASTA file as input instead of a single sequence. 

3. Take your adjusted `fasta_hammer_compare.py` program and use it to generate a report for "Control Sample A" called `Data/Controls/Control Sample A_hammer_report.tsv`. Open the file to verify that it is a list of genome IDs, genome names, and hammer scores. If you do not have any data in your hammer report, know that capital and lower case matter when matching the hammers and sequences. So make sure your adjusted program includes the `.lower()` function on the fasta sequences to make sure it matches the hammers in the `Data/myrep50.genomes.tbl` file. 

Once you confirm your data is there, notice that the list includes almost every genome id in your `Data/myrep50.genomes.tbl` file. This is because the hammer set is an approximation of the genetic data in the sample and therefore will have some false positives. We must determine where the genomes that are present in the sample end and where the noise of the false positives begins in our sample. It is not as simple as looking at a sharp dip in data, as some sequences will be incomplete or of lower quality. Therefore we need a frame of reference to determine where the noise begins.

4. We need a true read on what is actually in the sample to help us determine where that quality boundary is. To do this, we will be using a few tools in the bv-brc software suite. Ensure you have the bv-brc cli installed on your system before continuing. Our solutions and outputs were tested using the ERR1912946 SRA ID. Use that number in the Data directory to see example results of the command for the next steps. This first step will be started using the Data/ERR1912946_ptrim.fasta file in the example.

  ** Note: If your data is an AMPLICON data type and not a Whole Genome Shotgun data type, you will need to find a new data source as the hammer set will not work with Amplicon data. Please keep this in mind when following along with the rest of the lesson.**

5. There are 3 steps to the metagenomic binning process. We will be performing these steps on your "Control Sample A".
    1. Trimming: This step will remove the start and end sequences from your sample that are used in the lab to help the machine read the sample. Think of it like a cipher that the computer needs to know what each of the proteins are so it can read the sample.
    2. Assembly: This step will take the trimmed sample and put both sides of the genome back together again. The end of this step will be contigs of the paired reads.
    3. Binning: This step will take the assembled sample and identify the genomes that are present in the sample. It will also tag a "reference genome" that acts similarly to the representative genome in a taxonomic tree. We will be using these reference genomes to find where the genomes in our sample map to the representative genomes you created in your first unit.

6. First we will perform the trimming step on "Control Sample A". We will be using the `p3-submit-fastqutils` command to do this. It has quite a few activities that it can perform, but we will be using its trimming and quality control features. The command calls flags as follows:
    - First we call the SRA ID of the sample to pull it directly from the NCBI SRA database.
    - We then call the `--trim` flag to tell the program that we want to trim the sample.
    - Next we call the `--fastqc` flag to tell the program that we want to know the quality of the trimmed sample.
    - Finally, we tell the program where we want to output the trimmed sample and the fastqc report as well as what to name it. Know that this is a path on the bv-brc server, so you will need to replace the `/myusername@patricbrc.org/` path to your own username to access the job results.

    ```
    p3-submit-fastqutils --srr-id "Control Sample A" --trim --fastqc "/myusername@patricbrc.org/home" "trimmed_Control Sample A"
    ```

    If this command did not work due to the SRA being unavailable, you can use the ERR1912946_1.ptrim.fq.gz and ERR1912946_2.ptrim.fq.gz files from the Data directory to see example results of the command for the next step. 


7. When this is finished, we will have 2 trimmed fastq files called `trimmed_Control Sample A_1_ptrim.fq.gz` and `trimmed_Control Sample A_2_ptrim.fq.gz`. These are the two sides of DNA strands that were sequenced in the sample. Be sure to look inside of your bv-brc home directory in your workspace to see the `trimmed_Control Sample A_1_ptrim.fq.gz` and `trimmed_Control Sample A_2_ptrim.fq.gz` files. We now need to assemble them into contigs so that they can be binned. Technically, we could go straight to the binning step from this point as the metagenomic binning software also has an assembler built in. However the quality of that assembly will not be as good since it was not made specifically for that purpose. Therefore do the following command to assemble the sample.

    ```
    p3-submit-genome-assembly --paired-end-lib /@myusername@patricbrc.org/home/trimmed_Control Sample A_1_ptrim.fq.gz /@myusername@patricbrc.org/home/trimmed_Control Sample A_2_ptrim.fq.gz /@myusername@patricbrc.org/home/ assembled_Control Sample A
    ```
    - First we call the `p3-submit-genome-assembly` command to tell the program that we want to assemble the sample.
    - Next we call the `--paired-end-lib` flag to tell the program where to find the two sides of the DNA strands that were trimmed in the previous step.
    - Finally we tell the program the folder and file name that we want to use to output the assembled sample.

    If this command did not work due to the SRA being unavailable, you can use the ERR1912946_contigs.fasta file from the Data directory to see example results of this command for the next step.

8. When this is finished, we will have a single fasta file called `Control Sample A_contigs.fasta` in the same place that we had our trimmed files. This is the assembled sample. I know what you're thinking, "But we already had a fasta file we could use when we downloaded from the ncbi!" And that is almost true. That sample would have given us some false hammer hits from the shotgun sequencing process that we trimmed off in step 1. Without trimming and assembly, we are not able to get a true read on what is actually in the sample and will have a lot more noise in our data than before. If you are curious about the difference in quality between trimming, assembly, and binning, versus just binning, feel free to repeat this next step with your originally downloaded sample and see how the quality changes. You can also use the SRR-ID of the sample at any point in these steps to perform the same operations as long as the SRA database is available. 

9. We now need to bin our sample to identify the genomes that are present in the sample. Time to call the `p3-submit-metagenome-binning` command.

    ```
    p3-submit-metagenome-binning --contigs @myusername@patricbrc.org/home/assembled_Control Sample A_contigs.fasta --output @myusername@patricbrc.org/home/ binned_Control Sample A
    ```

    - First we call the `p3-submit-metagenome-binning` command to tell the program that we want to use the metagenome binning algorithm to bin the sample.
    - Next we call the `--contigs` flag to tell the program we only want to bin the contigs and not use any trimming or assembly in this step.
    - Finally we tell the program the folder and file name that we want to use to output the binned sample.

    If this command did not work due to the SRA being unavailable, you can use the ERR1912946_BinningReport.html file from the Data directory to see example results of this command for the next step.

10. When this is finished, we will have a file called `BinningReport.html` and a bunch of .fa files that start with the prefix `bin` inside the BV-BRC workspace. Open up the `BinningReport.html` file and look through it to see the genomes that are present in the sample. This information is what we will be using to compare to our hammer report. However the bv-brc does not know what your representative genomes are, so we will have to connect the dots between the genomes in the `BinningReport.html` to the genomes in your `Control Sample A_hammer_report.tsv` file by using our representative genome set. For now, look at the count of how many genomes are in the sample. That number will be right around the same number of genomes that are 'true' to the sample in your hammer report as well. 

11. The bin report currently contains a lot of information as well as html formatting. We will need to parse this report to get the information we need like the genomes and their reference genomes. Open up the `parse_binreport.py` program and look at its input and output requirements. We will be using our `BinningReport.html` file as our input and the output will be a list of genomes that are present in our sample. Be sure to ask Grimoire to help you install the Beautiful Soup module that this program requres. Since this is not a program you will need frequently, it has already been written for you in the Code directory.

```
python Code/parse_binreport.py Data/Control Sample A_BinningReport.html
```

If you would rather do this manually, you can copy the information from the table of "Good Bins" in the `BinningReport.html` file into a blank text file and save it as `Control Sample A_binning_report.tsv`. Ensure that you save the Genome ID, Genome Name, and Reference Genome columns in your output file as well as separating each column with a tab. This is all the information that we need to create our binning report.

**Note: If you get an error "No module named 'bs4'" when running the `parse_binreport.py` program, you will have to run the `pip install bs4` command to install the `beautifulsoup4` library**

12. Take your adjusted `parse_binreport.py` program and use it to generate a report for "Control Sample A". Name this file `Control Sample A_binning_report.tsv`. Now this file contains a very similar list of genomes to the `Control Sample A_hammer_report.tsv` file. However it is not from the same list of representative genomes and therefore will not match any of the features in our xmatrix or the list of genomes in our representative genome set. So we need to determine where our list matches with the binning report list. We can use the `Data/myrep50.genomes.tbl` file to help us determine which representative genomes are present in the sample. Theoretically, this list contains all of the genomes that are present in our known genome universe. So if we can find the genomes from the binning report in this file, we can connect them to a specific representative genome for our hammer set. This will give us an ultimate list of genomes that should be present in the hammer report.

13. Write a prompt for Grimoire to create a program that will open the `"Control Sample A"_binning_report.tsv` file and search for each representative genome in the first column of the `Data/rep10.list.tbl` file. It will then replace that genome id with the representative genome in the 6th column of that same row and count it for output in the output file of genome ids. If a genome id shows up more than once, it should add a counter to that genome id row. Name this program `binning_report_convert_to_repgen.py` and place it in the `Code` folder of this course.

14. Run your `binning_report_convert_to_repgen.py` program to generate a report of the genomes that are present in the "Control Sample A". This will give you a list of the genomes that are present in the sample that you can then compare to your hammer report. Use this list to determine where the 'noise' starts in your sample and use that as your cutoff point of hammer hits for the genomes in your sample. It should be the minimum nmber of hammer hits that a genome must have to be considered present in the sample. This cutoff point will be consistent across all of your samples and will help you to classify the samples in your dataset.

14. Now that you have your cutoff point identified, you will need to use your `fasta_hammer_compare.py` program to generate a report of the genomes that are present in each of your healthy and diseased samples. Do not worry about creating more trimming, assembly, or binning reports for the rest of the samples. That was only to determine the cutoff point for noise and verify our work. However it is good practice to confirm your work is of quality so that you are confident in your results. We recommend completing this process for at least 10% of your samples to confirm that your cutoff point is working.

15. Finish creating the hammer reports for the rest of your samples. We will be using these reports in the next Unit.