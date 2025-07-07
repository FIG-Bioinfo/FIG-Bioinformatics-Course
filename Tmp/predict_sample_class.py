import sys
import argparse
import pandas as pd
import numpy as np
import pickle
from scipy.stats import gmean
from scipy.optimize import curve_fit

# Argument Parsing
parser = argparse.ArgumentParser(description="Predict whether samples belong to disease or control group using a trained classifier.")
parser.add_argument("-C", "--classifier-file", type=str, required=True, help="Filename of the pickled classifier.")
args = parser.parse_args()

# Print progress message to STDERR
sys.stderr.write(f"Loading classifier from {args.classifier_file}...\n")
sys.stderr.flush()

# Load trained classifier
with open(args.classifier_file, "rb") as f:
    clf = pickle.load(f)

sys.stderr.write("Classifier loaded successfully.\n")
sys.stderr.flush()

### **Read Data from STDIN**
sys.stderr.write("Reading input data from STDIN...\n")
sys.stderr.flush()

# Read TSV data from STDIN
df = pd.read_csv(sys.stdin, sep="\t")

# Drop genome_name (not needed for classification)
df = df.drop(columns=["genome_name"])

# Ensure correct data types
df["sampleID"] = df["sampleID"].astype(str)
df["genome_id"] = df["genome_id"].astype(str)
df["score"] = df["score"].astype(float)
df["num_roles"] = df["num_roles"].astype(int)

### **Adaptive Threshold Selection (Same as Training) ###
def fit_power_law(scores):
    """Fits a Zipf/Pareto distribution to genome scores and finds threshold."""
    def power_law(x, a, b):
        return b * x ** (-a)

    x = np.arange(1, len(scores) + 1)
    y = np.sort(scores)[::-1]  # Sort in descending order

    try:
        popt, _ = curve_fit(power_law, x, y, maxfev=10000)
        alpha = popt[0]  # Exponent of power law
        cutoff = np.nanpercentile(scores, 100 * (1 - 1/alpha))  # Tail cutoff
    except:
        cutoff = np.nanpercentile(scores, 90)  # Fallback threshold

    return cutoff

### **Feature Extraction (Same as Training) ###
features = []
sample_groups = df.groupby("sampleID")

sys.stderr.write("Extracting features from input samples...\n")
sys.stderr.flush()

for sample, group in sample_groups:
    scores = group["score"].values
    num_roles = group["num_roles"].values

    # Determine adaptive threshold
    threshold = fit_power_law(scores)

    # Extract significant genomes
    significant = scores[scores >= threshold]
    high_confidence = scores[num_roles >= 4]  # Confidence-based filtering

    # Compute feature values using geometric mean
    mean_significant = gmean(significant) if len(significant) > 0 else 0
    mean_high_conf = gmean(high_confidence) if len(high_confidence) > 0 else 0

    num_significant = len(significant)  # How many genomes exceed threshold?
    num_high_conf = len(high_confidence)  # Count of confident genomes
    score_entropy = -np.sum((scores / np.sum(scores)) * np.log2(scores / np.sum(scores)))  # Diversity metric

    # Store extracted features
    features.append([sample, num_significant, mean_significant, num_high_conf, mean_high_conf, score_entropy])

# Convert features into a DataFrame
feature_df = pd.DataFrame(features, columns=["sampleID", "num_significant", "mean_significant", "num_high_conf", "mean_high_conf", "score_entropy"])

# Predict disease/control for each sample
sys.stderr.write("Making predictions...\n")
sys.stderr.flush()

X = feature_df.drop(columns=["sampleID"])  # Remove non-feature columns
predictions = clf.predict(X)

# Add predictions to feature_df
feature_df["prediction"] = predictions  # 1 = disease, 0 = control

# Output predictions as TSV
sys.stderr.write("Writing predictions to STDOUT...\n")
sys.stderr.flush()

feature_df[["sampleID", "prediction"]].to_csv(sys.stdout, sep="\t", index=False)

sys.stderr.write("Prediction complete!\n")
sys.stderr.flush()
