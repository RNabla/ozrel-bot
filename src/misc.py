def map_entity(lines, constructor):
    dictionary = {}
    for line in lines:
        instance = constructor(line)
        dictionary[instance.id] = instance
    return dictionary


def flat_map(lines, constructor):
    collection = []
    for line in lines:
        collection.append(constructor(line))
    return collection


def two_digit_number(num):
    if num < 9:
        return '0{0}'.format(num)
    return '{0}'.format(num)
