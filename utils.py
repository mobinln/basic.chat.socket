def findIndex(array, fn):
    for index, item in enumerate(array):
        if fn(item, index):
            return index
