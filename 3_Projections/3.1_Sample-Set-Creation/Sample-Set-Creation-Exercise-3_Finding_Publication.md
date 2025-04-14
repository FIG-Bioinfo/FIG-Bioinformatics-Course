# Sample Set Creation Exercise 3: Finding Publications

Objective: Find a publication that is relevant to your topic.

Sometimes finding data is the hardest part of getting a projection started. Especially since machine learning requires a lot of data to be effective. Therefore, we will be trying to find a publication that is relevant to your topic and then use the data from that publication to create a model.  

Many times a run of experiments are created to answer a theoretical question, or even fill out a gap in the current knowledge. This means that the data does not come from a publication, has less review, and does not necessarily need to have accurate or complete metadata before it is cataloged in the ncbi database. However publications are trying to defend their hypothesis, and therefore are more likely to have accurate and complete metadata. This is why we will be looking for an academic publication that is relevant to your topic because the data is more likely to be defined as diseased or control.

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
    └── Controls/
    └── Diseased/
```

This lesson will accomplish the same goal as the previous lesson, but it will be done in a different way. Therefore if your data is fully sorted and you have a sufficient amount of data, then feel free to move on to the next lesson.


## Exercise

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. Travel to the http://www.ncbi.nlm.nih.gov/ and search for your topic. This time, click on the PubMed link.

2. A list of papers will now show up on your screen. There are a few things to look out for and keep in mind when looking at these papers. 
    1. Many authors will write multiple papers on the same topic. When they do this, they have a tendency to reuse old data. Be sure to check against your own findings to make sure that any data you find is new. Also avoid looking into papers that share the same authors. 
    2. Not every paper shared in this search is free to the public. It is entirely possible that you will click on a link and find that you need to pay for the paper. If this is the case, move on to the next paper. 
    3. Not every paper will have a Data Availability statement. If you find a paper that does not have a Data Availability statement, you'll have to read more deeply into the paper to see if they mention a BioProject number, SRA Experiment ID, or other information mentioned from our SRA search.

3. As an example, let's look at a paper with a Data Availability statement so we know how to find it. Go to this paper. https://pmc.ncbi.nlm.nih.gov/articles/PMC9663292/

4. This paper written by Zachary Wallen among others mentions that the gut microbiome is a biomarker for Parkinson's Disease. If you scroll down through the paper, you will notice that it has a Data Availability statement. This means that the authors have made data, but it does not guarantee that the data is in the NCBI database. 

5. You'll see that the Data Availability statement mentions a BioProject ID explicitly. It also mentions the Sequence Read Archive (SRA) and gives the project number with a link attached, This is the best case scenario. It gives us multiple sources of information we can use to track down the data and its metadata. Click on the PRJNA number.

6. Scroll down to find the "Project Data" section. This gives you the number of samples in the project. Click on the number in the SRA experiments row to see the SRAs. 

7. This will give you a list of all the samples from that project in a search. Notice that this author gave us the courtesy of labelling each sample with the disease state in its name. Not every author will do this, so I am going to continue to find the metadata. Plus it will make our lives easier when we are sorting the data later. 

8. If you click on a single sample and see the Study, Sample, Library, and Runs sections. This page has everything we want. The metadata for the process, information on collection, and even all the metadata in a list. But we need to be able to download the metadata for all these samples to do research with them. Go back to the previous page where you had your search results from the full 700+ samples. 

9. Right above the search results is a white box with the option to view all of the data in an expanded table. This will take all of our search results and organize their metadata to be able to see it well. However, the more results you load in Run Selector, the longer it will take to load the entire table. Therefore, know that you will have to click that "Send results to Run selector" link and it will be a minute or two before you start seeing all of the data.

10. In this page, you can see the metadata for the processing of the samples and the metadata on content of the samples themselves. This is a great resource to use when you are searching for more data, but for now, let us download this metadata into a file that we can use. Click on the "Metadata" button to get the "SraRunTable.csv" file in your downloads folder. If your browser is not loading or the download is taking too long, you can find the file in our `Data/` directory of this course.

 Go ahead and open your new SraRunTable.csv file. Notice that you now have 700+ samples that you could use to run your model. This is the power of finding a publication that is relevant to your topic. They will do a lot of the work of sorting your data for you. 

11. Keep in mind that not every publication or academic paper will have the data you need readily available. Many will have data from an alternate source, data upon request, repeated data from a previous publication, or contextualize their data into graphs that are hard to parse. This makes it harder in general to find data through publications and requires more complex problem solving to gather. Below are links to examples of some papers on the Parkinson's Disease topic that have less optimal data availability. Use this to help determine if the publications you find are suitable for your needs.
    1. https://pubmed.ncbi.nlm.nih.gov/39955398/
    2. https://pubmed.ncbi.nlm.nih.gov/39955039/
    3. https://pubmed.ncbi.nlm.nih.gov/39954969/
    4. https://pubmed.ncbi.nlm.nih.gov/39954798/
