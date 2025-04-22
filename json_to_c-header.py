#!/usr/bin/env python3
import json
import os
import argparse
import sys

def convert_json_to_header(input_file, output_file=None):
    """
    Convert JSON data to C header file with memory address definitions.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str, optional): Path to the output header file.
                                   If not provided, will use input filename with '.h' extension
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.h"

        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Initialize a list to store the output lines
        output_lines = [
            "/* Auto-generated header file for ECU memory addresses */",
            "#ifndef ECU_MEMORY_MAP_H",
            "#define ECU_MEMORY_MAP_H",
            "",
            "#include <stdint.h>",
            ""
        ]

        # Iterate through each entity in the JSON
        for key, entity in data.items():
            if entity.get('type') == 'variable':
                # Determine the C-type based on the size
                size = entity.get('size')
                if size == 1:
                    c_type = 'uint8_t'
                elif size == 2:
                    c_type = 'uint16_t'
                elif size == 4:
                    c_type = 'uint32_t'
                elif size == 8:
                    c_type = 'uint64_t'
                else:
                    raise ValueError(f"Unsupported size: {size} for variable {key}")

                # Extract the name, address, bit mask, and description
                name = entity.get('name')
                name = name.replace('.', "_")
                address = entity.get('addr')
                bit_mask = entity.get('bit_mask')
                description = entity.get('description', '')

                # Add the description as a comment
                if description:
                    output_lines.append(f"/* {description} */")

                # Create the define statement
                if bit_mask:
                    define_statement = f"#define {name} ((*((volatile {c_type} *) {address})) & {bit_mask})"
                else:
                    define_statement = f"#define {name} (*((volatile {c_type} *) {address}))"

                output_lines.append(define_statement)
                output_lines.append("")  # Add empty line for readability

        # Add header guard end
        output_lines.extend([
            "#endif /* ECU_MEMORY_MAP_H */",
            ""
        ])

        # Join the output lines into a single string
        output_text = "\n".join(output_lines)

        # Write the output text to the header file
        with open(output_file, 'w', encoding='utf-8') as header_file:
            header_file.write(output_text)

        print(f"Successfully converted {input_file}")
        print(f"Header file saved as: {output_file}")
        return 0

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error converting to header: {str(e)}", file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON ECU data to C header file"
    )
    parser.add_argument(
        "input_file",
        help="Path to the input JSON file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output header file (optional)",
        default=None
    )

    args = parser.parse_args()
    return convert_json_to_header(args.input_file, args.output)

if __name__ == "__main__":
    sys.exit(main())
