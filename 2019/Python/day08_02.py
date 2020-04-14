import textwrap

from file_utils import read_data_to_string


def separate_into_layers(full_image, width, height):
    image_size = height * width
    layer_count = len(full_image) // image_size
    result = [full_image[i:i + image_size] for i in range(0, len(full_image), image_size)]

    return result, layer_count


# Task - https://adventofcode.com/2019/day/8
def main():
    image_width = 25
    image_height = 6
    layers, layer_count = separate_into_layers(read_data_to_string("day08.txt"), image_width, image_height)

    # tests
    # image_width = 2
    # image_height = 2
    # layers, layer_count = separate_into_layers("0222112222120000", image_width, image_height)

    output_image = ""
    for h in range(image_height):
        for w in range(image_width):
            pixel = 2
            for l in range(layer_count):
                layer_pixel = layers[l][h * image_width + w]
                if layer_pixel is not "2":
                    pixel = layer_pixel
                    break
            output_image += pixel

    print(textwrap.fill(output_image, image_width))


if __name__ == '__main__':
    main()