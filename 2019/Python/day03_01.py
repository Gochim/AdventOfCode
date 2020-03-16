from shapely.geometry import LineString

COMMAND_UP = "U"
COMMAND_DOWN = "D"
COMMAND_LEFT = "L"
COMMAND_RIGHT = "R"


def analyze_route(path):
    """
    Parses a list of commands and create a list of coordinates of wires for a specified path
    :param path: list of commands to execuse
    :return:
    """
    route = [(0, 0) for _ in range(len(path) + 1)]

    for index, item in enumerate(path):
        # parse operation
        operation = item[:1]
        count = int(item[1:])

        # map the new coordinates
        if operation is COMMAND_DOWN:
            route[index + 1] = (route[index][0], route[index][1] - count)
        elif operation is COMMAND_UP:
            route[index + 1] = (route[index][0], route[index][1] + count)
        elif operation is COMMAND_RIGHT:
            route[index + 1] = (route[index][0] + count, route[index][1])
        elif operation is COMMAND_LEFT:
            route[index + 1] = (route[index][0] - count, route[index][1])

    return route


def get_intersections(f_item, f_prev_item, s_item, s_prev_item):
    """
    Check if two lines intersect
    :param f_item: ending point of the first line
    :param f_prev_item: starting point of the first line
    :param s_item: ending point of the second line
    :param s_prev_item: starting point of the second line
    :return:
    """
    line1 = LineString([f_prev_item, f_item])
    line2 = LineString([s_prev_item, s_item])
    result = line1.intersection(line2)

    if result.is_empty:
        result = None
    elif result.geom_type is "Point" and result.x == 0 and result.y == 0:
        result = None
    elif result.geom_type is not "Point":  # for debug purposes
        raise ValueError("Not a point")

    return result


def main():
    data = open("day03_01.txt", 'r')
    first_path = data.readline().split(",")
    second_path = data.readline().split(",")
    data.close()

    print(first_path)
    print(second_path)

    first_route = analyze_route(first_path)
    second_route = analyze_route(second_path)

    print(first_route)
    print(second_route)

    min_distance = None
    f_len, s_len = len(first_route), len(second_route)
    for s_index in range(1, s_len):
        for f_index in range(1, f_len):
            # check if they have intersection and get their position
            intersection = get_intersections(
                first_route[f_index], first_route[f_index - 1],
                second_route[s_index], second_route[s_index - 1]
            )

            if intersection is not None:
                distance = abs(intersection.x) + abs(intersection.y)
                if min_distance is None or (distance < min_distance):
                    min_distance = distance

    print(min_distance)


if __name__ == '__main__':
    main()
