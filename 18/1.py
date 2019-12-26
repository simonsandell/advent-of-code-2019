import Tiles
from queue import Queue

if __name__ == '__main__':
    with open('input', 'r') as f:
        maze = f.read().strip().split('\n')

    tiles = Tiles.Tiles()
    for y, line  in enumerate(maze):
        for x, char in enumerate(line):
            tiles.set_color((x, y), char)
    lengths = set()
    target_num_keys = len(tiles.keys)

    cache = {}

    #def DFS(tiles, held_keys, start_v, w):
    #    adjacent_keys = tiles.get_adjacent_keys(start_v, held_keys)
    #    if len(adjacent_keys) == 0:
    #        if len(held_keys) == target_num_keys:
    #            lengths.add(w)
    #            return
    #        raise Exception("locked in somehow")
    #    for adj in adjacent_keys:
    #        new_keys = held_keys.copy()
    #        new_keys.add(tiles.keys_rev[adj])
    #        state = (adj, tiles.encode_keys(new_keys))
    #        if state not in cache:
    #            DFS(tiles, new_keys, adj, adjacent_keys[adj] + w)
    #            cache.add(state)
    #        print(lengths)


    #DFS(tiles, set(), tiles.player, 0)
    #print(lengths)
    #print(len(lengths))
    #print(min(lengths))

    queue = Queue()
    queue.put((tiles.player, set(), 0))

    while not queue.empty():
        start_v, held_keys, w = queue.get()
        adjacent_keys = tiles.get_adjacent_keys(start_v, held_keys)
        if len(held_keys) == target_num_keys:
                lengths.add(w)
        else:
            for adj in adjacent_keys:
                new_keys = held_keys.copy()
                new_keys.add(tiles.keys_rev[adj])
                state = (adj, tiles.encode_keys(new_keys))
                if state not in cache:
                    queue.put((adj, new_keys, adjacent_keys[adj] + w))
                    cache[state] = w + adjacent_keys[adj]
                elif cache[state] > w + adjacent_keys[adj]:
                    queue.put((adj, new_keys, adjacent_keys[adj] + w))
                    cache[state] = w + adjacent_keys[adj]

                print(state)

    print(lengths)
    print(len(lengths))
    print(min(lengths))


#3     for all edges e in G.incidentEdges(v) do
#4         if edge e is unexplored then
#5             w ← G.adjacentVertex(v, e)
#6             if vertex w is unexplored then
#7                 label e as a discovered edge
#8                 recursively call DFS(G, w)
#9             else
#10               label e as a back edge
    ####
    # Dijkstra's
    ####
    # Mark all nodes unvisited. 
    # Create a set of all the unvisited nodes called the unvisited set.
    #class Dijkstra:
    #    def __init__(self):
    #        self.unvisited_set = set()
    #        self.visited_set = set()
    #        self.tentative_distance = {}
    #        self.held_keys = {}

    #        self.current_node = None
    #dijkstra = Dijkstra()
    #dijkstra.unvisited_set = set(tiles.keys.values())

    ### Assign to every node a tentative distance value:
    ### set it to zero for our initial node and to infinity for all other nodes.
    #infinity = 9999999999
    #for node in dijkstra.unvisited_set:
    #    dijkstra.tentative_distance[node] = infinity
    #    dijkstra.held_keys[node] = []
    #dijkstra.unvisited_set.add(tiles.player)
    #dijkstra.tentative_distance[tiles.player] = 0
    #dijkstra.held_keys[tiles.player] = []

    ### Set the initial node as current.
    #dijkstra.current_node = tiles.player

    #while True:
    #    # print()
    #    # print()
    #    # print('numkeys',len(tiles.held_keys),"/",len(tiles.keys))
    #    # print(tiles.get_color(dijkstra.current_node))
    #    # print(dijkstra.tentative_distance[dijkstra.current_node])

    #    # For the current node,
    #    # consider all of its unvisited neighbours and calculate their
    #    # tentative distances through the current node.
    #    print(dijkstra.current_node)
    #    print(dijkstra.tentative_distance)
    #    print(dijkstra.unvisited_set)
    #    tiles.update_doors(dijkstra.held_keys[dijkstra.current_node])
    #    adjacent_keys = tiles.get_adjacent_keys(dijkstra.current_node)
    #    # Compare the newly calculated tentative distance to the
    #    # current assigned value and assign the smaller one.
    #    for adj in adjacent_keys:
    #        if tiles.get_color(adj) not in tiles.keys:
    #            raise Exception("got non-key")
    #        tot = (dijkstra.tentative_distance[dijkstra.current_node] + 
    #                adjacent_keys[adj])
    #        if tot < dijkstra.tentative_distance[adj]:
    #            dijkstra.tentative_distance[adj] = tot
    #            hkeys = dijkstra.held_keys[dijkstra.current_node].copy()
    #            hkeys.append(tiles.get_color(adj))
    #            dijkstra.held_keys[adj] = hkeys

    #    # For example, if the current node A is marked with a distance of 6,
    #    # and the edge connecting it with a neighbour B has length 2,
    #    # then the distance to B through A will be 6 + 2 = 8.

    #    # If B was previously marked with a distance greater than 8 then change it to 8.
    #    # Otherwise, the current value will be kept.

    #    # When we are done considering all of the unvisited neighbours of the
    #    # current node, mark the current node as visited and remove it from the
    #    # unvisited set.
    #    # A visited node will never be checked again.
    #    dijkstra.visited_set.add(dijkstra.current_node)
    #    dijkstra.unvisited_set.remove(dijkstra.current_node)

    #    # If the smallest tentative distance among the nodes
    #    # in the unvisited set is infinity (when planning a complete traversal;
    #    # occurs when there is no connection between the initial node and
    #    # remaining unvisited nodes), then stop. The algorithm has finished.
    #    if len(dijkstra.unvisited_set) == 0:
    #        break

    #    # Otherwise, select the unvisited node that is marked with the
    #    # smallest tentative distance, set it as the new "current node",
    #    # and go back to step 3.
    #    mindist = infinity
    #    minnode = None
    #    for node in dijkstra.unvisited_set:
    #        if dijkstra.tentative_distance[node] < mindist:
    #            mindist = dijkstra.tentative_distance[node]
    #            minnode = node
    #    if mindist == infinity:
    #        raise Exception("no nodes available")
    #    
    #    dijkstra.current_node = minnode


    #print(dijkstra.tentative_distance[dijkstra.current_node])
    #[print(k) for k in tiles.keys.keys() if k not in tiles.held_keys]
        
