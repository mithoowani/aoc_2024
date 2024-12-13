import numpy as np
import time

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


def parse_input(puzzle_input):
	# Return puzzle input as a 2-d numpy array

	array = puzzle_input.split('\n')
	array_lists = []
	for line in array:
		array_lists.append(list(line))
	return np.array(array_lists)


def initialize_empty_visited(grid: np.array, guard_loc) -> np.array:
	# Returns an empty np array of all locations visited so far
	# 0 = not visited; 1 = visited
	visited = np.zeros_like(grid, dtype='int64')
	visited = mark_visited(visited, guard_loc)
	return visited


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
	else:
		new_guard_loc = np.array([guard_loc[0], guard_loc[1] + 1])
	return new_guard_loc


def mark_visited(visited, guard_loc) -> np.array:
	# Finds the guard and marks his current location as visited
	visited[guard_loc[0], guard_loc[1]] = 1
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
# puzzle_grid = parse_input(TEST_INPUT)
# print(puzzle_grid)

# Real input
with open('input.txt', 'r') as f:
	puzzle_grid = parse_input(f.read())

current_loc = np.argwhere(puzzle_grid == '^')[0]
# print(current_pos)

visited_squares = initialize_empty_visited(puzzle_grid, current_loc)
# print(visited_squares)

current_direction = 'up'  # Assumption is that the guard always starts facing upward

# Part A
pre_time = time.time()
while not is_exiting(puzzle_grid, current_loc, current_direction):
	current_direction = get_new_direction(puzzle_grid, current_loc, current_direction)
	current_loc = move_guard(current_loc, current_direction)
	visited_squares = mark_visited(visited_squares, current_loc)
post_time = time.time()

print(np.sum(visited_squares))
print(post_time - pre_time)
