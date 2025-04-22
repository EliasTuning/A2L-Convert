#!/usr/bin/env python3
import argparse
import sys
import os
import chardet
from pya2l import DB
from pya2l.build import model
from src.preprocess_a2l import preprocess_a2l

def process_a2l_file(input_file, output_file=None):
    """
    Process an A2L file and create a database.
    
    Args:
        input_file (str): Path to input A2L file
        output_file (str, optional): Path to output preprocessed A2L file. 
                                   If not provided, will use input filename with '_preprocessed' suffix
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_preprocessed.a2l"

        # Preprocess the A2L file
        preprocess_a2l(input_file, output_file)
        
        # Create and import to database
        db = DB()
        session = db.import_a2l(output_file, remove_existing=True)
        
        print(f"Successfully processed {input_file}")
        print(f"Preprocessed file saved as: {output_file}")
        return 0

    except Exception as e:
        print(f"Error processing A2L file: {str(e)}", file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(
        description="Convert and preprocess A2L files for ECU tuning"
    )
    parser.add_argument(
        "input_file",
        help="Path to the input A2L file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output preprocessed A2L file (optional)",
        default=None
    )

    args = parser.parse_args()
    return process_a2l_file(args.input_file, args.output)

if __name__ == "__main__":
    sys.exit(main())
