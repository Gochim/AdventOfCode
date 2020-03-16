import math
from shapely.geometry import LineString

class MaxValues:
    def __init__(self) -> None:
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

    def __str__(self) -> str:
        return "{}, {}, {}, {}".format(self.left, self.right, self.bottom, self.top)


COMMAND_UP = "U"
COMMAND_DOWN = "D"
COMMAND_LEFT = "L"
COMMAND_RIGHT = "R"

the_map = []


def analyze_route(path):
    route = [(0, 0) for _ in range(len(path) + 1)]

    position = [0, 0]
    for index, item in enumerate(path):
        operation = item[:1]
        count = int(item[1:])

        if operation is COMMAND_DOWN:
            route[index + 1] = (route[index][0], route[index][1] - count)
            op_result = position[1] - count
            position[1] = op_result

        elif operation is COMMAND_UP:
            route[index + 1] = (route[index][0], route[index][1] + count)
            op_result = position[1] + count
            position[1] = op_result

        elif operation is COMMAND_RIGHT:
            route[index + 1] = (route[index][0] + count, route[index][1])
            op_result = position[0] + count
            position[0] = op_result

        elif operation is COMMAND_LEFT:
            route[index + 1] = (route[index][0] - count, route[index][1])
            op_result = position[0] - count
            position[0] = op_result

    return route


def get_intersections(f_item, f_prev_item, s_item, s_prev_item):
    line1 = LineString([f_prev_item, f_item])
    line2 = LineString([s_prev_item, s_item])

    result = line1.intersection(line2)
    if result.is_empty:
        result = None
    elif result.geom_type is not "Point":
        raise ValueError("NOt point")
    elif result.geom_type is "Point" and result.x == 0 and result.y == 0:
        result = None

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

    min_distance = None
    for s_index, s_item in enumerate(second_route):
        for f_index, f_item in enumerate(first_route):
            if s_index == 0 or f_index == 0:
                continue

            # check if they have intersection and get their position
            intersection = get_intersections(f_item, first_route[f_index - 1], s_item, second_route[s_index - 1])
            if intersection is not None:
                distance = abs(intersection.x) + abs(intersection.y)
                if min_distance is None or (distance < min_distance):
                    min_distance = distance

    print(first_route)
    print(second_route)

    print(min_distance)

    return


if __name__ == '__main__':
    main()
