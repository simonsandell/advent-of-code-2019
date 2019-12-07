

class Planet:
    def __init__(self, name):
        self.name = name
        self.orbits = None
        self.orbitees = []


    def get_orbit_number(self):
        if self.name == 'COM':
            return 0
        return 1 + self.orbits.get_orbit_number()

    def is_leaf(self):
        return len(self.orbitees) == 0

    def get_path_to_COM(self):
        if self.name == 'COM':
            return 'COM'
        return self.name + ',' + self.orbits.get_path_to_COM()

def compute_checksum(planets):
    s = 0
    for _, planet  in planets.items():
        s += planet.get_orbit_number()
    return s

def find_steps_between(path_1, path_2):
    first_steps = 0
    for i, planet in enumerate(path_1):
        if planet in path_2:
            first_steps = i
            break
    second_steps = 0
    for i, planet in enumerate(path_2):
        if planet in path_1:
            second_steps = i
            break
    return first_steps + second_steps 

if __name__ == '__main__':
    planets = {}
    with open("input", "r") as f:
        for l in f:
            inner, outer = [x.strip() for x in l.split(")")]
            if not outer in planets:
                planets[outer] = Planet(outer)
            if not inner in planets:
                planets[inner] = Planet(inner)
            planets[inner].orbitees.append(planets[outer])
            planets[outer].orbits = planets[inner]

    p1 = planets['YOU'].get_path_to_COM().split(',')
    p2 = planets['SAN'].get_path_to_COM().split(',')
    steps = find_steps_between(p1, p2)
    print(steps - 2)







