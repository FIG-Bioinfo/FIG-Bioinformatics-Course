# Machine Learning Classifier Exercise 1 - Run the Classifier

Objective: Learn how to run a random forest classifier on genomic data and interpret the results.

This lesson will be the beginning steps of creating a machine learning model. We will be using the xmatrix that we created in the previous unit to train a random forest classifier. Know that whether you choose to use an xmatrix on presence and absence or scaled for population, the process is relatively the same. 

## Materials

* [Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

* [Scikit-learn Random Forest Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)

* [Pandas DataFrame Documentation](https://pandas.pydata.org/docs/reference/frame.html)

* [NCBI](https://www.ncbi.nlm.nih.gov/)

* [SRAToolkit Download FASTA Documentation](https://www.ncbi.nlm.nih.gov/books/NBK242621/)

```
FIG-Bioinformatics-Course/
├── 3_Projections
│   └── 3.3_Machine-Learning-Classifier/
│       └── Machine-Learning-Classifier-Exercise-1_Run_the_Classifier.md (you are here)
└── Data/
    └── xmatrix.tsv
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

1. Start by asking Grimoire to describe how a random forest classifier works and how it is used in machine learning.

2. Open a new file in your `Code` folder and name it `run_classifier.py`. This will be the file that we use to run our classifier. 

3. Next we are going to go through the code of the machine learning program to put into this file. This lesson will be focusing on the process inside of the code to help explain how the machine learning model works. At any point in this lesson, you are encouraged to run your program to see what it does to the data and how it effects the output. At the top of `run_classifier.py` we need to import the necessary libraries. copy and paste the following code into your file:

```
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
```
From top to bottom, the libraries that we are importing are:

- `pandas` is a library that we are using to read in our data and keep it's structure.
- `sklearn` is a library that we are using to create our machine learning model and evaluate it's success.
- `RandomForestClassifier` is the object that creates our random forest classifier. This is the core of our machine learning model.
- `train_test_split` is a function that splits our data into training and testing sets. This ensures that we can evaluate the accuracy of our model.
- `accuracy_score`, `classification_report`, and `confusion_matrix` are variables we use to evaluate the metadata of our model.

4. Now we need to load in our xmatrix.tsv file that we created in the previous unit. We will use pandas to read in the file and keep the structure of the data to the columns and rows of the xmatrix. The new type of data that we are using is called a `DataFrame`. Copy and paste the following code into your file:

```
xmatrix = pd.read_csv("Data/xmatrix.tsv", sep="\t")
```
This line of code reads in the xmatrix.tsv file from the `Data` folder and keeps the structure of the data to the columns and rows of the xmatrix as a dataframe. If you want to see what a dataframe is, you can use the statement `print(xmatrix)` to print the dataframe to the terminal. That will show you how the data is structured for use in the next steps.

5. The next step is to split our data into training and testing sets. A training set is the data that the model uses to train itself on what the patterns might be to make a prediction. It is usually a large portion of the available data and includes the target variable(the variable that we are trying to predict) so the model can learn what the correct answer is. The testing set is a smaller set of data that then has no target variable attached so that the model does not know the correct answer. This testing set is then run through the model to make predictions. If the model gets those predictions correct, then we have a successful model and quality data. This is a crucial step in machine learning because it allows us to evaluate the accuracy of our model. Anything below 90% accuracy is not a good model and should be reevaluated for more tuning. So first we need to separate the target variable from the rest of the data to get it ready for the training and testing sets. Copy and paste the following code into your file:

```
X = xmatrix.drop(columns=["Disease Label"], axis=1)
y = xmatrix["Disease Label"]
```
This code separates the target variable from the rest of the data into the `y` variable. The target variable is the variable that we are trying to predict, in this case it is the `Disease Label`. The rest of the data is stored in the `X` variable.

6. Now we need to split the data into training and testing sets that we can then put into the model. The function `train_test_split` takes in four arguments: the features, the target variable, the test size, and the random state.

- The features are the data that we are using to make a prediction, in this case it is all of the genomes in the xmatrix labeled as `X`.
- The target variable is the variable that we are trying to predict, in this case it is the `Disease Label` we stored in the `y` variable.
- The test size is the portion of the data that will be used for the testing set in decimal form. So 0.2 would be 20% of the data and we would recommend not going any higher than that as the training set needs to be large enough to train the model.
- The random state is the seed for the random number generator and is used to make the split reproducible.

This function will give us four variables: `X_train`, `X_test`, `y_train`, and `y_test`. These variables are the training and testing sets for the features and target variable. Basically, the `X` and `y` variables we created earlier are being split into our training and testing versions of the same data. We will now use the `train_test_split` function to split the data. Copy and paste the following code into your file:

```
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
7. We can now create our random forest classifier. When creating a random forest classifier, we need to specify the number of trees in the forest and the maximum depth of each tree. This tells the model how many threads to create when making predictions while also deciding how many choices are for each tree. Ideally, we want to use as many trees as possible while also not having a maximum depth so that the trees can grow as large as possible. However this can create an algorithm that can be too slow to run and might not even be the best model for our data. Therefore we will want to start with a basic depth and tree count and then tune it from there. We will use 100 trees and no maximum depth. Copy and paste the following code into your file:

```
clf = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
```

8. Now we can train our model to teach it the patterns in the data to make predictions. We will use the `fit` method to train the model and create the trees it will use to make predictions. Copy and paste the following code into your file:

```
clf.fit(X_train, y_train)
```

9. At this point, our model has been trained and is ready to make predictions. So any data we put into the model will have to have the same structure as the training data. Luckily we pulled some data out in step 6 that we can use to test our model. We will use the `predict` method to make predictions on the testing set but not yet check to see if they are correct. We do not want the model to know the correct answer and skew the results. Copy and paste the following code into your file:

```
y_pred = clf.predict(X_test)
```

10. The variable `y_pred` now contains the predictions that the model made on the testing set. If the model is 100% accurate, the `y_pred` variable will be exactly the same as the `y_test` variable. If you printed them both out at this point, you would be able to see the same information printed out for each row. But we don't have to do it with our eyes when the model already can do that for us. We will use the `accuracy_score`, `classification_report`, and `confusion_matrix` functions to calculate the accuracy of the model. Copy and paste the following code into your file:

```
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

11. We could stop there and have a working model. But we would have to look at the terminal output to see how well the model is doing. We can print the results in a more readable format for later. Let's put it into a file and name it `model_results.txt`. Copy and paste the following code into your program to do just that:

```
with open("model_results.txt", "w") as file:
    file.write("Model Results\n")
    file.write(f"Accuracy: {accuracy_score(y_test, y_pred)}\n")
    file.write(f"Classification Report: {classification_report(y_test, y_pred)}\n")
    file.write(f"Confusion Matrix: {confusion_matrix(y_test, y_pred)}\n\n")
```
