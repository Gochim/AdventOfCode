from file_utils import read_data_to_string


def separate_into_layers(full_image, width, height):
    image_size = height * width
    layer_count = len(full_image) // image_size
    result = [full_image[i:i + image_size] for i in range(0, len(full_image), image_size)]

    return result, layer_count


# Task - https://adventofcode.com/2019/day/8
def main():
    layers, layer_count = separate_into_layers(read_data_to_string("day08.txt"), 25, 6)

    zero_counts = [layers[i].count("0") for i in layers]
    min_zeroes_index = zero_counts.index(min(zero_counts))

    print(layers[min_zeroes_index].count("1") * layers[min_zeroes_index].count("2"))


if __name__ == '__main__':
    main()