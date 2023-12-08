class CustomDict(dict):
    def __init__(self, *args, **kwargs):
        super(CustomDict, self).__init__(*args, **kwargs)

    # Add your additional features or overrides here
    def custom_method(self):
        print("This is a custom method.")