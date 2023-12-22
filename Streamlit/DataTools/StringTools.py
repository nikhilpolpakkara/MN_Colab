import re


def remove_unnecessary_characters(input_string):
    pattern = re.compile(r'[\n\r\t]')
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string


