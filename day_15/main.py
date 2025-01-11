from collections import deque
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
	moves_ = puzzle_input.split('\n\n')[1]
	maze_ = puzzle_input.split('\n\n')[0].split('\n')

	maze_lists = []
	for line in maze_:
		maze_lists.append(list(line))
	maze_array = np.array(maze_lists)

	# starting location of robot
	robot_location = (int(np.where(maze_array == '@')[0][0]),
					  int(np.where(maze_array == '@')[1][0]))

	return deque(moves_), maze_array, robot_location


def move_robot(direction_: str, maze_: np.array, loc_: tuple):
	new_robot_loc = loc_
	loc_row = loc_[0]
	loc_col = loc_[1]

	i = 1

	if direction_ == '<':
		while maze_[loc_row, loc_col - i] == 'O':
			i += 1

		if maze_[loc_row, loc_col - i] == '.':
			maze_[loc_row, loc_col] = '.'
			new_robot_loc = (loc_row, loc_col - 1)
			maze_[loc_row, loc_col - 1] = '@'

			if i > 1:
				maze_[loc_row, loc_col - i] = 'O'

	elif direction_ == '>':
		while maze_[loc_row, loc_col + i] == 'O':
			i += 1

		if maze_[loc_row, loc_col + i] == '.':
			maze_[loc_row, loc_col] = '.'
			new_robot_loc = (loc_row, loc_col + 1)
			maze_[loc_row, loc_col + 1] = '@'

			if i > 1:
				maze_[loc_row, loc_col + i] = 'O'

	elif direction_ == '^':
		while maze_[loc_row - i, loc_col] == 'O':
			i += 1

		if maze_[loc_row - i, loc_col] == '.':
			maze_[loc_row, loc_col] = '.'
			new_robot_loc = (loc_row - 1, loc_col)
			maze_[loc_row - 1, loc_col] = '@'

			if i > 1:
				maze_[loc_row - i, loc_col] = 'O'

	elif direction_ == 'v':
		while maze_[loc_row + i, loc_col] == 'O':
			i += 1

		if maze_[loc_row + i, loc_col] == '.':
			maze_[loc_row, loc_col] = '.'
			new_robot_loc = (loc_row + 1, loc_col)
			maze_[loc_row + 1, loc_col] = '@'

			if i > 1:
				maze_[loc_row + i, loc_col] = 'O'

	return maze_, new_robot_loc


def get_sum_gps(maze_: np.array) -> int:
	box_locations = np.where(maze_ == 'O')
	result = np.sum(box_locations[0] * 100 + box_locations[1])
	return result


# moves, maze, loc = parse_input(TEST_INPUT_2)
# print(moves)
# print(maze)
# print(loc)

with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

moves, maze, loc = parse_input(REAL_INPUT)

while moves:
	direction = moves.popleft()
	maze, loc = move_robot(direction, maze, loc)
	answer = get_sum_gps(maze)

print(maze)
print(answer)
