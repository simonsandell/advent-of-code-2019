import math
class Asteroid():
    def __init__(self):
        self.grid_top = -1
        self.grid_left = -1
        self.square_top = 0.5
        self.square_left = 0.5
    def __str__(self):
        return '(' + str(self.grid_top) + "," + str(self.grid_left) + ")"
    def __repr__(self):
        return self.__str__()

def get_angle(x, y):
    return math.atan2(x, y)

def flequals(a,b):
    if abs(a-b) < 10e-5:
        return True
    return False

def sign(n):
    "Return 1 if positive, 0 if 0, -1 if negative"
    return (n>0) - (n<0)

def same_signs(one_x, one_y, two_x, two_y):
    return sign(one_x) == sign(two_x) and sign(one_y) == sign(two_y)


def LOS_blocked(fr, to, asteroids):
    dist_left = to.grid_left - fr.grid_left
    dist_top = to.grid_top- fr.grid_top
    pyth_dist = math.sqrt(dist_left**2 + dist_top**2)
    angle = get_angle(dist_left, dist_top)

    other_asteroids = asteroids.copy()
    other_asteroids.remove(fr)
    other_asteroids.remove(to)

    for ast in other_asteroids:
        ast_dist_left = ast.grid_left - fr.grid_left
        ast_dist_top = ast.grid_top - fr.grid_top
        ast_angle = get_angle(ast_dist_left, ast_dist_top)
        if flequals(ast_angle, angle):
            ast_pyth_dist = math.sqrt(ast_dist_left**2 + ast_dist_top**2)
            if ast_pyth_dist < pyth_dist:
                return True
    return False
        
    

def asteroid_sees_n_asteroids(asteroids):
    res = []
    for asteroid in asteroids:
        num_can_see = 0
        for can_see in asteroids:
            if asteroid == can_see:
                continue
            if LOS_blocked(asteroid, can_see, asteroids):
                continue
            num_can_see += 1
        res.append((asteroid, num_can_see))
    return res

if __name__ == '__main__':
    #test
    a = Asteroid()
    b = Asteroid()
    c = Asteroid()

    a.grid_top = 0
    a.grid_left = 0
    b.grid_top = 5
    b.grid_left = 0
    c.grid_top = 9
    c.grid_left = 0
    
    belt = [a,b,c]
    print(LOS_blocked(a,c,belt))
    print(LOS_blocked(a,b,belt))
    print(LOS_blocked(b,a,belt))
    print(LOS_blocked(c,a,belt))

    input()
    res = asteroid_sees_n_asteroids(belt)
    print(res)
    input()






    belt = []
    with open('input', 'r') as f:
        lines = f.readlines()
    for i,l in enumerate(lines):
        for j,char in enumerate(list(l.strip())):
            if char == '#':
                ast = Asteroid()
                ast.grid_top = i
                ast.grid_left = j
                belt.append(ast)


    res = asteroid_sees_n_asteroids(belt)
    res.sort(key=lambda x: x[1])
    print(res[0])
    print(res[-1])





