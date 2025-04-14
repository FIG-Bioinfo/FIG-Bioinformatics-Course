# Creating the XMatrix: Universal Template

Objective: Create the universal table and template for the data with the columns pre-populated.

Now that you have curated your data, the next step is to create a universal XMatrix template. This template will serve as the foundation for organizing your genomic data in a structured format, which is essential for subsequent analysis and machine learning applications. Once we have our template and populate it with data, we can begin to explore the data and find patterns that we can use to classify new samples.

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
├── Code/
│   ├── xmatrix_feature_set.py
│   └── xmatrix_populate_samples.py
└── Data/
    ├── Controls/
    └── Diseased/
```

## Exercise

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-windown if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

The idea of the random forest classifier is that it takes a large number of decision trees and averages their results. Each decision tree looks at a random subset of the data and makes a prediction. The more trees there are, the more accurate the prediction is. This means that we need to give the machine learning algorithm a large set of data so that it can make more decision trees which gives us a more accurate prediction. 

This is where your hammer reports come in. Each report contains a list of genomes that are present in the sample. We need to create a table for our classifier that contains every possible genome that we have in our dataset. Luckily, we already have a list of all the genomes that could possibly show up in our dataset with the representative genome set. We will use the complete list of genomes in our representative genome set as our column headers for the XMatrix since those are the only ones that can be present. In traditional data science, the columns of the XMatrix are called features. So another name for our representative genome set is the feature set for our model.  The rows of the xmatrix will be the contents of each individual sample and is our data set. 

Your goal is to create a blank xmatrix template with the feature set (representative genome set) as the columns and the samples as the rows. As an example, you can look up the `Data/xmatrix_empty_example.tsv` file to see an example of what your xmatrix should look like.

1. Firstly, we need to curate our feature set. Open `Data/xmatrix_features_example.tsv` and look at the first row. This is the feature set of our model and has two columns that are not genome IDs. The first column is called "sample" to leave room for the SRA run accession number from each of our hammer reports. The last column is called "disease label" and is our target variable; diseased or control. Feel free to change the name of this column to your project's target variable name.

2. Now open `Data/rep10.list.tbl` and look at the first column. This is the list of genome IDs that we will be using as our feature set. This, as well as "sample" and "disease label" need to become the columns of your xmatrix. 

3. Write a prompt for Grimoire to write a program called `xmatrix_feature_set.py` that will take as input the `Data/rep10.list.tbl` file and use the genome ids to create a new file called `Data/xmatrix.tsv`. Don't forget to add a "Sample" column to the beginning of the row and your "disease label" column to the end of the row. Use `Data/xmatrix_features_example.tsv` as an example of what your goal should look like. 

4. Run your program and confirm that the xmatrix is populated correctly with all of your features. You can do this by checking that the number of columns in the xmatrix is equal to the number of genome IDs in your rep10.list.tbl file + 2 for your extra columns. 

**If you are missing a genome ID, you can add it from the `Data/rep10.list.tbl` file**

5. Now we need to populate the xmatrix with the SRA run accession numbers from each of our hammer reports. We will do this by writing a program that looks at the names of the files in the `Data/Controls` and `Data/Diseased` directories and extracts the SRA run accession numbers. If you have grabbed your data from a publication and have a metadata table, you can instead copy the SRA run accession numbers from the first column of the metadata table and paste them into the "Sample" column of the xmatrix.

6. Write a prompt for Grimoire to write a program called `xmatrix_populate_samples.py` that will take the names of the files in the `Data/Controls` and `Data/Diseased` directories and extract the SRA run accession numbers. Use `Data/xmatrix_empty_example.tsv` as an example of what your goal should look like. You will most likely need to program in the absolute path of both directories, and use the `os` library to iterate through the files. It is also recommended to create a new file as a copy from your old xmatrix file so that you can compare the new xmatrix to the old one and repair from any errors that may occur.

7. Run your program and confirm that the xmatrix is populated correctly with all of your samples. You can do this by checking that the number of rows in the xmatrix is equal to the number of samples in both Control and Diseased directories combined. Also you can check the first column of the data to ensure that it is labeled correctly.

**If you are missing a sample, you can add it's SRA run accession number from the `Data/Controls` and `Data/Diseased` directories directly to the xmatrix.**

## Self-Check
Audit your `xmatrix.tsv` file to ensure that it is populated correctly. 
1. Pick 10 of your samples and check that they are included in the xmatrix. 
2. Check that the first column is labeled correctly and that the last column is labeled correctly (Samples and Disease Label).
3. Pick 5 Control samples from your directory and make sure that they are labeled as Control in the xmatrix's last column.
4. Pick 5 Diseased samples from your directory and make sure that they are labeled as Diseased in the xmatrix's last column.
5. Pick 10 genome IDs from the middle of `Data/rep10.list.tbl` and check that they are included in the xmatrix.
6. Look at the formatting in `Data/xmatrix_empty_example.tsv` and ensure that your xmatrix is formatted the same way. 





