
def read_data_to_array(data_file):
    data = open(data_file, 'r')
    result = [int(x) for x in data.readline().split(",")]
    data.close()

    return result
