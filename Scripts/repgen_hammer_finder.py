import time
#This is a program that loads a sample, and a set of hammers, and tries to match the repgen pegs to that sample.
START = time.time()
CONTIG_COUNT = 0
#TODO load the sample with contigs into memory. Stop loading after 1000 contigs
def sample_reads_kmer_maker(Contig_Count, start):
    bin_report_file = "BinReport_Healthy.tsv"
    with open(bin_report_file) as sample_file:
        return
        #initialize a list of the kmers in the current contigs
        #initialize the contig that the kmers will be made from.
            #get rid of the formatting on the line.
            #This checks for the start of a new contig.
                #This only happens if it is not the first contig.
                #Create the 20mers to compare with the hammers.
                #Grab the number at the end of the contig name. This will tell us where to continue when we stop.
                #Reinitialize the total_contig so that you're only splitting one contig at a time.

#TODO input the 2 column table of the hammers: hammer then pegid
def hammer_data_load(start):
    counter = 0
    hammers_dict = {}
    hammer_data = open("hammer_set.tsv")
    for position, line in enumerate(hammer_data):
        counter += 1
        if counter % 10 == 0:
            line = line.strip("\n")
            row = line.split("\t")
            hammer = row[0]
            peg = row[1]
            hammers_dict[hammer] = peg
            checkpoint = time.time() - start
        if counter % 10000 == 0:
            print(f"This has taken {checkpoint} seconds and has counted {counter} hammers.")
    hammer_data.close()
    return hammers_dict


useful_hammers = hammer_data_load(START)
print(useful_hammers)
#TODO have a counter that counts the number of times each repgen genome is found in the contig.

#TODO print the repgens that have 3 or more hits.