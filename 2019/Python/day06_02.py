class SpaceObject:
    """
    Representation of an object in space with link to the object that
    the current is orbiting and all bodies that orbit the current
    """
    def __init__(self, name, parent = None) -> None:
        self.children = []
        self.name = name
        self.parent = parent

    def place_orbiting_element(self, child):
        self.children.append(child)
        return child

    def get_route(self):
        """
        Returns the path from COM to the position of the object
        :return:
        """
        route = []
        element = self
        while element.parent is not None:
            route.append(element.parent.name)
            element = element.parent

        return route[::-1]


def map_system():
    """
    Read data and put it into map with the full list of orbiting bodies around each space object
    :return:
    """
    list_of_orbits = {}
    data = open("day06.txt", 'r')

    for pair in data:
        center, orbiting_body = pair.rstrip().split(")")

        # for the "parent" body create a list of objects that orbit it
        for_body = list_of_orbits.get(center)
        if for_body:
            for_body.append(orbiting_body)
        else:
            list_of_orbits[center] = [orbiting_body]

    data.close()

    return list_of_orbits


def get_routes_to_elements(list_of_orbits):
    """
    Wide run through all elements connected to the COM and return the route to YOU and SAN elements
    :param list_of_orbits:
    :return:
    """
    current_orbital_set = set()
    current_orbital_set.add(SpaceObject("COM"))
    start_element = None
    dest_element = None
    while True:
        next_orbital_set = set()
        # for each item in current iteration of bodies
        for item in current_orbital_set:
            # add to the list of bodies we will go through on the next iteration
            list_of_subbodies = list_of_orbits.get(item.name)
            if list_of_subbodies and len(list_of_subbodies) > 0:
                for element in list_of_subbodies:
                    # create a tree element with current and one child element
                    new_space_object = SpaceObject(element, item)
                    next_orbital_set.add(item.place_orbiting_element(new_space_object))
                    # check if we found our current position or our destination
                    if element == "YOU":
                        start_element = new_space_object
                    elif element == "SAN":
                        dest_element = new_space_object

            # count number of direct and indirect orbits
            if start_element and dest_element:
                break

        current_orbital_set = next_orbital_set

        # execute until there are no new bodies to go through on next iteration
        if (len(next_orbital_set) == 0) or (start_element and dest_element):
            break

    return start_element.get_route(), dest_element.get_route()


# Task - https://adventofcode.com/2019/day/6#part2
def main():
    list_of_orbits = map_system()

    start_route, dest_route = [set(route) for route in get_routes_to_elements(list_of_orbits)]

    # first way
    print(len(start_route.symmetric_difference(dest_route)))

    # second way
    # index = 0
    # while start_route[index] == dest_route[index]:
    #     index += 1
    # print(len(start_route) + len(dest_route) - (2 * index))

    print(start_route)
    print(dest_route)


if __name__ == '__main__':
    main()
