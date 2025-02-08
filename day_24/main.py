from pprint import pprint

TEST_INPUT = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


def parse_input(puzzle_input):
	known_values = {}
	instructions = {}

	knowns, instructs = puzzle_input.split('\n\n')

	for known in knowns.split('\n'):
		wire, value = known.split(': ')
		value = int(value)
		known_values[wire] = value

	for instruction in instructs.split('\n'):
		inputs, output = instruction.split(' -> ')
		instructions[output] = inputs.split()

	return known_values, instructions


def answer(output):
	if known.get(output) is not None:
		return known[output]

	wire_1, operator, wire_2 = instruct[output]

	if operator == 'OR':
		return answer(wire_1) | answer(wire_2)

	elif operator == 'AND':
		return answer(wire_1) & answer(wire_2)

	elif operator == 'XOR':
		return answer(wire_1) ^ answer(wire_2)


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

known, instruct = parse_input(REAL_INPUT)

bits = {}
for instruction in instruct:
	if instruction.startswith('z'):
		bits[instruction] = answer(instruction)
bit_string = ''.join([str(bits[bit]) for bit in sorted(bits)])[::-1]
print(int(bit_string, 2))
