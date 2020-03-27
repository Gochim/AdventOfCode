class SpaceObject:

    def __init__(self) -> None:
        self.children = []
        self.orbits = 0

    def place_element(self, parent):
        self.orbits = parent.orbits + 1
        parent.children.append(self)


# Task - https://adventofcode.com/2019/day/6#part2
def main():
    list_of_orbits = {}
    data = open("day06.txt", 'r')

    # read data
    for pair in data:
        center, orbiting_body = pair.rstrip().split(")")

        # for the "parent" body create a list of objects that orbit it
        for_body = list_of_orbits.get(center)
        if for_body:
            for_body.append(orbiting_body)
        else:
            list_of_orbits[center] = [orbiting_body]

    data.close()

    # wide run through all elements connected to the COM
    current_orbital_set = set()
    current_orbital_set.add("COM")
    wave = 0
    orbit_count = 0
    while True:
        next_orbital_set = set()
        # for each item in current iteration of bodies
        for item in current_orbital_set:
            # add to the list of bodies we will go through on the next iteration
            list_of_subbodies = list_of_orbits.get(item)
            if list_of_subbodies and len(list_of_subbodies) > 0:
                for element in list_of_subbodies:
                    next_orbital_set.add(element)

            # count number of direct and indirect orbits
            orbit_count += wave
        current_orbital_set = next_orbital_set
        wave += 1

        # execute until there are no new bodies to go through on next iteration
        if len(next_orbital_set) == 0:
            break

    print(orbit_count)


if __name__ == '__main__':
    main()
