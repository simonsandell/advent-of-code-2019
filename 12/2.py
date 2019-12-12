import math

DIM = 3

class Moon:

    def __init__(self, x, v):
        self.x = x
        self.v = v

    def update_velocity(self, other, dim):
        if self.x[dim] < other.x[dim]:
            self.v[dim] += 1
        if self.x[dim] > other.x[dim]:
            self.v[dim] -= 1

    def update_velocity_backwards(self, other, dim):
        if self.x[dim] > other.x[dim]:
            self.v[dim] += 1
        if self.x[dim] < other.x[dim]:
            self.v[dim] -= 1

    def step(self, dim):
        self.x[dim] += self.v[dim]

    def step_backwards(self, dim):
        self.x[dim] -= self.v[dim]

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

    def get_state(self, dim):
        return [self.x[dim]]

    def get_full_state(self, dim):
        return self.x[dim], self.v[dim]

    def __str__(self):
        x = str(self.x)
        v = str(self.v)
        return 'x: ' + x + '\n' + 'v: ' + v + '\n'
    def __repr__(self):
        return str(self)

def get_state(moons, dim):
    state = []
    for m in moons:
        state.extend(m.get_state(dim))
    return state

def get_full_state(moons, dim):
    state = []
    for m in moons:
        state.extend(m.get_full_state(dim))
    return state

def run_until_revisit(moons, dim, states):
    steps = 0
    while True:
        moons = run_simulation(moons, dim,  1)
        steps += 1
        newstate = get_state(moons, dim)
        if newstate in states:
            break
        states.append(newstate)
    return moons, steps, states

def run_backwards_until_matching(moons, dim):
    full_state = get_full_state(moons, dim)
    states = [get_state(moons, dim)]
    steps_backward = 0
    while True:
        moons = run_simulation_backwards(moons, dim, 1)
        steps_backward += 1
        newstate = get_state(moons, dim)
        if newstate in states:
            newfullstate = get_full_state(moons, dim)
            if newfullstate == full_state:
                return steps_backward

def run_simulation_backwards(moons, dim, steps):
    for _ in range(steps):
        for moon in moons:
            moon.step_backwards(dim)
        for moon in moons:
            for othermoon in moons:
                if not othermoon is moon:
                    moon.update_velocity_backwards(othermoon, dim)
    return moons

def run_simulation(moons, dim, steps):
    for _ in range(steps):
        for moon in moons:
            for othermoon in moons:
                if not othermoon is moon:
                    moon.update_velocity(othermoon, dim)
        for moon in moons:
            moon.step(dim)
    return moons

if __name__ == '__main__':
    """
    Input
    """
    Io =       ([ 17,  5,  1], [0,0,0])
    Europa =   ([ -2, -8,  8], [0,0,0])
    Ganymede = ([  7, -6, 14], [0,0,0])
    Callisto = ([  1,-10,  4], [0,0,0])
    # Io = (      [ -1,  0,  2], [0,0,0])
    # Europa = (  [  2,-10, -7], [0,0,0])
    # Ganymede = ([  4, -8,  8], [0,0,0])
    # Callisto = ([  3,  5, -1], [0,0,0])
    moons = [Moon(*Io), Moon(*Europa), Moon(*Ganymede), Moon(*Callisto)]
    periods = []
    for dim in range(0, DIM):
        full_states = []
        total_steps = 0
        prev_states = [get_state(moons, dim)]
        while True:
            moons, x0_steps, prev_states = run_until_revisit(moons, dim, prev_states)
            prev_states = []
            newstate = get_full_state(moons, dim)
            total_steps += x0_steps
            if newstate in full_states:
                break
            full_states.append(newstate)
        period = run_backwards_until_matching(moons, dim)
        print(dim, 'period', period, 'tot', total_steps)
        periods.append(period)
    lcm = periods[0]
    for i in periods[1:]:
        lcm = lcm*i//math.gcd(lcm, i)
    print(lcm)
