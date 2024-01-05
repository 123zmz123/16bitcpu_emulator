
from collections import namedtuple
from memory import Memory
Region = namedtuple("Region","device start end remap")
class MemoryMapper():
    def __init__(self):
        self.regions:list[Region] = []
    
    def map(self,device,start,end,remap=False):
        self.regions.append(Region(device,start,end,remap))

    def get_region(self,address):
        for region in self.regions:
            if (region.start <= address and region.end >= address):
                return region
        return None

    def getUint8(self, address):
        region = self.get_region(address)
        if region.remap == True:
            finalAddress = address - region.start
        else:
            finalAddress = address
        return region.device.getUint8(finalAddress)

    def getUint16(self,address):
        region = self.get_region(address)
        if region.remap == True:
            finalAddress = address - region.start
        else:
            finalAddress = address
        return region.device.getUint16(finalAddress)
    
    def setUint16(self,address,value):
        region = self.get_region(address)
        if region.remap == True:
            finalAddress = address - region.start
        else:
            finalAddress = address
        region.device.setUint16(finalAddress,value)
    
    def setUint8(self,address,value):
        region = self.get_region(address)
        if region.remap == True:
            finalAddress = address - region.start
        else:
            finalAddress = address
        region.device.setUint8(finalAddress,value)



if __name__ == "__main__":
    mram = Memory(0xffff)
    mem_unit = MemoryMapper()
    mem_unit.map(mram,0x0000,0xffff)
    mem_unit.setUint8(0x0000,0x77)
    mem_unit.setUint16(0x0001,0xAABB)
    pass