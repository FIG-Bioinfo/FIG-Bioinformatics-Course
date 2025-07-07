import sys
import pandas as pd
import numpy as np
from collections import Counter

def read_data():
    """Reads TSV data from STDIN and returns a DataFrame."""
    df = pd.read_csv(sys.stdin, sep='\t')
    return df

def compute_good_turing(df):
    """
    Applies the Good-Turing estimator to adjust frequency estimates.
    """
    # Step 1: Get the frequency counts
    species_counts = Counter(df['score'])
    
    # Step 2: Compute frequency of frequencies (Nr)
    freq_of_freqs = Counter(species_counts.values())

    # Step 3: Compute adjusted Good-Turing estimates
    adjusted_counts = {}
    sorted_counts = sorted(species_counts.items())

    for i, (r, nr) in enumerate(sorted_counts):
        if (r + 1) in freq_of_freqs:
            next_r_count = freq_of_freqs[r + 1]
            adjusted_r = (r + 1) * (next_r_count / nr)
        else:
            adjusted_r = r  # If no next count, keep it the same
        adjusted_counts[r] = adjusted_r

    # Step 4: Apply Adjusted Counts
    df['adjusted_score'] = df['score'].apply(lambda x: adjusted_counts.get(x, x))
    
    return df, freq_of_freqs

def estimate_unseen_species(freq_of_freqs):
    """
    Computes the estimated number of unseen species (N0) using Good-Turing.
    """
    N1 = freq_of_freqs.get(1, 0)  # Count of species that appear exactly once
    total_species = sum(freq_of_freqs.values())  # Sum of all observed species
    
    if total_species == N1:  # Avoid division by zero
        N0 = 0
    else:
        N0 = N1 * (total_species / (total_species - N1))

    return int(round(N0))  # Round to nearest integer

def main():
    df = read_data()
    df, freq_of_freqs = compute_good_turing(df)
    
    # Estimate the number of unseen species
    unseen_species_estimate = estimate_unseen_species(freq_of_freqs)
    
    # Print the estimate to STDERR
    print(f"Estimated number of unseen species: {unseen_species_estimate}", file=sys.stderr)

    # Print adjusted data to STDOUT
    df.to_csv(sys.stdout, sep='\t', index=False)

if __name__ == "__main__":
    main()
