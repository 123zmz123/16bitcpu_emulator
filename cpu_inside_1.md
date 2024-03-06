# you must know
this doc were based on on the commit b929b8585f1eaf0cb0606ea64f723df76eb6ed80
it was inspired by youtube channel 

# overview
as you  can see we implement a very small cpu emulator. there are so many project on github that use rust or c/c++. I choose use python in case guys were lost in so much lanuage level detail.

# how does it work.
- the entry point which were located in emulator.py
- we define the cpu instruction set instr.py
- in cpu execute step by step, in each step, cpu fetch a instruction from memory, based on the instruction , it will start corresponding operation on memory and register .
```
def step(self):
        instr = self.fetch()
        res = self.excute(instr)
        return res

def excute(self,instr):
    if(instr == Instruction.MOV_LIT_REG):
        literal = self.fetch16()
        reg = self.fetch()
        self.setRegister(reg,literal)

    elif(instr == Instruction.MOV_REG_REG):
        registerFrom = self.fetch()
        registerTo = self.fetch()
        value = self.getRegister(registerFrom)
        self.setRegister(registerTo,value)
```

- the cpu has 12 registers, ip contain the current address, acc contain the operation result. r1~r8 were general registers. sp point to the current stack addrress , fp point to the current stack frame start address.
```
 self.registers = {
            ip:0,
            acc:0,
            r1:0,
            r2:0,
            r3:0,
            r4:0,
            r5:0,
            r6:0,
            r7:0,
            r8:0,
            sp:0xffff-1,
            fp:0xffff-1
        }
```

## context switch
context switch were used for call a new function. in cpu , the operation status were the content of each registers ,that means if we need call a new function , we must push the current status to the stack and then set ip to the calling function address. after complete execution, we pop the previous register content back to  register, it will execute from return.

```
|     code+data      | 0x0000
|                    |
|                    |
|                    |
|        ....        |
|                    |
|                    |
|                    |
|       stack        | 0xffff
```
In memory view, code & data were stored from 0x0000 to 0x2fff, stack were start at 0xffff.

To call a new function, the CPU need store the current execution state and setup the ip register  to the new function start address. this kind of operation were performed in stack.

the information that needs to be stored in each context switch is called a stack frame.

```
stack frame

|  stack frame size  |
|         ip         |
|         r8         |
|         r7         |
|         r6         |
|         r5         |
|         r4         |
|         r3         |
|         r2         |
|         r1         |
|     num of args    |
|        arg  1      |
|        arg  2      |
|        .....       |
|        arg  n      |

```