from bitarray import bitarray
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

# state codes
states = {
	'fetch'  : '0000', # set IR and incr PC
	'decode' : '0001', # calculate branch target address
	# execute stuffs
	'jump'   : '0010',
	'jr'     : '0011',
	'jal'    : '0100',
	'beq'    : '0101',
	'imm'    : '0110', # addi, andi, ori, slti
	'norm'   : '0111', # add, and, or, slt, sub
	'shift'  : '1000', # sll, srl
	'offset' : '1001', # prepare for mem ops
	# mem stuffs
	'read'   : '1010',
	'write'  : '1011',
	# write back
	'aluWB'  : '1100', # use d reg as dest
	'immWB'  : '1101', # t reg is dest
	'memWB'  : '1110',
}

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

def get_next_state(state, opcode, funct):
	# for each state, there is a next state
	# depends on the value of state,
	# and potentially opcode and/or funct

	# fetch always goes to decode
	if state == states['fetch']:
		return states['decode']

	# several states return to fetch unconditionally
	if state == states['jump']      \
		or state == states['beq']   \
		or state == states['jal']   \
		or state == states['write'] \
		or state == states['aluWB'] \
		or state == states['immWB'] \
		or state == states['memWB']:

		return states['fetch']

	# choose mem op based on opcode
	if state == states['offset']:
		if opcode == opcodes['LW']:
			return states['read']
		
		if opcode == opcodes['SW']:
			return states['write']

	# select write back state
	if state == states['imm']:
		return states['immWB']

	if state == states['norm']     \
		or state == states['shift']:

		return states['aluWB']

	if state == states['read']:
		return states['memWB']


	# select execute state
	if state == states['decode']:
		if opcode == opcodes['ALU']:

			if funct == functs['SRL'] \
				or funct == functs['SLL']:
				
				return states['shift']

			elif funct == functs['JR']:

				return states['jr']

			else:

				return states['norm']


		# immediate
		if opcode == opcodes['ADDI']     \
			or opcode == opcodes['ANDI'] \
			or opcode == opcodes['ORI']  \
			or opcode == opcodes['SLTI']:

			return states['imm']

		# mem
		if opcode == opcodes['LW'] \
			or opcode == opcodes['SW']:

			return states['offset']


		# jump types, except for JR which goes with ALU ops
		if opcode == opcodes['JAL']:
			return states['jal']

		if opcode == opcodes['J']:
			return states['jump']

		if opcode == opcodes['BEQ']:
			return states['beq']

	# default to fetch?
	# print "get_next_state is exiting through default with parameters: "
	# print "state: " + state
	# print "opcode: " + opcode
	# print "funct: " + funct
	return states['fetch']

	# end next state 


def get_alu_opcode(state, opcode, funct):
	# most of these are cut and dry.
	# only norm and imm state need extra attention

	if state == states['fetch']      \
		or state == states['decode'] \
		or state == states['offset']:
		
		return aluops['add']

	if state == states['beq']:
		return aluops['sub']

	if state == states['shift']:
		if funct == functs['SLL']:
			return aluops['sll']

		if funct == functs['SRL']:
			return aluops['slr'] # typo in the prompt; kept it


	if state == states['norm']:
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

		if funct == functs['SLL']:
			return aluops['sll']

		if funct == functs['SRL']:
			return aluops['slr']


	if state == states['imm']:
		if opcode == opcodes['ADDI']:
			return aluops['add']

		if opcode == opcodes['ANDI']:
			return aluops['and']

		if opcode == opcodes['ORI']:
			return aluops['or']

		if opcode == opcodes['SLTI']:
			return aluops['slt']


	# print "get_alu_opcode is exiting through default with parameters: "
	# print "state: " + state
	# print "opcode: " + opcode
	# print "funct: " + funct
	return aluops['sub']

	# end get alu opcodes


def get_reg_dst(state):
	if state == states['memWB']:
		return '01'

	if state == states['jal']:
		return '10'

	if state == states['aluWB']:
		return '00'

	if state == states['immWB']:
		return '01'

	return '00'


def get_reg_write(state):
	if state == states['memWB']     \
		or state == states['jal']   \
		or state == states['aluWB'] \
		or state == states['immWB']:

		return '1'

	else:

		return '0'


def get_alu_src_a(state):
	if state == states['offset']   \
		or state == states['norm'] \
		or state == states['imm']:

		return '1'

	else:
		return '0'


def get_alu_src_b(state):
	if state == states['decode'] \
		or state == states['beq']:

		return '11'

	if state == states['offset'] \
		or state == states['imm']:

		return '10'

	if state == states['shift'] \
		or state == states['norm']:

		return '00'

	if state == states['fetch']:
		return '01'

	return '00'


def get_alu_shamt_en(state):
	if state == states['shift']:
		return '1'
	else:
		return '0'


def get_mem_write(state):
	if state == states['write']:
		return '1'
	else:
		return '0'


def get_mem_read(state):
	if state == states['read'] \
		or state == states['fetch']:
		
		return '1'
	else:
		return '0'


def get_reg_mem_source(state):
	if state == states['aluWB'] \
		or state == states['immWB']:

		return '00'

	if state == states['memWB']:
		return '01'

	if state == states['jal']:
		return '10'

	return '00'


def get_ir_write_en(state):
	if state == states['fetch']:
		return '1'
	else:
		return '0'


def get_iord(state):
	if state == states['read'] \
		or state == states['write']:

		return '1'
	else:
		return '0'


def get_pc_write(state):
	if state == states['fetch']    \
		or state == states['jump'] \
		or state == states['jr']   \
		or state == states['jal']:

		return '1'

	else:
		return '0'


def get_pc_conditional_write(state):
	if state == states['beq']:
		return '1'
	else:
		return '0'


def get_pc_source(state):
	if state == states['fetch'] \
		or state == states['beq']:

		return '00'

	if state == states['jump'] \
		or state == states['jal']:

		return '10'

	if state == states['jr']:
		return '11'

	return '00'

the_file = open('microcodes.hex', 'w')
the_file.write('v2.0 raw\n')

for x in xrange(0,65535):
	xstr = "{:016b}".format(x)
	opcode = xstr[0:6] # was 5
	funct = xstr[6:12]
	state = xstr[12:]

	databutts = get_next_state(state, opcode, funct)
	databutts += get_alu_opcode(state, opcode, funct)
	databutts += get_reg_dst(state)
	databutts += get_reg_write(state)
	databutts += get_alu_src_a(state)
	databutts += get_alu_src_b(state)
	databutts += get_alu_shamt_en(state)
	databutts += get_mem_write(state)
	databutts += get_mem_read(state)
	databutts += get_reg_mem_source(state)
	databutts += get_ir_write_en(state)
	databutts += get_iord(state)
	databutts += get_pc_write(state)
	databutts += get_pc_conditional_write(state)
	databutts += get_pc_source(state)

	# print '{:x}'.format(int(databutts, 2))
	the_file.write('{:06x}'.format(int(databutts, 2)) + '\n')
	# sys.exit(0)



	# binarydata += 
