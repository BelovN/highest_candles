

def get_highest_lowest_indexes(data, lowest, highest):
    highest_indexes = []
    lowest_indexes = []
    for index, value in enumerate(data['<CLOSE>']):
        if index > 0:
            if value < lowest[index-1]:
                lowest_indexes.append(index)
            elif value > highest[index-1]:
                highest_indexes.append(index)

    return lowest_indexes, highest_indexes


def get_values_in_range(data, n, function):
    values = []
    for i in range(len(data)):
        if i <= n:
            values.append(function(data[:i+1]))
        else:
            values.append(function(data[i-n:i+1]))
    return values


def get_min_max_values(data):
    max_values = get_values_in_range(data['<HIGH>'], N, max)
    min_values = get_values_in_range(data['<LOW>'], N, min)

    return min_values, max_values
