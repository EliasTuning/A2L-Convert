import json
import os


def parse_json_and_generate_defines(json_file_path):
    # Load the JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Initialize a list to store the output lines
    output_lines = ["#include <stdint.h>"]  # Add the include statement at the beginning

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
                raise ValueError(f"Unsupported size: {size}")

            # Extract the name, address, bit mask, and description
            name = entity.get('name')
            name = name.replace('.', "_")
            address = entity.get('addr')
            bit_mask = entity.get('bit_mask')
            description = entity.get('description', '')

            # Add the description as a comment
            if description:
                output_lines.append(f"// {description}")

            # Create the define statement
            if bit_mask:
                define_statement = f"#define {name} ((*((volatile {c_type} *) {address})) & {bit_mask})"
            else:
                define_statement = f"#define {name} (*((volatile {c_type} *) {address}))"

            output_lines.append(define_statement)

    # Join the output lines into a single string
    output_text = "\n".join(output_lines)

    # Determine the output file path with .h extension
    base_name = os.path.splitext(json_file_path)[0]
    header_file_path = f"{base_name}.h"

    # Write the output text to the header file with UTF-8 encoding
    with open(header_file_path, 'w', encoding='utf-8') as header_file:
        header_file.write(output_text)

    return output_text


# Example usage
json_file_path = '8E0907115D_0070.json'
output_text = parse_json_and_generate_defines(json_file_path)
print(output_text)
