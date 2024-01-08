import sys
class Screen():
    def __init__(self):
        pass
    
    def eraseScreen(self):
        print('\x1b[2J')
    
    def setBold(self):
        print('\x1b[1m')

    def setRegular(self):
        print('\x1b[0m')

    def getUint16(self,address):
        return 0

    def getUint8(self,address):
        return 0
    
    def setUint16(self,address,value):
        command = (value & 0xff00)>>8
        charValue = value & 0xff
        y = address %16 + 1
        x = address // 16 + 2
        # print(x)
        # print(y)
        if (command ==  0xff):
            self.eraseScreen()
        elif(command == 0x01):
            self.setBold()
        elif(command == 0x02):
            self.setRegular()

        sys.stdout.write("\033[{0};{1}H{2}".format(x,y,chr(charValue)))
        










if __name__ == "__main__":
    # print('\x1b[1m') # bold
    # print('\x1b[0m') # retangle
    s=Screen()
    s.setUint16(16,0x0100 | (ord('+') & 0xff))
    s.setUint16(17,0x0100 | (ord('+') & 0xff))
    s.setUint16(18,0x0100 | (ord('+') & 0xff))
    # s.setUint16(17,0x0100 | (ord('@') & 0xff))
    # s.setUint16(0x81,0x0124)
    # s.setUint16(0x82,0x0124)
    # s.setUint16(0x83,0x0124)
    pass