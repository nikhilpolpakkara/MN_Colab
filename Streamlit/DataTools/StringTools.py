import re
import os


def remove_unnecessary_characters(input_string):
    if isinstance(input_string, str):
        pattern = re.compile(r'[\n\r\t]')
        cleaned_string = re.sub(pattern, '', input_string)
        return cleaned_string
    else:
        print(input_string)
        return input_string


def get_file_name_without_extension(file_path):
    file_name = os.path.basename(file_path)  # Get the base name from the path
    name_without_extension = os.path.splitext(file_name)[0]  # Get the file name without extension
    return name_without_extension