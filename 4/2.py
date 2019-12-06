MIN = 193651
MAX = 649729

def get_digits(n):
    digits = []
    for i in range(6):
        digits.append(n % pow(10, i+1) // pow(10, i))
    digits.reverse()
    return digits

def get_diffs(digits):
    return [x-y for x,y in zip(digits[:-1], digits[1:])]

def increasing(d):
    for diff in d:
       if diff > 0:
           return False
    return True

def indices(l, el):
    result = []
    offset = -1
    while True:
        try:
            offset = l.index(el, offset+1)
        except ValueError:
            return result
        result.append(offset)

def matching(diffs):
    if not 0 in diffs:
        return False
    # find isolated zero
    inds = indices(diffs, 0)
    for i in inds:
        if not (i-1 in inds) and not (i+1 in inds):
            return True
    return False

count = 0
for i in range(MIN, MAX):
    digs = get_digits(i)
    diffs = get_diffs(digs)
    if increasing(diffs) and matching(diffs):
        count += 1
print(count)

    
