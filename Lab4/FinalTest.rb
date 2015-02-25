ori $1, $0, 1  # $1 = 1 
add $2, $1, $1 # $2 = 2 forwarding both alu inputs from same source
sub $3, $1, $2 # $3 = -1 forwarding both alu inputs from different sources
addi $4, $3, 14 # $4 = 10 forwarding only A  value
and $5, $1, $3 # $5 = 0 forwarding B value only
sw $4, 10($5) # Mem[10] = 10. need to forward both $4 and $5
lw $6, 10($5) # $6 = 10. forward $5
and $7, $6, $4 # $7 = 10 stall or forward
beq $7, $1, branch #not taken. forward $7 or stall
slt $8, $6, $7 # $8 = 0. forward $7 and $6
beq $8, $8, branch #taken. forward $8 or stall
addi $28, $0, -1 #shouldn't execute
branch: lw $10, 10($0) # $10 = 10
sw $10, -9($10) # Mem[1] = 10. forward $10 or stall
lw $10, 10($0) # $10 = 10
beq $10, $1, branch # must stall for $10. not taken
jal almostdone
addi $27, $0, -1 #shouldn't execute
almostdone: addi $31, $31, 24 #$31 = address of end
sw $31, 0($0) # Mem[0] = address of end
lw $21, 0($0) # $21 = address of end.  
jr $21 #must stall here
addi $26, $0, -1 #shouldn't execute
end: j end #infiinte loop to mark we are done

#5 stalls max


#createArray(start, n)
#creates an array containg values 1 through n beginning at start
#start is assumed to be in reg1 and n in reg2
createArray: addi $3, $1, 0 #copy of start
	#copy over values
	
	addi $4, $2, 0 #copy of n
	addi $5, $0, 1 #first value to copy
	add $6, $5, $0 #value of 1

	beq $4, $0, doneCreateArray
	startLoop: sw $5, 0($3)
		addi $4, $4, 1
		addi $3, $3, 1
		sub $4, $4, $6
		beq $4, $0, doneCreateArray
		j startLoop
		
doneCreateArray: jr $31
 

