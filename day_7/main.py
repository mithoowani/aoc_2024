from operator import mul, add

TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def parse_input(puzzle_input: str) -> (tuple, tuple):
	lines = puzzle_input.split('\n')
	answers, components = [], []
	for line in lines:
		answer, component = line.split(':')
		answer, component = int(answer), tuple([int(num) for num in component.split()])
		answers.append(answer)
		components.append(component)
	return tuple(answers), tuple(components)


def concatenate(num_1, num_2):
	# Code for || operator (Part B)
	concatenated = int(str(num_1) + str(num_2))
	return concatenated


def get_result(nums, index=1, result_so_far=None):
	global answer_flag

	if result_so_far is None:
		result_so_far = nums[0]

	# Have to use all the numbers in order for it to be a valid solution;
	# i.e. only evaluate this at the end of a tree
	if result_so_far == solution and index == len(nums):
		answer_flag = True

	elif index < len(nums):
		get_result(nums, index + 1, mul(result_so_far, nums[index]))
		get_result(nums, index + 1, add(result_so_far, nums[index]))

		# Part B
		get_result(nums, index + 1, concatenate(result_so_far, nums[index]))


# Test input
# all_answers, all_components = parse_input(TEST_INPUT)

# Real input
with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()
all_answers, all_components = parse_input(REAL_INPUT)

result = 0

# Part B
for entry in zip(all_answers, all_components):
	answer_flag = False
	solution = entry[0]
	get_result(entry[1])
	if answer_flag:
		result += solution

print('Part B Result:', result)
