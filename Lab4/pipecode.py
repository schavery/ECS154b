# from bitarray import bitarray
import sys

# hi everybody, i'm doctor nick
opcodes = {
	'ALU'  : '000000', # ADD, SUB, AND, OR, SLT, SLL, SRL, JR
	'ADDI' : '001000', 
	'ANDI' : '001100', 
	'ORI'  : '001101',
	'SLTI' : '001010',
	'BEQ'  : '000100',
	'J'    : '000010',
	'JAL'  : '000011',
	'LW'   : '100011',
	'SW'   : '101011',
}

# for the ALU normal ops
functs = {	
	'ADD' : '100000',
	'AND' : '100100',
	'JR'  : '001000', # tricky bugger
	'OR'  : '100101',
	'SLL' : '000000',
	'SLT' : '101010',
	'SRL' : '000010',
	'SUB' : '100010',
}

# # state codes
# states = {
# 	'fetch'  : '0000', # set IR and incr PC
# 	'decode' : '0001', # calculate branch target address
# 	# execute stuffs
# 	'jump'   : '0010',
# 	'jr'     : '0011',
# 	'jal'    : '0100',
# 	'beq'    : '0101',
# 	'imm'    : '0110', # addi, andi, ori, slti
# 	'norm'   : '0111', # add, and, or, slt, sub
# 	'shift'  : '1000', # sll, srl
# 	'offset' : '1001', # prepare for mem ops
# 	# mem stuffs
# 	'read'   : '1010',
# 	'write'  : '1011',
# 	# write back
# 	'aluWB'  : '1100', # use d reg as dest
# 	'immWB'  : '1101', # t reg is dest
# 	'memWB'  : '1110',
# }

# alu control signals
aluops = {
	'sub' : '000',
	'and' : '001',
	'add' : '010',
	'or'  : '011',
	'slt' : '100',
	'sll' : '101',
	'slr' : '110',
}


def get_alu_opcode(opcode, funct):
	# most of these are cut and dry.
	# only norm and imm state need extra attention

	if opcode == opcodes['ALU']:
		if funct == functs['SLL']:
			return aluops['sll']

		if funct == functs['SRL']:
			return aluops['slr'] # typo in the prompt; kept it

		if funct == functs['SUB']:
			return aluops['sub']

		if funct == functs['AND']:
			return aluops['and']

		if funct == functs['ADD']:
			return aluops['add']

		if funct == functs['OR']:
			return aluops['or']

		if funct == functs['SLT']:
			return aluops['slt']

	if opcode == opcodes['BEQ']:
		return aluops['sub']

	if opcode == opcodes['ADDI']:
		return aluops['add']

	if opcode == opcodes['ANDI']:
		return aluops['and']

	if opcode == opcodes['ORI']:
		return aluops['or']

	if opcode == opcodes['SLTI']:
		return aluops['slt']

	# default return
	return aluops['sub']

	# end get alu opcodes


def get_reg_dst(opcode):
	if opcode == opcodes['ALU']:
		# r-type; d = s OP t
		return '0'

	if opcode == opcodes['ADDI']     \
		or opcode == opcodes['ANDI'] \
		or opcode == opcodes['ORI']  \
		or opcode == opcodes['SLTI']:
		# i-type t = s OP iiiiii
		return '1'

	return '0'


def get_reg_write(opcode, funct):
	if (opcode == opcodes['ALU'] and funct == functs['JR']) \
		or opcode == opcodes['J']   \
		or opcode == opcodes['BEQ'] \
		or opcode == opcodes['SW']:

		return '0'

	else:

		return '1'

	return '0'


def get_alu_src_b(opcode):
	if opcode == opcodes['ADDI']     \
		or opcode == opcodes['ANDI'] \
		or opcode == opcodes['ORI']  \
		or opcode == opcodes['SLTI']:
		# use the immediate value
		return '1'

	return '0'


def get_alu_shamt_en(opcode, funct):
	if opcode == opcodes['ALU']:
		if funct == functs['SRL'] \
			or funct == functs['SLL']:
			return '1'

	return '0'


def get_mem_write(opcode):
	if opcode == opcodes['SW']:
		return '1'
	else:
		return '0'


def get_mem_read(opcode):
	if opcode == opcodes['LW']:
		return '1'
	else:
		return '0'


def get_reg_mem_source(opcode):
	if opcode == opcodes['JAL']:
		return '10'

	if opcode == opcodes['LW']:
		return '00'

	# default to ALU out
	return '01'


def get_branch_condition(opcode):
	if opcode == opcodes['BEQ']:
		return '1'
	else:
		return '0'


def ex_squanch(opcode, funct):
	return '0'

def mem_squanch(opcode, funct):
	return '0'

def wb_squanch(opcode, funct):
	return '0'


the_file = open('microcodes.hex', 'w')
the_file.write('v2.0 raw\n')

for x in xrange(0,4095):
	xstr = "{:012b}".format(x)
	opcode = xstr[0:6] # was 5
	funct = xstr[6:]

	# EX Stage
	databutts = get_alu_opcode(opcode, funct)
	databutts += get_alu_src_b(opcode)
	databutts += get_alu_shamt_en(opcode, funct)
	databutts += get_reg_dst(opcode)

	# Memers
	databutts += get_branch_condition(opcode)
	databutts += get_mem_write(opcode)
	databutts += get_mem_read(opcode)

	# WB
	databutts += get_reg_write(opcode, funct)
	databutts += get_reg_mem_source(opcode)


	# squanchs
	databutts += ex_squanch(opcode, funct)
	databutts += mem_squanch(opcode, funct)
	databutts += wb_squanch(opcode, funct)

	# print '{:x}'.format(int(databutts, 2))
	the_file.write('{:04x}'.format(int(databutts, 2)) + '\n')
	
