import array
class Memory():
    def __init__(self,sizeInbytes) -> None:
        self.raw_mem = array.array('B',[0]*sizeInbytes)
    
    def getUint8(self,address):
        return self.raw_mem[address]
        pass

    def getUint16(self,address):
        uint16_res = self.raw_mem[address]<<8 | self.raw_mem[address+1]
        return uint16_res
    
if __name__ == '__main__':
    mem = Memory(16)
    mem.raw_mem[0]=0x01
    mem.raw_mem[1]=0x02
    mem.raw_mem[2]=0x14
    print(mem.getUint8(0))
    print(hex(mem.getUint16(1)))