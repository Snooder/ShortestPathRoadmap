import random
import Queue

''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For Search Algorithms
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''

q = Queue.Queue()
p = Queue.LifoQueue()
r = Queue.PriorityQueue()

'''
BFS add to queue
'''
def add_to_queue_BFS(node_id, parent_node_id, cost, initialize=False):
	if initialize == True:
		q.queue.clear()
	q.put((node_id, parent_node_id))
	return

'''
BFS add to queue
'''
def is_queue_empty_BFS():
	if (q.empty()):
		return True
	else:
		return False

'''
BFS pop from queue
'''
def pop_front_BFS():
    return (q.get())

'''
DFS add to queue
'''
def add_to_queue_DFS(node_id, parent_node_id, cost, initialize=False):
	if initialize == True:
		while (not p.empty):
			p.get()
	p.put((node_id,parent_node_id))
	return

'''
DFS add to queue
'''
def is_queue_empty_DFS():
	if (p.empty()):
		return True
	else:
		return False

'''
DFS pop from queue
'''
def pop_front_DFS():
    return (p.get())

'''
UC add to queue
'''
def add_to_queue_UC(node_id, parent_node_id, cost, initialize=False):
	if initialize == True:
		while (not r.empty):
			r.get()
	r.put((cost,node_id,parent_node_id))
	return


def is_queue_empty_UC():
	if (r.empty()):
		return True
	else:
		return False

'''
UC pop from queue
'''
def pop_front_UC():
	(node_id, parent_node_id) = (0, 0)
	node = r.get()
	(node_id, parent_node_id) = (node[1],node[2])
	return (node_id, parent_node_id)

'''
A* add to queue
'''
def add_to_queue_ASTAR(node_id, parent_node_id, cost, initialize=False):
    if initialize == True:
        while (not(r.empty())):
            r.get()
    r.put(tuple([cost, node_id, parent_node_id]))
    return

'''
A* add to queue
'''
def is_queue_empty_ASTAR():
    if (r.empty()):
        return True
    else:
        return False

'''
A* pop from queue
'''
def pop_front_ASTAR():
    (node_id, parent_node_id) = (0, 0)
    node = r.get()
    (node_id, parent_node_id) = (node[1], node[2])
    return (node_id, parent_node_id)

''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For n-queens problem
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''


'''
Compute a random state
'''
def get_random_state(n):
    state = []
    for x in range(0, n, 1):
        state.append(random.randint(1,n))
    return state

'''
Compute pairs of queens in conflict
'''
def compute_attacking_pairs(state):
    number_attacking_pairs = 0
    for x in range(0, len(state)-1, 1):
        for y in range(x+1, len(state), 1):
            if state[x] == state[y]:
                number_attacking_pairs += 1
            else:
                diff = y - x
                if state[x] - diff == state[y]:
                    number_attacking_pairs += 1
                elif state[x] + diff == state[y]:
                    number_attacking_pairs += 1
    return number_attacking_pairs

'''
The basic hill-climing algorithm for n queens
'''
def hill_desending_n_queens(state, comp_att_pairs):
    final_state = []
    # find the lowest heuristic value and move the queen there
    heuristic_val = comp_att_pairs(state)
    min_heuristic_val = heuristic_val

    x_val = 0
    y_val = 0

    while min_heuristic_val != 0:
        new_state = list(state)
        for x in range(0, len(new_state), 1):
            for y in range(1, len(new_state)+1, 1):
                new_state[x] = y
                new_heuristic_val = comp_att_pairs(new_state)
                if new_heuristic_val < min_heuristic_val:
                    min_heuristic_val = new_heuristic_val
                    x_val = x
                    y_val = y
            new_state = list(state)
        if min_heuristic_val == heuristic_val:
            final_state = list(new_state)
            break
        heuristic_val = min_heuristic_val
        state[x_val] = y_val

    final_state = list(state)
    return final_state

'''
Hill-climing algorithm for n queens with restart
'''
def n_queens(n, get_rand_st, comp_att_pairs, hill_descending):
    final_state = []
    if n <= 3:
        return "No Valid Solution"
    state = get_rand_st(n)
    while comp_att_pairs(state) != 0:
        state = hill_descending(state, comp_att_pairs)
        if comp_att_pairs(state) > 0:
            state = get_rand_st(n)
    final_state = state
    return final_state
