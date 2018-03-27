import random


# Finding i and j coordinates of the empty tile
def zero_ij(current_state):
    ij = []
    for entry in current_state:
        if current_state[entry] == 0:
            i = (entry) // 3
            j = (entry) % 3
    ij.append(i)
    ij.append(j)
    return ij

# Finding possible moves North East South West
def possible_moves(ij):
    moves = []
    if ij[0] - 1 >= 0:
        moves.append('North')
    if ij[1] + 1 <= 2:
        moves.append('East')
    if ij[0] + 1 <= 2:
        moves.append('South')
    if ij[1] - 1 >= 0:
        moves.append('West')
    return moves

# finding amount of available moves
def available_moves_amount(available_moves):
    return len(available_moves)

# Function to delete the step that returns back from the available steps
def back_move_excluder(available_moves, next_move, number_available_moves):
    result = []
    if next_move == 'North':
        available_moves.remove('South')
        number_available_moves -= 1
    if next_move == 'East':
        available_moves.remove('West')
        number_available_moves -= 1
    if next_move == 'South':
        available_moves.remove('North')
        number_available_moves -= 1
    if next_move == 'West':
        available_moves.remove('East')
        number_available_moves -= 1
    else:
        available_moves = available_moves
    result.append(number_available_moves)
    result.append(available_moves)
    return result

# adding all info about the state to a single list named info_carrier
def combiner(info_carrier, next_move, ij,
             number_available_moves, available_moves,
             previous_expand_index, current_state, punish_value):
    info_carrier.extend(current_state)
    next_move_cap = next_move[0]
    info_carrier.append(next_move_cap)
    info_carrier.extend(ij)
    info_carrier.append(number_available_moves)
    info_carrier.extend(available_moves)
    info_carrier.append(punish_value)
    info_carrier.append(previous_expand_index)
    return info_carrier

# Add the info carrier to state space
def state_space_add(space_state, info_carrier):
    space_state.append(info_carrier)
    return space_state

# Make a frontier list
def make_frontier(state_space):
    frontier = []
    for i in state_space:
        if i[12] != 0:
            frontier.append(i)
    return frontier

# Find a state to expand next
def who_is_next(frontier):
    values = []
    for i in frontier:
        err = i[-2]
        values.append(err)
    min_index = values.index(min(values))
    return frontier[min_index]

# Finding the next move
def find_next_move(expand):
    next_move = expand[13]
    return next_move

# Function to find each state index
def state_index_finder(state_space, expand):
    current_index = state_space.index(expand)
    return current_index

# Adding punishment function
def punish(expand):
    punishment = expand[-2]
    punishment += 1
    return punishment

# Function to update the state info report after every taken step
def update_state_info(expand, next_move):
    remove_value = expand[13]
    expand.remove(remove_value)
    expand[12] -= 1
    return expand

# Updating state space with an index of the previously expanded state
def updated_state_space(state_space, expand, index_expand):
    state_space[index_expand] = expand
    return state_space

# Finding ij coordinates of a state to expand
def ij_after_expand(expand):
    ij_frame = expand[:9]
    ij = []
    i,j = 0,0
    for entry in ij_frame:
        if ij_frame[entry] == 0:
            i = (entry) // 3
            j = (entry) % 3
    ij.append(i)
    ij.append(j)
    return ij

# Finding the values of i and j coordinates of a new position of an empty tile
def new_zero_position_ij(ij, next_move):
    new_ij = [0,0]
    new_ij[0] = ij[0]
    new_ij[1] = ij[1]
    if next_move == 'North':
        new_ij[0] -= 1
    if next_move == 'East':
        new_ij[1] += 1
    if next_move == 'South':
        new_ij[0] += 1
    if next_move == 'West':
        new_ij[1] -= 1
    return new_ij

# Finding a new state
def new_state(ij, new_ij, expand):
    new_state = expand[:9]
    old_num_index = ij[0] * 3 + ij[1]
    new_num_index = new_ij[0] * 3 + new_ij[1]
    old_num_value = new_state[old_num_index]
    new_num_value = new_state[new_num_index]
    new_state[old_num_index] = new_num_value
    new_state[new_num_index] = 0
    return new_state

# Making a list of solution state indexes
def solution_state_index(solution_index, state_space):
    tracker = 0
    next_to_check = 0
    i = 1
    solution_index.append(len(state_space) - 1)
    while i != 0:
        prev_step = solution_index[tracker]
        state_to_add = state_space[prev_step]
        state_last_digit = state_to_add[-1]
        solution_index.append(state_last_digit)
        tracker += 1
        i = state_last_digit
    return solution_index

# Making a solution states list
def solution_state_all(solution_steps, solution_index, state_space):
    for i in solution_index:
        state_to_append = state_space[i]
        solution_steps.append(state_to_append)
    return solution_steps

# Printing out everything
def fancy_output(show):
        print(show[0], '', show[1], '', show[2])
        print(show[3], '', show[4], '', show[5])
        print(show[6], '', show[7], '', show[8])
        print('\n')

# Mixing input values
def mixer(g_state, trials):
    new_next_state = g_state
    while trials > 0:
        current_state = new_next_state
        ij = zero_ij(current_state)
        available_moves = possible_moves(ij)
        max_num = len(available_moves) - 1
        min_num = 0
        shuffle_move_index = random.randint(min_num, max_num)
        next_move = available_moves[shuffle_move_index]
        new_ij = new_zero_position_ij(ij, next_move)
        expand = current_state
        new_next_state = new_state(ij, new_ij, expand)
        trials -= 1
    return new_next_state

# Asking a user to input the winning state
def winning_state():
    print('x00','x01','x02')
    print('x10','x11','x12')
    print('x20','x21','x22')
    print('Input the values accordingly')
    x00_string = input('type in x00: ')
    x00 = int(x00_string)
    x01_string = input('type in x01: ')
    x01 = int(x01_string)
    x02_string = input('type in x02: ')
    x02 = int(x02_string)
    x10_string = input('type in x10: ')
    x10 = int(x10_string)
    x11_string = input('type in x11: ')
    x11 = int(x11_string)
    x12_string = input('type in x12: ')
    x12 = int(x12_string)
    x20_string = input('type in x20: ')
    x20 = int(x20_string)
    x21_string = input('type in x21: ')
    x21 = int(x21_string)
    x22_string = input('type in x22: ')
    x22 = int(x22_string)
    goal_state = [x00,x01,x02,x10,x11,x12,x20,x21,x22]
    return goal_state


solution_index = []
solution_steps = []
next_move = 'Appear'
previous_expand_index = -1
frontier = []
state_space = []
punish_value = 0
#g_state = winning_state()
g_state = [0,1,2,3,4,5,6,7,8]
#trials_string = input('how many times do you want to shuffle the goal state?: ')
#trials = int(trials_string)
#next_state = mixer(g_state, trials)
next_state = [1,2,5,3,4,8,6,7,0]
current_state = next_state

while current_state != g_state:
    current_state = next_state
    info_carrier = []
    ij = zero_ij(current_state)
    available_moves = possible_moves(ij)
    number_available_moves = available_moves_amount(available_moves)
    available_moves_list = back_move_excluder(available_moves, next_move, number_available_moves)
    number_available_moves = available_moves_list[0]
    available_moves = available_moves_list[1]
    info_carrier = combiner(info_carrier, next_move, ij, number_available_moves, available_moves,
                                    previous_expand_index, current_state, punish_value)
    state_space = state_space_add(state_space, info_carrier)
    frontier = make_frontier(state_space)
    expand = who_is_next(frontier)
    next_move = find_next_move(expand)
    index_expand = state_index_finder(state_space, expand)
    previous_expand_index = index_expand
    punish_value = punish(expand)
    expand = update_state_info(expand, next_move)
    state_space = updated_state_space(state_space, expand, index_expand)
    frontier = make_frontier(state_space)
    ij = ij_after_expand(expand)
    new_ij = new_zero_position_ij(ij, next_move)
    next_state = new_state(ij, new_ij, expand)
solution_index = solution_state_index(solution_index, state_space)
solution_steps = solution_state_all(solution_steps, solution_index, state_space)
print('solution indexes', solution_index)
print('solution steps', solution_steps)
print('it took me', len(solution_index),'steps to solve your puzzle')
print('but took me', len(state_space),'steps to find the solution')
for i in solution_steps:
    show = i
    fancy_output(show)
