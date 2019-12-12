
DIM = 3

class Moon:


    def __init__(self, x, v):
        self.x = x
        self.v = v

    def update_velocity(self, other):
        for i in range(DIM):
            if self.x[i] < other.x[i]:
                self.v[i] += 1
            if self.x[i] > other.x[i]:
                self.v[i] -= 1

    def step(self):
        for i in range(DIM):
            self.x[i] += self.v[i]

    def get_potential(self):
        p = 0
        for i in range(DIM):
            p += abs(self.x[i])
        return p
    def get_kinetic(self):
        k = 0
        for i in range(DIM):
            k += abs(self.v[i])
        return k
    def get_total_energy(self):
        return self.get_potential()*self.get_kinetic()
    def __str__(self):
        x = str(self.x)
        v = str(self.v)
        return 'x: ' + x + '\n' + 'v: ' + v + '\n'
    def __repr__(self):
        return str(self)

def run_simulation(moons, steps):
    for _ in range(steps):
        for moon in moons:
            for othermoon in moons:
                if not othermoon == moon:
                    moon.update_velocity(othermoon)
        for moon in moons:
            moon.step()
    return moons

if __name__ == '__main__':
    """
    Input
    """
    # Io = Moon(      [ 17,  5,  1], [0,0,0])
    # Europa = Moon(  [ -2, -8,  8], [0,0,0])
    # Ganymede = Moon([  7, -6, 14], [0,0,0])
    # Callisto = Moon([  1,-10,  4], [0,0,0])
    Io = Moon(      [ -8,-10,  0], [0,0,0])
    Europa = Moon(  [  5,  5, 10], [0,0,0])
    Ganymede = Moon([  2, -7,  3], [0,0,0])
    Callisto = Moon([  9, -8, -3], [0,0,0])
    moons = [Io, Europa, Ganymede, Callisto]
    moons = run_simulation(moons, 100)
    print(moons)
    print(sum([moon.get_total_energy() for moon in moons]))

