import re

TEST_INPUT = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
with open('input.txt', 'r') as f:
	INPUT = f.read()


def find_sum(matches_):
	sum = 0
	for match in matches_:
		digits = [int(digit) for digit in match[4:-1].split(',')]
		sum += digits[0] * digits[1]
	return sum


# PART A
regex_string = """mul\(\d{1,3},\d{1,3}\)"""
matches = re.findall(regex_string, INPUT)
sum = find_sum(matches)
print(sum)

# PART B
regex_string = """mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"""
matches = re.findall(regex_string, INPUT)
trimmed_matches = []
flag = True
for match in matches:
	if match == 'do()':
		flag = True
		continue
	elif match == "don't()":
		flag = False
		continue
	elif flag:
		trimmed_matches.append(match)
	else:
		continue

sum = find_sum(trimmed_matches)
print(sum)
