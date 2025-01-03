import csv
from itertools import islice

def filter_rows(input_file, output_file, step=175):
    # Open the output file in write mode to clear its contents before writing
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Using islice to select every 'step' row
        for index, row in enumerate(islice(reader, 0, None, step)):
            writer.writerow(row)
        
    print(f"Every {step}th row has been written to {output_file}")

# Change the step as needed
filter_rows('ratings.csv', 'filtered_ratings.csv')
