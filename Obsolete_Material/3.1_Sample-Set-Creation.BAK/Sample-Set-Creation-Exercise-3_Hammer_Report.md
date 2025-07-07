# Sample Set Creation: Generating Hammer Reports

**Objective:** Create a report of the genomes present inside of a sample to insert into your data set. 

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
        └── Sample-Set-Creation Exercise-3_Hammer_Report.md (you are here)
```

## Exercise

*ALWAYS RESET YOUR PATH* 

Type `cd $COURSE_DIR` into your command line to reset your path to the Course directory before starting each exercise.

1. From the data set that you sorted from the previous exercise, choose one control sample that you want to look into. We will be referring to this sample as "Control Sample A" for the purposes of this exercise. It is recommended that you do not change the name of this sample, as it will be used in your model and keeping the SRA ID number in tact will allow you to more easily keep track of its metadata and origins for the model.

2. Open up your `hammer_compare.py` program and look at its input and output requirements. We will be using our sample FASTA file as our input and the output will be a list of genomes that are present in our sample. Give your program to Grimoire and ask it to adjust the program to take a FASTA file as input and output a list of genomes that are present in our sample as a tsv file. 

3. Take your adjusted `hammer_compare.py` program and use it to generate a report for "Control Sample A". 

4. Now comes the tricky part. You will need to look at your output and see if you can identify where the genomes that are present in the sample end and where the noise begins in your sample. So we need a true read on what is actually in the sample to help us determine where that boundary is. To do this, we will be using a few tools in the bv-brc software suite. Ensure you have the bv-brc cli installed on your system. 



  ** Note: If your data is an AMPLICON data type and not a Whole Genome Shotgun data type, you will be seeing less genomes in your report than our example. This is because your data is processed with a cheaper method and therefore does not capture as much data when it is being processed in the lab. Please keep this in mind when following along with the rest of the lesson.**

5. There are 3 steps to the metagenomic binning process. We will be performing these steps on "Control Sample A".
    1. Trimming: This step will remove the start and end sequences from your sample that are used in the lab to help the machine read the sample. Think of it like a cipher that the computer needs to know what each of the proteins are so it can read the sample.
    2. Assembly: This step will take the trimmed sample and put both sides of the genome back together again. The end of this step will be contigs of the paired reads.
    3. Binning: This step will take the assembled sample and identify the genomes that are present in the sample. It will also tag a "reference genome" that acts similarly to the representative genome in a taxonomic tree. We will be using these reference genomes to find where the genomes in our sample map to the representative genomes you created in your first unit.

6. First we will perform the trimming step on "Control Sample A". We will be using the `p3-submit-fastqutils` command to do this. It has quite a few activities that it can perform, but we will be using its trimming and quality control features. The command calls flags as follows:
    - First we call the SRA ID of the sample to pull it directly from the NCBI SRA database.
    - We then call the `-trim` flag to tell the program that we want to trim the sample.
    - Next we call the `-fastqc` flag to tell the program that we want to know the quality of the trimmed sample.
    - Finally, we tell the program where we want to output the trimmed sample and the fastqc report as well as what to name it.

    ```
    p3-submit-fastqutils --srr-id SRAControlSampleA -trim -fastqc Data/TrimmedControlSamples trimmed_control_sample_a
    ```

7. When this is finished, we will have 2 trimmed fastq files called `trimmed_control_sample_a_1_ptrim.fq.gz` and `trimmed_control_sample_a_2_ptrim.fq.gz`. These are the two sides of DNA strands that were sequenced in the sample. We now need to assemble them into contigs so that they can be binned. Technically, we could go straight to the binning step from this point as the metagenomic binning software also has an assembler built in. However the quality of that assembly will not be as good since it was not made specifically for that purpose. Therefore do the following command to assemble the sample.

    ```
    p3-submit-genome-assembly --paired-end-lib Data/TrimmedControlSamples/trimmed_control_sample_a_1_ptrim.fq.gz Data/TrimmedControlSamples/trimmed_control_sample_a_2_ptrim.fq.gz Data/AssembledControlSamples/ assembled_control_sample_a
    ```
    - First we call the `p3-submit-genome-assembly` command to tell the program that we want to assemble the sample.
    - Next we call the `--paired-end-lib` flag to tell the program where to find the two sides of the DNA strands that were trimmed in the previous step.
    - Finally we tell the program the folder and file name that we want to use to output the assembled sample.

8. When this is finished, we will have a single fasta file called `assembled_control_sample_a_contigs.fasta`. This is the assembled sample. I know what you're thinking, "But we already had a fasta file we could use when we downloaded from the ncbi!" And that is almost true. That sample would have given us some false hammer hits from the shotgun sequencing process that we trimmed off in step 1. Without trimming and assembly, we are not able to get a true read on what is actually in the sample and will have a lot more noise in our data than before. If you are curious about the difference in quality between trimming, assembly, and binning, versus just binning, feel free to repeat this next step with your originally downloaded sample and see how the quality changes. You can also use the SRR-ID of the sample at any point in these steps to perform the same operations. 

9. We now need to bin our sample to identify the genomes that are present in the sample. Time to call the `p3-submit-metagenome-binning` command.

    ```
    p3-submit-metagenome-binning -contigs Data/AssembledControlSamples/assembled_control_sample_a_contigs.fasta Data/BinnedControlSamples binned_control_sample_a
    ```

    - First we call the `p3-submit-metagenome-binning` command to tell the program that we want to use the metagenome binning algorithm to bin the sample.
    - Next we call the `-contigs` flag to tell the program we only want to bin the contigs and not use any trimming or assembly in this step.
    - Finally we tell the program the folder and file name that we want to use to output the binned sample.

10. When this is finished, we will have a file called `BinningReport.html` and a bunch of .fa files that start with the prefix `bin`. Open up the `BinningReport.html` file and look through it to see the genomes that are present in the sample. This information is what we will be using to compare to our hammer report. However the bv-brc does not know what your representative genomes are, so we will have to connect the dots between the genomes in the `BinningReport.html` to the genomes in your `HammerReport.tsv` file by using our representative genome set. For now, look at the count of how many genomes are in the sample. That number will be right around the same number of genomes that are 'true' to the sample in your hammer report as well. 

11. The bin report currently contains a lot of information as well as html formatting. We will need to parse this report to get the information we need like the genomes and their reference genomes. Open up the `parse_binreport.py` program and look at its input and output requirements. We will be using our `BinningReport.html` file as our input and the output will be a list of genomes that are present in our sample. Give your program to Grimoire and ask it to adjust the program to fit your requirements. Be sure to mention that it uses the "BeautifulSoup" library to parse the html.

12. Take your adjusted `parse_binreport.py` program and use it to generate a report for "Control Sample A". Ask Grimoire to create a program that will find the representative genome for each reference genome in the `BinningReport.html` file. This will give you a list of the genomes that are present in the sample that you can then compare to your hammer report. Name this file `reference_representative_compare.py` and place it in the `Code` folder of this course.

13. Run your `reference_representative_compare.py` program to generate a report of the genomes that are present in the sample. This will give you a list of the genomes that are present in the sample that you can then compare to your hammer report. Use this list to determine where the 'noise' starts in your sample and use that as your cutoff point of hammer hits for the genomes in your sample. It should be the minimum nmber of hammer hits that a genome must have to be considered present in the sample. This cutoff point will be consistent across all of your samples and will help you to classify the samples in your dataset.

14. Now that you have your cutoff point identified, you will need to use your `hammer_compare.py` program to generate a report of the genomes that are present in each of your healthy and diseased samples. Do not worry about creating more trimming, assembly, or binning reports for the rest of the samples. That was only to determine the cutoff point. However it is good practice to confirm your work so that you are confident in your results. We recommend completing this process for at least 10% of your samples to confirm that your cutoff point is working.

15. Finish creating the hammer reports for the rest of your samples. We will be using these reports in the next exercise. 