from queue import Queue
import Tiles2

if __name__ == '__main__':
    with open('input2', 'r') as f:
        maze = f.read().strip().split('\n')

    tiles = Tiles2.Tiles()
    for y, line  in enumerate(maze):
        for x, char in enumerate(line):
            tiles.set_color((x, y), char)

    tiles.assign_to_robots()
    tiles.assign_door_to_key()
    tiles.assign_needed_keys()
    tiles.clear_robot_symbols()

    target_num_keys = len(tiles.keys)
    lengths = set()

    cache = {}

    #bfs
    queue = Queue()

    # a state is described by all held keys, positions of the robots, and taken steps
    queue.put((tiles.robot_starts, set(), 0))

    while not queue.empty():
        robpositions, hkeys, w = queue.get()
        if len(hkeys) == target_num_keys:
            lengths.add(w)

        # get possible next states, append these to the queue
        for i,robpos in enumerate(robpositions):
            adjkeys = tiles.get_nn_weights(robpos, hkeys)
            for adj in adjkeys:
                nkeys = hkeys.copy()
                nkeys.add(adj)
                npos = robpositions.copy()
                npos[i] = adj
                state = (tuple(npos), tiles.encode_keys(nkeys))
                if state not in cache:
                    cache[state] = w + adjkeys[adj]
                    queue.put((npos, nkeys, w + adjkeys[adj]))
                elif cache[state] > w + adjkeys[adj]:
                    cache[state] = w + adjkeys[adj]
                    queue.put((npos, nkeys, w + adjkeys[adj]))
                print(len(nkeys))
    print(lengths)
    print(len(lengths))
    print(min(lengths))
