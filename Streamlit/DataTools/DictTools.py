class CustomDict(dict):
    def __init__(self, *args, **kwargs):
        super(CustomDict, self).__init__(*args, **kwargs)

    # Add your additional features or overrides here
    def custom_method(self):
        print("This is a custom method.")


def non_empty_lists_fields(input_dict):
    """
    Returns a list of fields in the input dictionary
    that have non-empty lists as values.

    Args:
    - input_dict (dict): The input dictionary.

    Returns:
    - List of fields with non-empty lists.
    """
    non_empty_fields = []
    for key, value in input_dict.items():
        if isinstance(value, list) and len(value) > 0:
            non_empty_fields.append(key)
    return non_empty_fields
