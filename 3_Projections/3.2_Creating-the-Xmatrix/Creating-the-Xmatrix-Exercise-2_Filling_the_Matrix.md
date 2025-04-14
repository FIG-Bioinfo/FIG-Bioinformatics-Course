# Creating the XMatrix: Filling the Matrix

Objective: Fill the universal template with the correct data.

Now that we have an xmatrix template, we can populate it with the presence or absence of the genomes in each sample making our dataset ready for machine learning. After we have the xmatrix populated, we can then explore it programmatically to find the best parameters for our model. And hopefully tease out a pattern that we can use to classify new samples.

## Materials

* [Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

* [NCBI](https://www.ncbi.nlm.nih.gov/)

* [SRAToolkit Download FASTA Documentation](https://www.ncbi.nlm.nih.gov/books/NBK242621/)

* [BV-BRC](https://bv-brc.org/)

* [BV-BRC CLI Reference Documentation](https://www.bv-brc.org/docs/cli_tutorial/command_list/index.html)

```
FIG-Bioinformatics-Course/
├── 3_Projections/
│   └── 3.2_Creating-the-Xmatrix/
│       └── Creating-the-Xmatrix-Exercise-1_Universal_Template.md (you are here)
└── Data/
    └── Controls/
    │   └── hammer_report_controls.tsv
    └── Diseased/
        └── hammer_report_diseased.tsv
```

## Exercise

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.


1. We will now need to populate the xmatrix with the presence or absence of the genomes in each sample. We will do this by using the hammer reports for each sample and populating them into the xmatrix. Using Grimoire to support your work, write a program that will take a hammer report and populate a new row in the xmatrix for each sample. It must have the following requirements:

- It must take the hammer reports from two directories, one for the controls and one for the diseased.
- It must open up each file in that directory and read the sample's genome data. This is recommended to be done with a dictionary data structure to maximize the look up speed.
- It must then populate the xmatrix template with the presence or absence of the representative genomes in each sample by using 0 for absent and 1 for present. (This voting structure may not be the best for your specific model, but it is a good place to start.)
- The first column of the xmatrix should be the sample name.
- The last column should be the label for the sample, either 'control' or 'diseased'. (This information is called the target variable in machine learning. It is the variable that we are trying to predict and will be used explicitly in our model's metadata.)

3. Run your program and confirm that the xmatrix is populated correctly with all of your samples. You can do this by checking that the number of rows in the xmatrix is equal to the number of samples in each directory. Also you can check the last column of the data to ensure that it is labeled correctly.

4. We have now created a table of data that includes all of the information that we need to begin our machine learning analysis. Save the file as `xmatrix.tsv`. We will be using this file in the next exercise.

## Self-Check
Audit your `xmatrix.tsv` file to ensure that it is populated correctly. 
1. Pick 10 of your samples and check that the number of 1s and 0s in the columns are correct. 
2. Check that the first column is labeled correctly and that the last column is labeled correctly (Samples and Disease Label).
3. Check that the number of rows in the xmatrix is equal to the number of samples in each directory.






