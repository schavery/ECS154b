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
	'JR'  : 0b001000,
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
}

def get_next_state(state, opcode, funct):
	# for each state, there is a next state
	# depends on the value of state,
	# and potentially opcode / funct

	# fetch always goes to decode
	if state == states['fetch']:
		return states['decode']

	# several states return to fetch unconditionally
	if (state == states['jump'])      \
		or (state == states['j'])     \
		or (state == states['beq'])   \
		or (state == states['jal'])   \
		or (state == states['write']) \
		or (state == states['aluWB']) \
		or (state == states['immWB']):

		return states['fetch']

	# choose mem op based on opcode
	if state == states['offset']:
		if opcode == opcodes['LW']:
			return states['read']
		
		if opcode == opcodes['SW']:
			return states['write']

	# select write back state
	if state == states['']



