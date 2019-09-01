

def circular_range(collection, start, end, step=1):
    if start < 0:
        return collection[start::step] + collection[:end:step]
    else:
        return collection[start:end:step]

