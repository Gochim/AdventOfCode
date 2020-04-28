import time

from shapely.geometry import LineString, Point

from file_utils import read_map


# Task - https://adventofcode.com/2019/day/10
def main():
    map = read_map("day10.txt")

    items = []
    points = []
    for line_id, line in enumerate(map):
        for item_id, item in enumerate(line):
            if item is "#":
                items.append((item_id, line_id))
                points.append(Point(item_id, line_id))

    best_el = None
    best_val = 0
    print("Number of asteroids: {}".format(len(items)))

    the_lazor_pos = (22, 19)

    t0 = time.time()
    for location in items:
        # check how many asteroids are visible
        cur_val = 0
        for asteroid in items:
            if asteroid is not location:
                line = LineString([location, asteroid])
                has_blocker = False
                for obs_id, obstacle in enumerate(items):
                    if (obstacle is not location) and (obstacle is not asteroid):
                        if line.contains(points[obs_id]):
                            has_blocker = True
                            break

                if has_blocker is False:
                    cur_val += 1

        if cur_val > best_val:
            best_val = cur_val
            best_el = location

    t1 = time.time()

    print("Time: {}", t1 - t0)
    print("Element {} sees {}".format(best_el, best_val))

if __name__ == '__main__':
    main()