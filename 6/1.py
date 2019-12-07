

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

def compute_checksum(planets):
    s = 0
    for _,planet  in planets.items():
        s += planet.get_orbit_number()
    return s

    


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
    
    checksum = compute_checksum(planets)
    print(checksum)
    







