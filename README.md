# Fixed Width File Parser

A Python solution for parsing fixed width files and converting them to CSV format.

## Overview

This project provides utilities to:
1. Generate fixed-width files with random data based on a specification
2. Parse fixed-width files and convert them to CSV format
3. Handle encodings properly (windows-1252 for fixed-width, utf-8 for CSV)

## Files

- `fixed_width_parser.py`: Core functionality for generating and parsing fixed-width files
- `spec.json`: The specification file defining the fixed-width format
- `Dockerfile`: For running the parser in a container

## Running the Parser

### Using Python directly

```bash
# Generate a fixed-width file and parse it to CSV
python fixed_width_parser.py
```

### Using Docker

```bash
# Build the Docker image
docker build -t fixed-width-parser .

# Run the parser
docker run --rm -v $(pwd):/app fixed-width-parser
```


## Design Considerations

- **No external dependencies**: Uses only Python standard library (no pandas)
- **Encoding awareness**: Handles windows-1252 for input and utf-8 for output
- **Robust parsing**: Handles edge cases like shorter lines
- **Clean code**: Well-documented with descriptive variable names
- **Test coverage**: Comprehensive tests ensure correctness

## How It Works

1. The parser calculates the exact position of each column in the fixed-width file
2. It reads the file line by line, extracting each field based on its position
3. It writes the extracted data to a CSV file using the standard library's csv module
4. The process respects the encodings specified in the spec file

## Specification Format

The parser uses a JSON specification file with the following structure:

```json
{
    "ColumnNames": ["column1", "column2", ...],
    "Offsets": ["5", "10", ...],
    "FixedWidthEncoding": "windows-1252",
    "IncludeHeader": "True",
    "DelimitedEncoding": "utf-8"
}
```

Where:
- `ColumnNames`: Array of column names
- `Offsets`: Array of column widths (as strings)
- `FixedWidthEncoding`: Encoding for the fixed-width file
- `IncludeHeader`: Whether to include a header row in the fixed-width file
- `DelimitedEncoding`: Encoding for the output CSV file
