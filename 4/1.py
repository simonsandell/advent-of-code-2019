MIN = 193651
MAX = 649729

def get_digits(n):
    digits = []
    for i in range(6):
        digits.append(n % pow(10, i+1) // pow(10, i))
    digits.reverse()
    return digits

def repeating_and_increasing(digits):
    d = [x-y for x,y in zip(digits[:-1], digits[1:])]
    if 0 in d :
        for diff in d:
            if diff > 0:
                return False
        return True
    return False

count = 0
for i in range(MIN, MAX):
    digs = get_digits(i)
    if repeating_and_increasing(digs):
        count += 1
print(count)

    
