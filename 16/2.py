if __name__ == "__main__":
    with open("input", "r") as f:
        inp = f.read().strip()
    message_offset = int(inp[0:7])

    l = [int(c) for c in inp]*10000
    l = l[message_offset:]

    l.reverse()
    for _ in range(100):
        print(_)
        for i,__ in enumerate(l):
            if i == 0:
                continue
            l[i] = ((l[i] + l[i-1]) % 10)
    l.reverse()
    print(l[:8])
