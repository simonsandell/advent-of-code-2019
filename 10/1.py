


class Asteriod:
    def __init__(self):
        self.grid_top = -1
        self.grid_left = -1
        self.square_top = 0.5
        self.square_left = 0.5

def get_common_divisors(dist_left, dist_top):
    # need to handle negative dist!
    div_left = []
    div_top = []
    for d in range(2, dist_left):
        if dist_left % == 0:
            div_left.append(d)
    for d in range(2, dist_top):
        if dist_top % == 0:
            div_top.append(d)
    intersection = [x for x in dist_top if  x in dist_left]
    return intersection


def LOS_blocked(fr, to, asteroids):
    dist_left = to.grid_left - fr.grid_left
    dist_top = to.grid_top- fr.grid_top
    common_divisors = get_common_divisors(dist_left, dist_top)
    if len(common_divisors) == 0:
        return False
    for div in common_divisors:
        
    

    

def asteroid_sees_n_asteroids(asteroids):
    res = {}
    for asteroid in asteroids:


    asteroids.
    for to


