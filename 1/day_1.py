import numpy as np

TEST_INPUT = """3   4
4   3
2   5
1   3
3   9
3   3"""

with open('input.txt', 'r') as file:
	INPUT = file.read()


def parse_input(input: str) -> (np.array, np.array):
	input_length = len(input.split('\n'))
	left, right = np.zeros(input_length), np.zeros(input_length)
	input_list = input.split('\n')
	for i, row in enumerate(input_list):
		left[i], right[i] = row.split()[0], row.split()[1]
	return left, right


def sum_of_distances(left_, right_):
	left_.sort()
	right_.sort()
	return np.sum(np.abs(left_ - right_)).astype('int64')


def similarity_score(left_, right_):
	sum_ = 0
	for entry in left_:
		sum_ += entry * np.where(right_ == entry)[0].shape[0]
	return int(sum_)


left, right = parse_input(INPUT)

# PART ONE
total_distance = sum_of_distances(left, right)
print(total_distance)

# PART TWO
similarity = similarity_score(left, right)
print(similarity)
