# hi everybody, i'm doctor nick
opcodes = {
	'ALU'  : 0b000000, # ADD, SUB, AND, OR, SLT, SLL, SRL, JR
	'ADDI' : 0b001000, 
	'ANDI' : 0b001100, 
	'ORI'  : 0b001101,
	'SLTI' : 0b001010,
	'BEQ'  : 0b000100,
	'J'    : 0b000010,
	'JAL'  : 0b000011,
	'LW'   : 0b100011,
	'SW'   : 0b101011,
}

# for the ALU normal ops
functs = {	
	'ADD' : 0b100000,
	'AND' : 0b100100,
	'JR'  : 0b001000, # tricky bugger
	'OR'  : 0b100101,
	'SLL' : 0b000000,
	'SLT' : 0b101010,
	'SRL' : 0b000010,
	'SUB' : 0b100010,
}

# state codes
states = {
	'fetch'  : 0b0000, # set IR and incr PC
	'decode' : 0b0001, # calculate branch target address
	# execute stuffs
	'jump'   : 0b0010,
	'jr'     : 0b0011,
	'jal'    : 0b0100,
	'beq'    : 0b0101,
	'imm'    : 0b0110, # addi, andi, ori, slti
	'norm'   : 0b0111, # add, and, or, slt, sub
	'shift'  : 0b1000, # sll, srl
	'offset' : 0b1001, # prepare for mem ops
	# mem stuffs
	'read'   : 0b1010,
	'write'  : 0b1011,
	# write back
	'aluWB'  : 0b1100, # use d reg as dest
	'immWB'  : 0b1101, # t reg is dest
	'memWB'  : 0b1110,
}

# alu control signals
aluops = {
	'sub' : 0b000,
	'and' : 0b001,
	'add' : 0b010,
	'or'  : 0b011,
	'slt' : 0b100,
	'sll' : 0b101,
	'slr' : 0b110,
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
		or state == states['j']     \
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
	print "get_next_state is exiting through default with parameters: "
	print "state: " + state
	print "opcode: " + opcode
	print "funct: " + funct
	return states['fetch']

	# end next state 


def get_alu_opcode(state, opcode, funct):
	# most of these are cut and dry.
	# only norm and imm state need extra attention

	if state == states['fetch']      \
		or state == states['decode'] \
		or state == states['offset']:
		
		return aluops['add']:

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


	print "get_alu_opcode is exiting through default with parameters: "
	print "state: " + state
	print "opcode: " + opcode
	print "funct: " + funct
	return aluops['sub']

	# end get alu opcodes


def get_reg_dst(state):
	if state == states['memWB']:
		return 0b01

	if state == states['jal']:
		return 0b10

	if state == states['aluWB']:
		return 0b00

	if state == states['immWB']:
		return 0b01

	return 0b00


def get_reg_write(state):
	if state == states['memWB']     \
		or state == states['jal']   \
		or state == states['aluWB'] \
		or state == states['immWB']:

		return 0b1

	else:

		return 0b0


def get_alu_src_a(state):
	if state == states['offset']   \
		or state == states['norm'] \
		or state == states['imm']:

		return 0b1

	else:
		return 0b0


def get_alu_src_b(state):
	if state == states['decode'] \
		or state == states['beq']:

		return 0b11

	if state == states['offset'] \
		or state == states['imm']:

		return 0b10

	if state == states['shift'] \
		or state == states['norm']:

		return 0b00

	if state == states['fetch']:
		return 0b01

	return 0b00


def get_alu_shamt_en(state):
	if state == states['shift']:
		return 0b1
	else:
		return 0b0


def get_mem_write(state):
	if state == states['write']:
		return 0b1
	else:
		return 0b0


def get_mem_read(state):
	if state == states['read'] \
		or state == states['fetch']:
		
		return 0b1
	else:
		return 0b0

def get_reg_mem_source(state):
	pass