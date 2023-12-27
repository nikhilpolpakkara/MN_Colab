import re


def remove_unnecessary_characters(input_string):
    if isinstance(input_string, str):
        pattern = re.compile(r'[\n\r\t]')
        cleaned_string = re.sub(pattern, '', input_string)
        return cleaned_string
    else:
        print(input_string)
        return input_string


