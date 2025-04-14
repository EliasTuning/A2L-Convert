import re
import chardet as chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding


def preprocess_a2l(input, output):
    encoding = detect_encoding(input)
    print(f"The detected encoding is: {encoding}")

    # Open the file for reading
    with open(input, 'r', encoding=encoding) as file:
        updated_content = file.read()

    # Replace occurrences of "//=" with "="
    updated_content = updated_content.replace("//=", "=")
    # Replace occurrences of "//" with "/"
    updated_content = updated_content.replace("//", "/")
    # Replace \" with nothing
    updated_content = updated_content.replace("\\\"", "")


    # Replace Doublequotes
    updated_content = re.sub(r'""(.+?)""', r'\1', updated_content)

    # Remove comments like : / *orig_adr: * /
    # updated_content = re.sub(r'/\*.*?\*/', '', updated_content, flags=re.DOTALL)

    # Remove remaining double quotes:
    lines = updated_content.split('\n')
    processed_lines = []
    for line in lines:
        # Check if line starts and ends with a quotation mark, removing the inside ones
        line_strip = line.strip()
        if line_strip.startswith('"') and line_strip.endswith('"') and len(line_strip) != 2:
            line = line.replace('""', "")
        # Remove all others:
        if line.startswith('/*') and line.endswith('*/'):
            pass
        else:
            line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)
        processed_lines.append(line)

    updated_content = '\n'.join(processed_lines)

    # Function "-" remove:
    pattern = r"(/begin FUNCTION[\s\S]*?\")"
    process_match = lambda match: match.group().replace("-", "_")
    updated_content = re.sub(pattern, lambda m: process_match(m), updated_content)

    # updated_content = re.sub(r'//.*?$', '', updated_content, flags=re.MULTILINE)

    # Open the file for writing (this will overwrite the existing content)
    with open(output, 'w', encoding='utf-8') as file:
        file.write(updated_content)
