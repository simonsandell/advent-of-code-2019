import collections

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __hash__(self):
        return (self.x,self.y).__hash__()
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def get_points_in_line(startpoint, direction, length):
    pts = [startpoint]
    vertical = direction in ('U', 'D')
    positive = direction in ('U', 'R')
    for i in range(1, length + 1):
        if vertical:
            if positive:
                pts.append(Point(startpoint.x, startpoint.y + i))
            else:
                pts.append(Point(startpoint.x, startpoint.y - i))
        else:
            if positive:
                pts.append(Point(startpoint.x + i, startpoint.y))
            else:
                pts.append(Point(startpoint.x - i, startpoint.y))
    return pts
def get_intersectionpoints(l1, l2):
    i = []
    pts1 = get_points_in_line(l1.startpoint, l1.direction, l1.length)
    pts2 = get_points_in_line(l2.startpoint, l2.direction, l2.length)
    for p1 in pts1:
        if p1 in pts2:
            i.append(p1)
    return i
            


class Line:

    def __init__(self, startpoint, dirlen):
        self.startpoint = startpoint # Point
        self.direction = dirlen[0]
        self.vertical = self.direction in ('U', 'D')
        self.positive = self.direction in ('U', 'R')
        self.length = int(dirlen[1:].strip())
        if self.vertical:
            if self.positive:
                self.endpoint = Point(self.startpoint.x, self.startpoint.y + self.length)
            else:
                self.endpoint = Point(self.startpoint.x, self.startpoint.y - self.length)
        else:
            if self.positive:
                self.endpoint = Point(self.startpoint.x + self.length, self.startpoint.y)
            else:
                self.endpoint = Point(self.startpoint.x - self.length, self.startpoint.y)
        self.max_x = max(self.startpoint.x, self.endpoint.x)
        self.min_x = min(self.startpoint.x, self.endpoint.x)
        self.max_y = max(self.startpoint.y, self.endpoint.y)
        self.min_y = min(self.startpoint.y, self.endpoint.y)

    def get_interserctions(self, otherline):
        if self.vertical and otherline.vertical:
            if self.startpoint.x != otherline.startpoint.x:
                return []
            if self.max_y < otherline.min_y or self.min_y > otherline.max_y:
                return []
            return get_intersectionpoints(self, otherline)
        if not self.vertical and not otherline.vertical:
            if self.startpoint.y != otherline.startpoint.y:
                return []
            if self.max_x < otherline.min_x or self.min_x > otherline.max_x:
                return []
            return get_intersectionpoints(self, otherline)
        if not self.vertical and otherline.vertical:
            if self.max_x < otherline.startpoint.x or self.min_x > otherline.startpoint.x:
                return []
            if otherline.max_y < self.startpoint.y or otherline.min_y > self.startpoint.y:
                return []
            return get_intersectionpoints(self, otherline)
        if self.vertical and not otherline.vertical:
            if otherline.max_x < self.startpoint.x or otherline.min_x > self.startpoint.x:
                return []
            if self.max_y < otherline.startpoint.y or self.min_y > otherline.startpoint.y:
                return []
            return get_intersectionpoints(self, otherline)

def dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y- p2.y)


if __name__ == "__main__":
    wires = []
    with open('input', 'r') as f:
        for l in f:
            wires.append(l.split(","))
    wirelines = []
    for wire in wires:
        current_point = Point(0, 0)
        lines = []
        for lineinstruction in wire:
            l = Line(current_point, lineinstruction)
            lines.append(l)
            current_point = l.endpoint
        wirelines.append(lines)
    intersectiondict = {}
    for l in wirelines[0]:
        for l2 in wirelines[1]:
            i = l.get_interserctions(l2)
            for intersection in i:
                intersectiondict[intersection] = dist(intersection, Point(0,0))

    sorted_x = sorted(intersectiondict.items(), key =lambda kv: kv[1])
    print(sorted_x[1][1])
