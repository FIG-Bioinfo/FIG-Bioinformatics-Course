#!/bin/bash

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <SRR_ACCESSION_ID>"
    exit 1
fi

SRR_ID=$1
OUTPUT_DIR="./$SRR_ID"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Step 1: Download the SRA file
echo "Downloading SRA file for $SRR_ID..."
prefetch "$SRR_ID" --output-directory "$OUTPUT_DIR"

# Check if prefetch was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to download SRA entry."
    exit 1
fi

# Step 2: Convert SRA to FASTQ
SRA_FILE="$OUTPUT_DIR/$SRR_ID.sra"
echo "Extracting FASTQ from $SRA_FILE..."
fasterq-dump "$SRA_FILE" --split-files --outdir "$OUTPUT_DIR"

# Check if fasterq-dump was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to extract FASTQ."
    exit 1
fi

# Step 3: Handle Paired-End Reads
FASTQ1="$OUTPUT_DIR/${SRR_ID}_1.fastq"
FASTQ2="$OUTPUT_DIR/${SRR_ID}_2.fastq"

if [ -f "$FASTQ1" ] && [ -f "$FASTQ2" ]; then
    echo "Paired-end FASTQ files found. Left reads: $FASTQ1, Right reads: $FASTQ2"
else
    echo "Single-end FASTQ file found: $OUTPUT_DIR/${SRR_ID}.fastq"
fi

echo "Process completed successfully."
