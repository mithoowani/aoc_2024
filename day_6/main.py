import numpy as np

TEST_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

# From reddit
TEST_INPUT_2 = """.##..
....#
.....
.^.#.
....."""

# From reddit
TEST_INPUT_3 = """.#....
.....#
#..#..
..#...
.^...#
....#."""

# Integers in this dictionary are arbitrary
DIRECTION_TO_INT = {'up': 1,
					'down': 2,
					'left': 3,
					'right': 4}


def parse_input(puzzle_input):
	# Return puzzle input as a 2-d numpy array

	array = puzzle_input.split('\n')
	array_lists = []
	for line in array:
		array_lists.append(list(line))
	return np.array(array_lists)


def get_new_direction(grid, guard_loc, direction) -> str:
	# Checks if the guard is directly facing an obstacle; if yes returns new guard direction (right by 90 deg)
	# Otherwise returns false
	if direction == 'up' and grid[guard_loc[0] - 1, guard_loc[1]] == '#':
		return 'right'
	elif direction == 'down' and grid[guard_loc[0] + 1, guard_loc[1]] == '#':
		return 'left'
	elif direction == 'left' and grid[guard_loc[0], guard_loc[1] - 1] == '#':
		return 'up'
	elif direction == 'right' and grid[guard_loc[0], guard_loc[1] + 1] == '#':
		return 'down'
	else:
		return direction


def move_guard(guard_loc, direction) -> np.array:
	# Moves guard by one square in the direction that he's facing
	# Returns guard's new location after the move
	if direction == 'up':
		new_guard_loc = np.array([guard_loc[0] - 1, guard_loc[1]])
	elif direction == 'down':
		new_guard_loc = np.array([guard_loc[0] + 1, guard_loc[1]])
	elif direction == 'left':
		new_guard_loc = np.array([guard_loc[0], guard_loc[1] - 1])
	elif direction == 'right':
		new_guard_loc = np.array([guard_loc[0], guard_loc[1] + 1])
	return new_guard_loc


def mark_visited(visited, guard_loc, direction) -> np.array:
	# Finds the guard and marks his current location as visited
	visited[guard_loc[0], guard_loc[1]] = DIRECTION_TO_INT[direction]
	return visited


def is_exiting(grid, guard_loc, direction) -> bool:
	# Returns true if the guard is exiting the maze with a move in the direction
	if direction == 'up' and guard_loc[0] == 0:
		return True
	elif direction == 'down' and guard_loc[0] == grid.shape[0] - 1:
		return True
	elif direction == 'left' and guard_loc[1] == 0:
		return True
	elif direction == 'right' and guard_loc[1] == grid.shape[1] - 1:
		return True
	else:
		return False


# Test input
# puzzle_grid = parse_input(TEST_INPUT_3)
# print(puzzle_grid)

# Real input
with open('input.txt', 'r') as f:
	puzzle_grid = parse_input(f.read())

current_loc = np.argwhere(puzzle_grid == '^')[0]
# print(current_pos)

current_direction = 'up'  # Assumption is that the guard always starts facing upward

visited_squares = np.zeros_like(puzzle_grid, dtype='int64')
visited_squares = mark_visited(visited_squares, current_loc, current_direction)
# print(visited_squares)

# Part A
while not is_exiting(puzzle_grid, current_loc, current_direction):
	current_direction = get_new_direction(puzzle_grid, current_loc, current_direction)
	current_loc = move_guard(current_loc, current_direction)
	visited_squares = mark_visited(visited_squares, current_loc, current_direction)
print('Part A:', np.count_nonzero(visited_squares))

# Part B
count = 0

# Only evaluate positions of the new obstacle that the guard originally visited in part A
all_possible_locations = np.argwhere(visited_squares > 0)
starting_loc = np.argwhere(puzzle_grid == '^')[0]
filt = ~(all_possible_locations == [starting_loc[0], starting_loc[1]]).all(axis=1)
all_possible_locations = all_possible_locations[filt]

for location in all_possible_locations:
	# Re-initialize all variables
	new_grid = np.copy(puzzle_grid)
	current_loc = starting_loc
	current_direction = 'up'
	visited_squares = np.zeros_like(new_grid, dtype='int64')

	# Add new obstacle to the grid
	new_grid[location[0], location[1]] = '#'

	while not is_exiting(new_grid, current_loc, current_direction):
		if visited_squares[current_loc[0], current_loc[1]] == DIRECTION_TO_INT[current_direction]:
			count += 1
			break
		visited_squares = mark_visited(visited_squares, current_loc, current_direction)
		for _ in range(3):  # This takes into account that guard might face another obstacle immediately after turning
			current_direction = get_new_direction(new_grid, current_loc, current_direction)
		current_loc = move_guard(current_loc, current_direction)

print('Part B:', count)
