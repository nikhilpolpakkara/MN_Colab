class CustomList(list):
    def __init__(self, *args):
        super(CustomList, self).__init__(*args)

    def list_to_dict(self, key):
        """
        :param key: key inside the dictionary which will be used as key in new dictionary for storing the dictionary
        which was earlier present in list.
        :return: dictionary
        """
        print(self)
        d = {}
        for item in self:
            print("sdgfjashd")
            print(item)
            d[item[key]] = item
        return d

