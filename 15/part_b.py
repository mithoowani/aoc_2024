import numpy as np

TEST_INPUT_1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

TEST_INPUT_2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


def parse_input(puzzle_input: str):
	moves_ = list(puzzle_input.split('\n\n')[1])
	maze_ = puzzle_input.split('\n\n')[0].split('\n')

	modified_maze = []

	# modify maze based on instructions in part b
	for line in maze_:
		modified_maze.append(line.replace('#', '##').
							 replace('O', '[]').
							 replace('.', '..').
							 replace('@', '@.'))

	maze_lists = []
	for line in modified_maze:
		maze_lists.append(list(line))
	maze_array = np.array(maze_lists)

	# cleans up new line characters from input
	moves_ = [element for element in moves_ if element != '\n']

	return moves_, maze_array


def pretty_print_maze(maze_):
	"""Neatly prints the maze to terminal (helper function for debugging)"""
	for line in maze_:
		print(''.join(line))


def find_robot(maze_):
	"""Returns the location of the robot in form (row, col)"""
	robot_loc = (int(np.where(maze_ == '@')[0][0]),
				 int(np.where(maze_ == '@')[1][0]))
	return robot_loc


def move_robot_left(maze_: np.array) -> np.array:
	"""Moves robot left (if possible), returns the modified maze"""
	loc_row, loc_col = find_robot(maze_)
	squares_to_move = list()

	# creates a stack of tile coordinates to shift, including robot and boxes
	i = 0
	while maze_[loc_row, loc_col - i] in '[]@':
		squares_to_move.append((loc_row, loc_col - i))
		i += 1

	# if the space beyond the last tile is a free space, shift everything in the stack by 1 column
	if maze_[loc_row, loc_col - i] == '.':
		while squares_to_move:
			square = squares_to_move.pop()
			maze_[square[0], square[1] - 1] = maze_[square[0], square[1]]

		# create a free space where the robot used to be
		maze_[loc_row, loc_col] = '.'

	return maze_


def move_robot_right(maze_: np.array) -> np.array:
	"""Moves robot right (if possible), returns the modified maze"""
	loc_row, loc_col = find_robot(maze_)
	squares_to_move = list()

	# creates a stack of tile coordinates to shift, including robot and boxes
	i = 0
	while maze_[loc_row, loc_col + i] in '[]@':
		squares_to_move.append((loc_row, loc_col + i))
		i += 1

	# if the space beyond the last tile is a free space, shift everything in the stack by 1 column
	if maze_[loc_row, loc_col + i] == '.':
		while squares_to_move:
			square = squares_to_move.pop()
			maze_[square[0], square[1] + 1] = maze_[square[0], square[1]]

		# create a free space where the robot used to be
		maze_[loc_row, loc_col] = '.'

	return maze_


def move_robot_up(maze_: np.array):
	"""Moves robot up (if possible), returns the modified maze"""
	global can_move

	# Retrieve all boxes that need to be moved
	boxes_to_move = get_boxes_up(maze_)

	if can_move:
		robot_loc = find_robot(maze_)
		boxes_to_move.sort(key=lambda x: x[0])  # by row
		for box in boxes_to_move:
			maze_[box[0] - 1, box[1]] = maze_[box[0], box[1]]
			maze_[box[0], box[1]] = '.'

		# move robot up at the end
		maze_[robot_loc[0] - 1, robot_loc[1]] = '@'
		maze_[robot_loc[0], robot_loc[1]] = '.'

	return maze_


def move_robot_down(maze_: np.array):
	"""Moves robot up (if possible), returns the modified maze"""
	global can_move

	# Retrieve all boxes that need to be moved
	boxes_to_move = get_boxes_down(maze_)

	if can_move:
		robot_loc = find_robot(maze_)
		boxes_to_move.sort(key=lambda x: x[0], reverse=True)  # by row, in reverse order (so bottom box moves first)

		for box in boxes_to_move:
			maze_[box[0] + 1, box[1]] = maze_[box[0], box[1]]
			maze_[box[0], box[1]] = '.'

		# move robot down at the end
		maze_[robot_loc[0] + 1, robot_loc[1]] = '@'
		maze_[robot_loc[0], robot_loc[1]] = '.'

	return maze_


def get_boxes_up(maze_: np.array, row: int = None, col: int = None, seen=None):
	"""Returns a list of boxes that need to be moved upwards, essentially a depth first search"""

	global can_move

	if seen is None:
		seen = []

	# first call to function looks at square immediately above the robot
	if row is None or col is None:
		robot_loc = find_robot(maze_)
		return get_boxes_up(maze_, robot_loc[0] - 1, robot_loc[1])

	if maze_[row, col] == '#':
		can_move = False

	elif maze_[row, col] in '[]' and (row, col) not in seen:
		seen.append((row, col))

		# call recursively on box immediately above the current box
		get_boxes_up(maze_, row - 1, col, seen)

		# call recursively on the other tile comprising the current box
		if maze_[row, col] == '[':
			get_boxes_up(maze_, row, col + 1, seen)

		elif maze_[row, col] == ']':
			get_boxes_up(maze_, row, col - 1, seen)

	return seen


def get_boxes_down(maze_: np.array, row: int = None, col: int = None, seen=None):
	"""Returns a list of boxes that need to be moved upwards, essentially a depth first search"""

	global can_move

	if seen is None:
		seen = []

	# first call to function looks at square immediately below robot
	if row is None or col is None:
		robot_loc = find_robot(maze_)
		return get_boxes_down(maze_, robot_loc[0] + 1, robot_loc[1])

	if maze_[row, col] == '#':
		can_move = False

	elif maze_[row, col] in '[]' and (row, col) not in seen:
		seen.append((row, col))

		# call recursively on box immediately below the current box
		get_boxes_down(maze_, row + 1, col, seen)

		# call recursively on the other tile comprising the current box
		if maze_[row, col] == '[':
			get_boxes_down(maze_, row, col + 1, seen)

		elif maze_[row, col] == ']':
			get_boxes_down(maze_, row, col - 1, seen)

	return seen


def get_sum_gps(maze_: np.array) -> int:
	"""Returns the sum of all GPS coordinates for a maze (using rules from part b)"""
	box_locations = np.where(maze_ == '[')

	# GPS = 100 * distance from the top + distance from the left
	result = np.sum(box_locations[0] * 100 + box_locations[1])

	return result


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

moves, maze = parse_input(REAL_INPUT)

move_robot = {'<': move_robot_left,
			  '>': move_robot_right,
			  '^': move_robot_up,
			  'v': move_robot_down}

for direction in moves:
	can_move = True
	move_robot[direction](maze)

pretty_print_maze(maze)
print()
print(f'Part B: {get_sum_gps(maze)}')
