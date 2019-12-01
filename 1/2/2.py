
def get_fuel(weight):
    p = int(int(weight)/3.0) - 2
    if p < 0:
        return 0
    return p

def get_realfuel(weight):
    base = get_fuel(weight)
    total = base
    while True:
        new = get_fuel(base)
        total += new
        base = new
        if new == 0:
            return total
totfuel = 0 
with open('input', 'r') as f:
    for l in f:
        totfuel += get_realfuel(l)
print(totfuel)


