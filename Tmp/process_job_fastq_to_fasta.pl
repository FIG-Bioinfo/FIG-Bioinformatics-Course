#!/usr/bin/env perl

use strict;
use warnings;
use File::Basename;

# Check for command-line argument
if (@ARGV != 1) {
    die "Usage: $0 <directory-name>\n";
}

my $dirname = $ARGV[0];
my $fastq_dir = "WGS/FASTQ/$dirname";  # Corrected source directory path
my $fasta_dir = "WGS/FASTA/$dirname";  # Corrected target directory path

# Ensure the source directory exists
unless (-d $fastq_dir) {
    die "Directory '$fastq_dir' does not exist.\n";
}

# Ensure the target directory exists, create it if not
unless (-d $fasta_dir) {
    mkdir $fasta_dir or die "Failed to create directory '$fasta_dir': $!\n";
}

# Open the directory
opendir(my $dh, $fastq_dir) or die "Cannot open directory '$fastq_dir': $!\n";

# Process files
while (my $file = readdir($dh)) {
    next if $file =~ /^\./;  # Skip hidden files and parent/current dir entries

    # Extract prefix (everything before the first dot)
    if ($file =~ /^([^\.]+)\..+$/) {
        my $prefix = $1;

        # Construct system command
        my $command = "gunzip -c WGS/FASTQ/$dirname/$file | python $ENV{HOME}/bin/convert_fastq_to_fasta.py > WGS/FASTA/$dirname/$prefix.fna";

        # Execute the system command
        print "Executing: $command\n";
        my $exit_code = system($command);

        # Check for execution success
        if ($exit_code != 0) {
            warn "Warning: Command failed with exit code $exit_code\n";
        }
    }
}

# Close the directory
closedir($dh);
