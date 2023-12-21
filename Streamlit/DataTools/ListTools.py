import pandas as pd


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


def list_to_csv(my_list, filename):
    df = pd.DataFrame(my_list, columns=['Column_Name'])
    df.to_excel(f'../data/{filename}.xlsx', index=False)

