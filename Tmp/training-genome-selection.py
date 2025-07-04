########################################################################
#...Prompt that generated this program:
"""
Interactive development session;
prompt still under development.
"""

########################################################################
#...Pseudocode for this program:
"""
# Parse command-line arguments
DEFINE parser AS ArgumentParser()
ADD argument "disease_file" (TSV file containing disease sample data)
ADD argument "control_file" (TSV file containing control sample data)
PARSE arguments

# Load disease and control datasets
SET disease_df = READ_TSV(arguments.disease_file)
SET control_df = READ_TSV(arguments.control_file)

# Assign labels (1 for disease, 0 for control)
SET disease_df["label"] = 1
SET control_df["label"] = 0

# Combine both datasets
SET df = CONCATENATE(disease_df, control_df)

# Drop "genome_name" column (not needed)
REMOVE column "genome_name" from df

# Convert data types
CONVERT df["sampleID"] TO STRING
CONVERT df["genome_id"] TO STRING
CONVERT df["score"] TO FLOAT
CONVERT df["num_roles"] TO INTEGER

### Compute Summary Statistics ###
SET summary_stats = {
    "Total Samples": COUNT UNIQUE(df["sampleID"]),
    "Total Genomes": COUNT UNIQUE(df["genome_id"]),
    "Mean Score": MEAN(df["score"]),
    "Median Score": MEDIAN(df["score"]),
    "Std Dev Score": STANDARD_DEVIATION(df["score"]),
    "Mean Num Roles": MEAN(df["num_roles"]),
    "Median Num Roles": MEDIAN(df["num_roles"])
}

# Output summary statistics as TSV
PRINT "Metric\tValue"
FOR EACH key, value IN summary_stats:
    PRINT key + "\t" + value
PRINT "//"  # End of summary statistics block

### Adaptive Threshold Selection Function ###
FUNCTION fit_power_law(scores):
    SORT scores IN DESCENDING ORDER
    DEFINE power_law(x, a, b) AS b * x^(-a)

    TRY:
        FIT power_law TO scores
        SET alpha = fitted exponent
        RETURN PERCENTILE(scores, 100 * (1 - 1/alpha))  # Determine cutoff
    EXCEPT:
        RETURN PERCENTILE(scores, 90)  # Fallback threshold

### Feature Extraction ###
SET features = EMPTY LIST
SET significant_genomes = EMPTY LIST  # Store significant genomes per sample

GROUP df BY "sampleID"

FOR EACH (sample, group) IN sample_groups:
    SET scores = group["score"]
    SET genome_ids = group["genome_id"]
    SET num_roles = group["num_roles"]

    # Determine adaptive threshold
    SET threshold = fit_power_law(scores)

    # Identify significant genomes
    SET significant_indices = FIND INDICES WHERE scores >= threshold
    SET significant = scores[significant_indices]
    SET significant_genome_ids = genome_ids[significant_indices]

    # Identify high-confidence genomes
    SET high_confidence = FILTER scores WHERE num_roles >= 4

    # Compute statistical features
    SET mean_significant = GEOMETRIC_MEAN(significant) IF COUNT(significant) > 0 ELSE 0
    SET mean_high_conf = GEOMETRIC_MEAN(high_confidence) IF COUNT(high_confidence) > 0 ELSE 0
    SET num_significant = COUNT(significant)
    SET num_high_conf = COUNT(high_confidence)
    SET score_entropy = -SUM((scores / SUM(scores)) * LOG2(scores / SUM(scores)))  # Diversity metric

    # Store extracted features
    APPEND [sample, num_significant, mean_significant, num_high_conf, mean_high_conf, score_entropy] TO features

    # Store significant genome selections
    FOR EACH genome_id IN significant_genome_ids:
        APPEND [sample, genome_id] TO significant_genomes

# Convert features to structured dataset
SET feature_df = CREATE DATAFRAME(features, COLUMNS=["sampleID", "num_significant", "mean_significant", "num_high_conf", "mean_high_conf", "score_entropy"])

# Merge sample labels
SET sample_labels = DISTINCT df[["sampleID", "label"]]
SET feature_df = MERGE feature_df WITH sample_labels ON "sampleID"

# Output extracted features as TSV
PRINT feature_df AS TSV

# End of extracted features block
PRINT "//"

# Output significant genomes as TSV
PRINT "sampleID\tgenome_id"
FOR EACH row IN significant_genomes:
    PRINT row[0] + "\t" + row[1]

# End of significant genomes block
PRINT "//"
"""

########################################################################
#...Code generated by Grimoire:
import argparse
import pandas as pd
import numpy as np
import sys
from scipy.stats import gmean

# Argument Parsing
parser = argparse.ArgumentParser(description="Feature Extraction for Disease & Control Genomes")
parser.add_argument("-D", "--disease-file", type=str, required=True, help="Path to the disease dataset (TSV format)")
parser.add_argument("-C", "--control-file", type=str, required=True, help="Path to the control dataset (TSV format)")
parser.add_argument("-N", "--num-genomes", type=int, default=20, help="Number of top genomes to include as features")
args = parser.parse_args()

# Load disease and control datasets
disease_df = pd.read_csv(args.disease_file, sep="\t")
control_df = pd.read_csv(args.control_file, sep="\t")

# Assign labels (1 for disease, 0 for control)
disease_df["label"] = 1
control_df["label"] = 0

# Combine both datasets
df = pd.concat([disease_df, control_df])

# Drop genome_name (not needed)
df = df.drop(columns=["genome_name"])

# Ensure correct data types
df["sampleID"] = df["sampleID"].astype(str)
df["genome_id"] = df["genome_id"].astype(str)
df["score"] = df["score"].astype(float)
df["num_roles"] = df["num_roles"].astype(int)

### **Step 1: Filter to Keep Only `num_roles == 5`**
sys.stderr.write("Filtering genomes to keep only `num_roles == 5`...\n")
sys.stderr.flush()

df = df[df["num_roles"] == 5]

### **Step 2: Compute Read Count Features**
sys.stderr.write("Computing total read counts per sample...\n")
sys.stderr.flush()

df["total_reads"] = df.groupby("sampleID")["score"].transform("sum")
df["log_total_reads"] = np.log1p(df["total_reads"])  # log(1 + total_reads)

### **Step 3: Normalize Scores Per Sample**
sys.stderr.write("Normalizing scores by read count...\n")
sys.stderr.flush()

df["read_normalized_score"] = df["score"] / df["total_reads"]

### **Step 4: Rank Scores Within Each Sample**
sys.stderr.write("Computing ranked scores per sample...\n")
sys.stderr.flush()

df["genome_rank"] = df.groupby("sampleID")["read_normalized_score"].rank(method="first", ascending=False)

### **Step 5: Determine Significant Genomes Using Adaptive Cutoff**
def adaptive_threshold(scores):
    """Use a percentile-based adaptive cutoff for significance."""
    if len(scores) == 0:
        return np.nan  # Handle empty case
    return np.percentile(scores, 90)  # Top 10% as significant

sys.stderr.write("Determining significant genomes...\n")
sys.stderr.flush()

df["sig_threshold"] = df.groupby("sampleID")["read_normalized_score"].transform(adaptive_threshold)
df["is_significant"] = df["read_normalized_score"] >= df["sig_threshold"]

### **Step 6: Identify Top N Genomes Based on Rank Position**
sys.stderr.write(f"Selecting genomes based on top-{args.num_genomes} rankings per sample...\n")
sys.stderr.flush()

# Keep only the genomes that are ranked within the top-N in each sample
top_genomes_per_sample = df[df["genome_rank"] <= args.num_genomes]

# Count how many times each genome appears in the top-N rankings across samples
top_genome_counts = top_genomes_per_sample.groupby("genome_id")["sampleID"].nunique()

# Select the genomes that appear most frequently in top-N rankings
top_genomes = top_genome_counts.sort_values(ascending=False).head(args.num_genomes).index.tolist()

# Print to STDERR how many disease and control samples contain each genome in top-N
sys.stderr.write("\nTop-N Genomes Presence in Disease and Control Samples:\n")
sys.stderr.write("Genome_ID\tDisease_Count\tControl_Count\n")

for genome in top_genomes:
    disease_count = df[(df["genome_id"] == genome) & (df["label"] == 1) & (df["genome_rank"] <= args.num_genomes)]["sampleID"].nunique()
    control_count = df[(df["genome_id"] == genome) & (df["label"] == 0) & (df["genome_rank"] <= args.num_genomes)]["sampleID"].nunique()
    
    sys.stderr.write(f"{genome}\t{disease_count}\t{control_count}\n")

sys.stderr.flush()

# Create presence/absence features for each genome in the top-N
for genome in top_genomes:
    df[f"genome_{genome}"] = (df["genome_id"] == genome).astype(int)

# Aggregate these genome-level features per sample
genome_features = df.groupby("sampleID")[[f"genome_{g}" for g in top_genomes]].sum().reset_index()

### **Step 7: Compute Summary Statistics**
summary_stats = {
    "Total Samples": len(df["sampleID"].unique()),
    "Total Genomes": len(df["genome_id"].unique()),
    "Mean Normalized Score": df["read_normalized_score"].mean(),
    "Median Normalized Score": df["read_normalized_score"].median(),
    "Std Dev Normalized Score": df["read_normalized_score"].std(),
    "Mean Log Total Reads": df["log_total_reads"].mean(),
    "Median Log Total Reads": df["log_total_reads"].median(),
}

# Compute geometric mean of **normalized scores** separately for disease and control groups
disease_scores = df[df["label"] == 1]["read_normalized_score"].values
control_scores = df[df["label"] == 0]["read_normalized_score"].values

if len(disease_scores) > 0:
    summary_stats["Geometric Mean Normalized Score (Disease)"] = gmean(disease_scores)
else:
    summary_stats["Geometric Mean Normalized Score (Disease)"] = np.nan

if len(control_scores) > 0:
    summary_stats["Geometric Mean Normalized Score (Control)"] = gmean(control_scores)
else:
    summary_stats["Geometric Mean Normalized Score (Control)"] = np.nan

# Output summary statistics as TSV
sys.stdout.write("Metric\tValue\n")
for key, value in summary_stats.items():
    sys.stdout.write(f"{key}\t{value}\n")
sys.stdout.write("//\n")  # End of summary statistics block

### **Step 8: Extract Features for Classifier**
sys.stderr.write("Extracting features for classification...\n")
sys.stderr.flush()

features = []
significant_genomes = []  # List for storing significant genome records
sample_groups = df.groupby("sampleID")

for sample, group in sample_groups:
    scores = group["read_normalized_score"].values

    # Extract only significant genomes
    significant = group[group["is_significant"]]
    num_significant = len(significant)
    significant_genome_ids = significant["genome_id"].tolist()  # Extract genome IDs

    # Compute feature values
    mean_normalized = gmean(scores) if len(scores) > 0 else 0
    score_entropy = -np.sum((scores / np.sum(scores)) * np.log2(scores / np.sum(scores)))

    # Store extracted features
    features.append([
        sample, num_significant, mean_normalized, score_entropy,
        group["log_total_reads"].values[0]
    ])

    # Store significant genome records
    for genome_id in significant_genome_ids:
        significant_genomes.append([sample, genome_id])

# Convert features into a DataFrame
feature_df = pd.DataFrame(features, columns=[
    "sampleID", "num_significant", "mean_normalized", "score_entropy", "log_total_reads"
])

# Merge with genome presence features and sample labels
feature_df = feature_df.merge(genome_features, on="sampleID", how="left").fillna(0)
sample_labels = df[["sampleID", "label"]].drop_duplicates()
feature_df = feature_df.merge(sample_labels, on="sampleID")

# Output extracted features as TSV
feature_df.to_csv(sys.stdout, sep="\t", index=False)
sys.stdout.write("//\n")  # End of feature block
