addi $1, $0, 8                #0  $1 = 8
ori  $2, $1, 5                #4  $2 = 13
andi $3, $2, -1               #8  $3 = 13
add  $4, $3, $1               #12 $4 = 8 + 13 = 21
sub  $5, $4, $3               #16 $5 = 21 - 13 = 8
and  $6, $1, $2               #20 $6 = 8
or   $7, $6, $3               #24 $7 = 13
sw   $4, 100($5)              #28 memory[100 + 8] = 21
lw   $8, 100($5)              #32 $8 = memory[100 + 8] = 21
slt  $9, $1, $2               #36 $9 = $1 < $2 = 8 < 13 = 1
slti $10, $1, 5               #40 $10 = $1 < 5 = 8 < 5 = 0
goback: beq $8, $5, finish    #44 not taken first time
sub  $8, $8, $3               #48 $8 = 21 - 13 = 8
jal  goback                   #52 jumps to goback, $31 has address of next instr
addi $11, $0, 1               #56 should not execute
finish: addi $12, $0, 5       #60 $12 = 5
