
def get_pattern(n, size):
    base = (n-1)*[0] + n*[1] + n*[0] + n*[-1] + [0]
    factor = 1 + (size // len(base))
    return (base*factor)[0:size]

def mult_sum_lists(l1, l2):
    return abs(sum([e1*e2 for e1,e2 in zip(l1,l2)])) % 10

def FFT(l):
    r = []
    for i in range(len(l)):
        r.append(mult_sum_lists(l, get_pattern(i + 1, len(l))))
    return r


if __name__ == "__main__":
    with open("input", "r") as f:
        inp = f.read().strip()
    l = [int(c) for c in inp]
    for _ in range(100):
        l = FFT(l)
    print(l[0:8])
