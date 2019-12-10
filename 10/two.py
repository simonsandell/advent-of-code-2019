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
    return -math.atan2( -x, -y)

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

    for ast in asteroids:
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

def get_asteroids_seeable(asteroid, belt):
    res = []
    for ast in belt:
        if not LOS_blocked(asteroid, ast, belt):
            angle = get_angle(asteroid.grid_left-ast.grid_left, asteroid.grid_top - ast.grid_top)
            res.append((angle,ast))
    return res

def fire_lazor(starbase, belt, number_of_kills):
    obliterees = []
    poor_souls = get_asteroids_seeable(starbase, belt)
    poor_souls.sort(key=lambda x: x[0])
    for soul in poor_souls:
        number_of_kills += 1
        obliterees.append((number_of_kills, soul[1]))
    return obliterees



if __name__ == '__main__':
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

    for ast in belt:
        if ast.grid_top == 20 and ast.grid_left == 20:
            starbase = ast
            break
    belt.remove(starbase)
    victims = 0
    rounds = {}
    k = 0
    while len(belt) > 0:
        k += 1
        obliterees = fire_lazor(starbase, belt, victims)
        victims += len(obliterees)
        for obliteree in obliterees:
            belt.remove(obliteree[1])
        rounds[k] = obliterees
    for key,value in rounds.items():
        print('round',key)
        for ast in value:
            print(ast[0], ast[1])
            if ast[0] == 200:
                input()

