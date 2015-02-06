addi $1, $0, 5              # $1 = 5
ori  $2, $1, 3              # $2 = 7
andi $3, $2, -1             # $3 = 7
add  $4, $3, $1             # $4 = 5 + 7 = 12
sub  $5, $2, $3             # $5 = 7 - 7 = 0
and  $6, $1, $4             # $6 = 12 & 5 = 4 
sw   $4, 100($5)            # memory[100] = 12
lw   $7, 100($0)            # $7 = memory[100] = 12
slt  $8, $1, $2             # $8 = $1 < $2 = 5 < 7 = 1
sll  $9, $6, 10							# $9 = 4096
srl  $11,$9, 5 							# $11= 128
goback: beq  $8, $0, go     # branch not taken the first time but taken the second
slt  $8, $2, $1             # $9 = $2 < $1 = 7 < 5 = 0
slti  $10, $1, 9            # $10 = $1 < 9 = 5 < 9 = 1
beq  $8, $0, goback         # go back to line 10
go: jal almostdone          # jump to line 18. store location of instruction 15 in $31 
done: j done                # infinite loop to mark that we are done
almostdone: addi $1, $1, 1  # $1 = 6
add $1, $1, $1              # $1 = 6 + 6 = 12
jr $31                      # go to line 17
addi $1, $0, 100            # should not execute
bad: j bad                  # should not execute

