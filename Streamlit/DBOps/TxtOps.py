def extract_content_from_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def find_lines_between_keywords(lines, start_keyword, end_keyword):
    result = []
    inside_block = False

    for line in lines:
        if line.startswith(start_keyword):
            inside_block = True
            try:
                result.append(line.split()[1])
            except:
                pass
        elif inside_block:
            try:
                result.append(line.split()[1])
            except:
                pass
            if line.startswith(end_keyword):
                inside_block = False
                break  # Stop capturing lines when the end keyword is found

    return result

def read_lines_after_keyword(file_lines, keyword):
    # Find the index of the first line starting with "END"
    end_index = next((index for index, line in enumerate(file_lines) if line.startswith(keyword)), None)

    if end_index is not None:
        # Remove lines before the first "END" line
        file_lines = file_lines[end_index+1:]
        return file_lines

def split_lines_by_end(lines, keyword):
    blocks = []
    current_block = []

    for line in lines:
        current_block.append(line.strip())
        if line.startswith(keyword):
            blocks.append(current_block)
            current_block = []

    return blocks