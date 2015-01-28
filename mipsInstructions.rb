addi $1, $0, 8                #$1 = 8
ori  $2, $1, 5                #$2 = 13
andi $3, $2, -1               #$3 = 13
add  $4, $3, $1               #$4 = 8 + 13 = 21
sub  $5, $4, $3               #$5 = 21 - 13 = 8
and  $6, $1, $2               #$6 = 8
or   $7, $6, $3               #$7 = 13
sw   $4, 100($5)              #memory[100 + 8] = 21
lw   $8, 100($5)              #$8 = memory[100 + 8] = 21
slt  $9, $1, $2               #$9 = $1 < $2 = 8 < 13 = 1
slti $10, $1, 5               #$10 = $1 < 5 = 8 < 5 = 0
goback: beq $8, $5, finish    #not taken first time
sub  $8, $8, $3               #$8 = 21 - 13 = 8
jal  goback                   #jumps to goback, $31 has address of next instr
addi $11, $0, 1               #should not execute
finish: addi $12, $0, 5       #$12 = 5