from ALU_Phase3 import *
#reg=[[0 for x in range(0,32)] for x in range(0,32)]
#MEM=[0 for x in range(0,10000)]

# comment reg,MEM when mergred


def write_to_memory(start, len, reg_id):        #byte addressable
    start *= 8
    len *= 8
    # print("start: {}".format(start))
    for i in range(len):
        MEM[i+start] = reg[reg_id][31-i]
    len = int(len/8)
    for i in range(len) :
        for j in range(4) :
            MEM[start + 8*i + j], MEM[start + 8*(i+1) - 1  - j] = MEM[start + 8*(i+1) - 1  - j], MEM[start + 8*i + j]


def write_from_memory(start, len, reg_id):      #byte addressable
    start *= 8
    len *= 8
    if reg_id==-1:
    for i in range(32):
        reg[reg_id][i] = 0
    print("start: {}".format(start))
    for i in range(len):
        reg[reg_id][32-len+i] = MEM[start+len-1-i]
    print(MEM[start:start + len])
    len = int(len/8)
    for i in range(len) :
        for j in range(4) :
            reg[reg_id][8*(3-i) + j], reg[reg_id][8*(4-i) - 1  - j] = reg[reg_id][8*(4-i) - 1  - j], reg[reg_id][8*(3-i) + j]
            
def RW(machine_code, aluVals,ins_type,mem_read,mem_write,mem_qty,PC):
    # print("PC: {}".format(PC))
    aluVal=[]
    print("alu: {}".format(aluVals))
    for _ in aluVals:
        aluVal.append(int(_))
    #print(aluVals)
    #print(ins_type)

    def binary(arr):
        sum=0
        for i in range(len(arr)):
            sum+=int(arr[i])*(2**(len(arr)-1-i))
        return sum       

    SIZE = 1<<32
    SIZE -= 1
    i=0
    # for _ in reg:
    #     print(i,end=" ")
    #     print(binary(_))
    #     i+=1
    def add(m):
        n = 0
        carr = 1
        pow = 1
        while m>0:
            sum = m%2 + carr
            carr = 0
            if sum==2:
                sum = 0
                carr = 1
            n += sum*pow
            pow *= 2
            m = int(m/2)
        n %= (SIZE+1)
        return n

    def _2C(n):
        m = SIZE
        m = m^n 
        return add(m)

    def toBinary(n):
        val = ""
        if n<0:
            n = _2C(-n)
        while n>0 or len(val)<32:
            if n%2:
                val += "1"
            else:
                val += "0"
            k = int(n/2)
            n = int(k)
        string = "".join(reversed(val))
        return string
    
    add_op=[0,1,1,0,0,1,1]
    addi_op=[0,0,1,0,0,1,1]
    add_funct7=[0,0,0,0,0,0,0]
    sub_funct7=[0,1,0,0,0,0,0]
    mul_funct7=[0,0,0,0,0,0,1]
    add_funct3=[0,0,0]
    and_funct3=[1,1,1]
    or_funct3=[1,1,0]
    sll_funct3=[0,0,1]
    slt_funct3=[0,1,0]
    sra_funct3=[1,0,1]
    xor_funct3=[1,0,0]
    andi_funct3=[1,1,1]        

    # I-format
    
    lb_op = [0,0,0,0,0,1,1]
    lb_funct3 = [0,0,0]

    ld_op = [0,0,0,0,0,1,1]
    ld_funct3 = [0,1,1]
    
    lh_op = [0,0,0,0,0,1,1]
    lh_funct3 = [0,0,1]
    
    lw_op = [0,0,0,0,0,1,1]
    lw_funct3 = [0,1,0]
    
    jalr_op = [1,1,0,0,1,1,1]
    jalr_funct3 = [0,0,0]

    # S-format
    sb_op = [0,1,0,0,0,1,1]
    sb_funct3 = [0,0,0]
    
    sw_op = [0,1,0,0,0,1,1]
    sw_funct3 = [0,1,0]
    
    sh_op = [0,1,0,0,0,1,1]
    sh_funct3 = [0,0,1]
    
    sd_op = [0,1,0,0,0,1,1]     # I or S ? ? ? ? ?
    sd_funct3 = [0,1,1]
    
    # SB-format
    beq_op = [1,1,0,0,0,1,1]
    beq_funct3 = [0,0,0]
    
    bne_op = [1,1,0,0,0,1,1]
    bne_funct3 = [0,0,1]
    
    bge_op = [1,1,0,0,0,1,1]
    bge_funct3 = [1,0,1]
    
    blt_op = [1,1,0,0,0,1,1]
    blt_funct3 = [1,0,0]

    # U-format
    auipc_op = [0,0,1,0,1,1,1]

    lui_op = [0,1,1,0,1,1,1]

    # UJ-format
    jal_op = [1,1,0,1,1,1,1]

    reg_id = binary(machine_code[20:25])
    # print('alu val ',end=" ") 
    # print(aluVal)

    start = binary(aluVal)
    # print("aluval: {}".format(aluVal))
    # print("start1: {}".format(start))
    #print("aluval for writeformfmwda", aluVal)
    if(machine_code[25:32]==ld_op and machine_code[17:20]==ld_funct3):
        # NOT SUPPORTED
        print("Error, 64 bit operation")
        return -1
    if(ins_type=="I" and mem_read==1):
    #if(machine_code[25:32]==lb_op and machine_code[17:20]==lb_funct3):
        print("start: {}".format(start))
        write_from_memory(start,mem_qty,reg_id)
        return reg_id
    #if(ins_type=="I" and mem_read==2):    
    #if(machine_code[25:32]==lh_op and machine_code[17:20]==lh_funct3):
        #write_from_memory(start,16,reg_id)
    #if(ins_type=="I" and mem_read==3):    
    #if(machine_code[25:32]==lw_op and machine_code[17:20]==lw_funct3):
        #write_from_memory(start,32,reg_id)
    if(machine_code[25:32]==jalr_op and machine_code[17:20]==jalr_funct3):
        i=29
        carry = 1
        while i>=0:
            aluVal[i] = (aluVal[i]+carry)
            carry = aluVal[i]/2
            aluVal[i] = aluVal[i]%2
            i = i-1
        reg[reg_id] = aluVal
        #print("id")
        #print(reg[reg_id])
        return reg_id
    if(ins_type=="S" and mem_write==1):
    #if(machine_code[25:32]==sb_op and machine_code[17:20]==sb_funct3):
        write_to_memory(start,mem_qty,binary(machine_code[7:12]))
        return reg_id
    #if(ins_type=="S" and mem_write==3):    
    #if(machine_code[25:32]==sw_op and machine_code[17:20]==sw_funct3):
        #write_to_memory(start,32,reg_id)
    if(machine_code[25:32]==sd_op and machine_code[17:20]==sd_funct3):
        # NOT SUPPORTED
        print("Error, 64 bit operation")
        return -1
    #if(ins_type=="S" and mem_write==2):    
    #if(machine_code[25:32]==sh_op and machine_code[17:20]==sh_funct3):
        #write_to_memory(start,16,reg_id)
        

    if(ins_type=="R" or (ins_type=="I" and mem_read==0 and mem_write==0)):
        reg[binary(machine_code[20:25])]=aluVal
        return reg_id
    # if(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==add_funct7):      #add
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==sub_funct7):    #sub
    #     reg[binary(machine_code[20:25])]=aluVal                        
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==and_funct3 and machine_code[0:7]==add_funct7):    #and
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==or_funct3 and machine_code[0:7]==add_funct7):     #or
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==sll_funct3 and machine_code[0:7]==add_funct7):    #sll
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==slt_funct3 and machine_code[0:7]==add_funct7):    #slt
    #     reg[binary(machine_code[20:25])]=aluVal        
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==sra_funct3 and machine_code[0:7]==sub_funct7):    #sra
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==sra_funct3 and machine_code[0:7]==add_funct7):    #srl
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==xor_funct3 and machine_code[0:7]==add_funct7):    #xor
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==mul_funct7):    #mul
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==xor_funct3 and machine_code[0:7]==mul_funct7):    #div
    #     reg[binary(machine_code[20:25])]=aluVal  
    # elif(machine_code[25:32]==addi_op and machine_code[17:20]==add_funct3):                                     #addi
    #     reg[binary(machine_code[20:25])]=aluVal      
    # elif(machine_code[25:32]==addi_op and machine_code[17:20]==andi_funct3):                                    #andi
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==addi_op and machine_code[17:20]==or_funct3):                                      #ori
    #     reg[binary(machine_code[20:25])]=aluVal
    # elif(machine_code[25:32]==add_op and machine_code[17:20]==or_funct3 and machine_code[0:7]==mul_funct7):     #rem
    #     reg[binary(machine_code[20:25])]=aluVal    
    elif(machine_code[25:32]==lui_op):                                                                          #lui            
        for i in range(20):
            reg[binary(machine_code[20:25])][i]=machine_code[i]
        for i in range(20,32):
            reg[binary(machine_code[20:32])][i]=0    
        return reg_id    
    
    if(machine_code[25:32]==jal_op):
        # PC = []*32                      #                    # comment when merged
        #print("jjjjjjjjjj")
        #print(PC)
        x=toBinary(PC*4)
        y=[]
        for _ in x:
            y.append(int(_))
        reg[binary(machine_code[20:25])] = y 
        #print(y)                                   # Global PC
        #print('this is jal in RW')
        return reg_id
    if(machine_code[25:32]==auipc_op):
        imm = binary(machine_code[0:20])
        imm = imm<<12
        x=toBinary(imm+PC*4)
        y=[]
        for _ in x:
            y.append(int(_))
        reg[binary(machine_code[20:25])] = y
        return reg_id
    return 0
