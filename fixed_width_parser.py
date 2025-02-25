import csv
import random
import string
import json


def generate_fixed_width_file(spec, output_file, num_rows=100):
    """
    Generate a fixed-width file based on the provided specification.
    
    Args:
        spec (dict): The specification dictionary with column names and offsets.
        output_file (str): The output file path.
        num_rows (int): Number of data rows to generate.
    """
    column_names = spec["ColumnNames"]
    offsets = [int(offset) for offset in spec["Offsets"]]
    encoding = spec["FixedWidthEncoding"]
    include_header = spec["IncludeHeader"].lower() == "true"
    
    with open(output_file, 'w', encoding=encoding) as f:
        # Write header if required
        if include_header:
            header_line = ""
            for i, col in enumerate(column_names):
                # Ensure column name fits within the offset
                header_value = col[:offsets[i]].ljust(offsets[i])
                header_line += header_value
            f.write(header_line + "\n")
        
        # Generate random data rows
        for _ in range(num_rows):
            data_line = ""
            for offset in offsets:
                # Generate random data for each column
                data_length = random.randint(1, offset)
                random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=data_length))
                data_line += random_data.ljust(offset)
            f.write(data_line + "\n")


def parse_fixed_width_file(spec, input_file, output_file):
    """
    Parse a fixed-width file and convert it to a delimited (CSV) file.
    
    Args:
        spec (dict): The specification dictionary with column names and offsets.
        input_file (str): The input fixed-width file path.
        output_file (str): The output CSV file path.
    """
    column_names = spec["ColumnNames"]
    offsets = [int(offset) for offset in spec["Offsets"]]
    input_encoding = spec["FixedWidthEncoding"]
    output_encoding = spec["DelimitedEncoding"]
    include_header = spec["IncludeHeader"].lower() == "true"
    
    # Calculate start and end positions for each column
    positions = []
    start_pos = 0
    for offset in offsets:
        positions.append((start_pos, start_pos + offset))
        start_pos += offset
    
    with open(input_file, 'r', encoding=input_encoding) as infile:
        with open(output_file, 'w', newline='', encoding=output_encoding) as outfile:
            writer = csv.writer(outfile)
            
            # Write header
            writer.writerow(column_names)
            
            # Skip header in input file if it exists
            if include_header:
                next(infile)
            
            # Process data rows
            for line in infile:
                row_data = []
                
                for start, end in positions:
                    if start < len(line):
                        # Extract field value and strip whitespace
                        end = min(end, len(line))  # Handle lines shorter than expected
                        field_value = line[start:end].strip()
                        row_data.append(field_value)
                    else:
                        row_data.append("")  # Handle missing columns
                
                writer.writerow(row_data)


if __name__ == "__main__":
    # Example usage
    with open('spec.json', 'r') as f:
        spec = json.load(f)
    
    fixed_width_file = 'generated_data.txt'
    csv_file = 'parsed_data.csv'
    
    # Generate a sample fixed-width file
    generate_fixed_width_file(spec, fixed_width_file)
    print(f"Generated fixed-width file: {fixed_width_file}")
    
    # Parse it to CSV
    parse_fixed_width_file(spec, fixed_width_file, csv_file)
    print(f"Parsed and converted to CSV: {csv_file}")
