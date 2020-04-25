
def read_data_to_array(data_file):
    data = open(data_file, 'r')
    result = [int(x) for x in data.readline().split(",")]
    data.close()

    return result


def read_data_to_string(data_file):
    data = open(data_file, 'r')
    result = data.readline()
    data.close()
    return result


def read_map(data_file):
    data = open(data_file, 'r')
    result = [list(row.strip()) for row in data]
    data.close()
    return result
