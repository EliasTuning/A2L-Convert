#!/usr/bin/env python3
import argparse
import sys
import os
from pya2l import DB, model

from src.datatypes import get_datatype_size
from src.get_maps import get_maps
from src.get_vars import get_vars
from src.json import write_json_file

def export_to_json(input_file, output_file=None):
    """
    Export A2L data to JSON format.
    
    Args:
        input_file (str): Path to the preprocessed A2L file
        output_file (str, optional): Path to the output JSON file.
                                   If not provided, will use input filename with '.json' extension
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.json"

        # Open database and extract data
        db = DB()
        session = db.open_existing(input_file)

        # Get static and dynamic values
        static_values = get_maps(session)
        dynamic_values = get_vars(session)
        all_values = {**static_values, **dynamic_values}

        # Write to JSON file
        write_json_file(output_file, all_values)
        
        print(f"Successfully exported data from {input_file}")
        print(f"JSON file saved as: {output_file}")
        return 0

    except Exception as e:
        print(f"Error exporting to JSON: {str(e)}", file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(
        description="Export A2L data to JSON format"
    )
    parser.add_argument(
        "input_file",
        help="Path to the preprocessed A2L file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output JSON file (optional)",
        default=None
    )

    args = parser.parse_args()
    return export_to_json(args.input_file, args.output)

if __name__ == "__main__":
    sys.exit(main())
