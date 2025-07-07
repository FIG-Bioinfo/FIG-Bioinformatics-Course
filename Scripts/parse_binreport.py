from bs4 import BeautifulSoup
import os
import math
import argparse

# This is a beautiful soup program that parses a standard binning report downloaded as an html file


# Main function to parse binning reports
def parse_reports(input_path):
     # Read the HTML file
    with open(input_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tables in the document
    tables = soup.find_all('table', class_='p3basic')

    # Initialize a list to store the extracted data
    extracted_data = []

    # Iterate over each table
    for table in tables:
        # Find all rows in the table
        rows = table.find_all('tr')

        # Iterate over each row (skip the header row)
        for row in rows[1:]:
            # Find all columns in the row
            cols = row.find_all('td')

            # Extract the second, third, and fourth columns
            if len(cols) >= 4:
                second_col = cols[1].get_text(strip=True)
                third_col = cols[2].get_text(strip=True)
                fourth_col = cols[3].get_text(strip=True)

                # Append the extracted data to the list
                extracted_data.append((second_col, third_col, fourth_col))

    return extracted_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse binning reports and representative genomes.")
    parser.add_argument('input_path', type=str, help='Path to the directory containing bin reports. Each report should be an HTML file.')

    args = parser.parse_args()

    # Get the extracted data
    data = parse_reports(args.input_path)
    
    # Get output filename by replacing extension with .tsv
    output_file = os.path.splitext(args.input_path)[0] + '.tsv'
    
    # Write the data to TSV file
    with open(output_file, 'w') as f:
        # Write header
        f.write("Genome ID\tGenome Name\tReference Genome ID\n")
        
        # Write each row of data
        for genome_id, genome_name, ref_id in data:
            f.write(f"{genome_id}\t{genome_name}\t{ref_id}\n")
