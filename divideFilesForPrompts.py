import os

def read_file_content(file_path):
    """Reads the content of a single file and returns it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()  # Return lines instead of a single string
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def generate_combined_content(files_list):
    """Combines file contents in the specified pattern."""
    combined_content = []
    for file_path in files_list:
        file_name = os.path.basename(file_path)  # Extract the file name
        file_lines = read_file_content(file_path)
        combined_content.append(f"{file_name}\n'''\n")
        combined_content.extend(file_lines)
        combined_content.append("'''\n\n")  # End the file section with the '''
    return combined_content

def split_text_into_parts(lines, max_chars):
    """Splits lines into parts, ensuring no line exceeds max_chars."""
    parts = []
    current_part = ""
    current_part_length = 0

    for line in lines:
        line_length = len(line)

        # If adding the line exceeds the max_chars limit, finalize the current part and start a new one
        if current_part_length + line_length > max_chars:
            # Make sure current part ends with triple quotes '''
            if not current_part.endswith("'''\n"):
                current_part += "'''\n"
            parts.append(current_part)

            # Start a new part with the current line
            current_part = line
            current_part_length = line_length
        else:
            # Otherwise, add the line to the current part
            current_part += line
            current_part_length += line_length

    # Append any remaining content as the last part
    if current_part:
        # Ensure the last part also ends with '''
        if not current_part.endswith("'''\n"):
            current_part += "'''\n"
        parts.append(current_part)

    return parts

def save_text_parts(text_parts, output_folder):
    """Saves the split parts into separate files in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_parts = len(text_parts)
    for idx, part in enumerate(text_parts):
        part_filename = os.path.join(output_folder, f"combined_code_part_{idx + 1}.txt")
        with open(part_filename, 'w', encoding='utf-8') as f:
            # Add the header 'Part x of y'
            f.write(f"Part {idx + 1} of {total_parts}\n\n")
            f.write(part)
        print(f"Saved {part_filename}")

def main():
    # Read the list of files
    list_file = "List of files to prompt.txt"
    try:
        with open(list_file, 'r', encoding='utf-8') as file:
            files_list = [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error reading {list_file}: {e}")
        return

    # Combine the content from the files
    combined_content = generate_combined_content(files_list)

    # Set the maximum number of characters for each part
    max_chars = 19800

    # Split the combined content into parts
    text_parts = split_text_into_parts(combined_content, max_chars)

    # Define the output folder
    output_folder = "Output files"

    # Save the parts to separate files in the output folder
    save_text_parts(text_parts, output_folder)

if __name__ == "__main__":
    main()
