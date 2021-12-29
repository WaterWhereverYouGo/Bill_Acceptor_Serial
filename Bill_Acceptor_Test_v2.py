import serial
import keyboard
import subprocess

from serial.serialutil import to_bytes

def clear_console():
    subprocess.call('clear')

class BA_Msg_Type:
    def __init__(self, Ack_Num, Msg_Type):
        self.Ack_Num = Ack_Num                          #bit 0 - bit 3
        self.Msg_Type = Msg_Type                        #bit 4 - bit 6
          
    def __str__(self):
        return str(self.giveInt())

    def giveBytes_formatted(self):
        return str('%02x' % int(self.giveInt())).encode("UTF-8")

    def giveBytes(self):
        return (chr(self.giveInt()).encode('UTF-8'))

    def giveInt(self):
        together = (self.Msg_Type * 16) + (self.Ack_Num * 1)
        
        return int(together)


class BA_Status_Byte_0:
    def __init__(self, Idle, Accepting, Escrowed, Stacking, Stacked, Returning, Returned):
        self.Idle = Idle                                  #bit 0 
        self.Accepting = Accepting                        #bit 1 
        self.Escrowed = Escrowed                          #bit 2
        self.Stacking = Stacking                          #bit 3 
        self.Stacked = Stacked                            #bit 4 
        self.Returning = Returning                        #bit 5
        self.Returned = Returned                          #bit 6 
        
    def __str__(self):
        return str(self.giveInt())

    def giveBytes_formatted(self):
        return str('%02x' % int(self.giveInt())).encode("UTF-8")

    def giveBytes(self):
        return (chr(self.giveInt()).encode('UTF-8'))

    def giveInt(self):
        together = ( self.Returned * 64 ) + ( self.Returning * 32 ) + ( self.Stacked   *  16 ) +\
                   ( self.Stacking *  8 ) + ( self.Escrowed  *  4 ) + ( self.Accepting *   2 ) +\
                   ( self.Idle     *  1 ) 
        
        return int(together)

class BA_Status_Byte_1:
    def __init__(self, Cheated, Rejected, Jammed, Stacker_Full, LRC_Status, Reserved, Calibration):
        self.Cheated = Cheated                            #bit 0 
        self.Rejected = Rejected                          #bit 1 
        self.Jammed = Jammed                              #bit 2
        self.Stacker_Full = Stacker_Full                  #bit 3 
        self.LRC_Status = LRC_Status                      #bit 4 
        self.Reserved = Reserved                          #bit 5
        self.Calibration = Calibration                    #bit 6 
 
    def __str__(self):
        return str(self.giveInt())

    def giveBytes_formatted(self):
        return str('%02x' % int(self.giveInt())).encode("UTF-8")

    def giveBytes(self):
        return (chr(self.giveInt()).encode('UTF-8'))

    def giveInt(self):
        together = ( self.Calibration  * 64 ) + ( self.Reserved * 32 ) + ( self.LRC_Status *  16 ) +\
                   ( self.Stacker_Full *  8 ) + ( self.Jammed   *  4 ) + ( self.Rejected   *   2 ) +\
                   ( self.Cheated      *  1 ) 
        
        return int(together)


class BA_Status_Byte_2:
    def __init__(self, Power_Up, Invalid_Cmd, Failure, Bill_Value, Reserved):
        self.Power_Up = Power_Up                          #bit 0 
        self.Invalid_Cmd = Invalid_Cmd                    #bit 1 
        self.Failure = Failure                            #bit 2
        self.Bill_Value = Bill_Value                      #bit 3 - bit 5
        self.Reserved = Reserved                          #bit 6
 
    def __str__(self):
        return str(self.giveInt())

    def giveBytes_formatted(self):
        return str('%02x' % int(self.giveInt())).encode("UTF-8")

    def giveBytes(self):
        return (chr(self.giveInt()).encode('UTF-8'))

    def giveInt(self):
        together = ( self.Reserved    * 64 ) + ( self.Bill_Value * 8 ) + ( self.Failure * 4 ) +\
                   ( self.Invalid_Cmd *  2 ) + ( self.Power_Up   * 1 ) 
        
        return int(together)
        

class BA_Status_Byte_3:
    def __init__(self, No_Push_Mode, Flash_Download, Reserved):
        self.No_Push_Mode = No_Push_Mode                  #bit 0 
        self.Flash_Download = Flash_Download              #bit 1 
        self.Reserved = Reserved                          #bit 2 - bit 6
 
    def __str__(self):
        return str(self.giveInt())

    def giveBytes_formatted(self):
        return str('%02x' % int(self.giveInt())).encode("UTF-8")

    def giveBytes(self):
        return (chr(self.giveInt()).encode('UTF-8'))

    def giveInt(self):
        together = ( self.Reserved     * 4 )  + ( self.Flash_Download *   2 ) + ( self.No_Push_Mode * 1 ) 
        
        return int(together)
        #return str(self.Parity) + str(self.Reserved) + str(self.Flash_Download) + str(self.No_Push_Mode)


class BillAcceptorStruct:
    def __init__(self, BA_STX, Length, Msg_Type_Char, Stat_Byte_0, Stat_Byte_1, Stat_Byte_2, Stat_Byte_3, Model, Revision, BA_ETX, Check_Sum):
        self.BA_STX = BA_STX
        self.Length = Length
        self.Msg_Type_Char = Msg_Type_Char
        self.Stat_Byte_0 = Stat_Byte_0
        self.Stat_Byte_1 = Stat_Byte_1
        self.Stat_Byte_2 = Stat_Byte_2
        self.Stat_Byte_3 = Stat_Byte_3
        self.Model = Model
        self.Revision = Revision
        self.BA_ETX = BA_ETX
        self.Check_Sum = Check_Sum
 
    def __str__(self):      # it's hex!
        return ( ("%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x" % (self.BA_STX, self.Length, int(str(self.Msg_Type_Char)), int(str(self.Stat_Byte_0)),\
                 int(str(self.Stat_Byte_1)), int(str(self.Stat_Byte_2)), int(str(self.Stat_Byte_3)), self.Model,\
                 self.Revision, self.BA_ETX, self.Check_Sum) ) )

    def print(self):
        print ( ("0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x" % (self.BA_STX, self.Length, int(str(self.Msg_Type_Char)), int(str(self.Stat_Byte_0)),\
                 int(str(self.Stat_Byte_1)), int(str(self.Stat_Byte_2)), int(str(self.Stat_Byte_3)), self.Model,\
                 self.Revision, self.BA_ETX, self.Check_Sum) ) )

    def giveAscii(self):
        return ((chr(self.BA_STX).encode("UTF-8")) + (chr(self.Length).encode("UTF-8")) + self.Msg_Type_Char.giveBytes() + self.Stat_Byte_0.giveBytes() +\
                self.Stat_Byte_1.giveBytes() + self.Stat_Byte_2.giveBytes() + self.Stat_Byte_3.giveBytes() + \
                (chr(self.Model).encode("UTF-8")) + (chr(self.Revision).encode("UTF-8")) + (chr(self.BA_ETX).encode("UTF-8")) + (chr(self.Check_Sum).encode("UTF-8")))





if __name__ == "__main__":

    keyboard.add_hotkey('c', clear_console)

    serial1 = serial.Serial()
    serial1.baudrate = 9600
    serial1.port = 'COM2'
    serial1.parity = serial.PARITY_EVEN
    serial1.bytesize = 7
    serial1.timeout = 2
    serial1.open()
    serial1Output = b''

    prompt = 1
    forever = 1
    STX = 2
    ETX = 3

    if(serial1.isOpen()):
        print("comms good\n")

        ## format message , null message
        BillAcceptor = BillAcceptorStruct(0,0,BA_Msg_Type(0,0),\
                        BA_Status_Byte_0(0,0,0,0,0,0,0),\
                        BA_Status_Byte_1(0,0,0,0,0,0,0),\
                        BA_Status_Byte_2(0,0,0,0,0),\
                        BA_Status_Byte_3(0,0,0),\
                        0,0,0,0)

        ## fill the message
        BillAcceptor.BA_STX = STX
        BillAcceptor.Length = 9

        BillAcceptor.Msg_Type_Char.Ack_Num      = 1
        BillAcceptor.Msg_Type_Char.Msg_Type     = 1  

        BillAcceptor.Stat_Byte_0.Idle           = 0
        BillAcceptor.Stat_Byte_0.Accepting      = 0
        BillAcceptor.Stat_Byte_0.Escrowed       = 1
        BillAcceptor.Stat_Byte_0.Stacking       = 0
        BillAcceptor.Stat_Byte_0.Stacked        = 0
        BillAcceptor.Stat_Byte_0.Returning      = 0
        BillAcceptor.Stat_Byte_0.Returned       = 0   

        BillAcceptor.Stat_Byte_1.Cheated        = 0
        BillAcceptor.Stat_Byte_1.Rejected       = 0
        BillAcceptor.Stat_Byte_1.Jammed         = 0
        BillAcceptor.Stat_Byte_1.Stacker_Full   = 0
        BillAcceptor.Stat_Byte_1.LRC_Status     = 0
        BillAcceptor.Stat_Byte_1.Reserved       = 1
        BillAcceptor.Stat_Byte_1.Calibration    = 0

        BillAcceptor.Stat_Byte_2.Power_Up       = 0
        BillAcceptor.Stat_Byte_2.Invalid_Cmd    = 0
        BillAcceptor.Stat_Byte_2.Failure        = 0
        BillAcceptor.Stat_Byte_2.Bill_Value     = 1
        BillAcceptor.Stat_Byte_2.Reserved       = 1

        BillAcceptor.Stat_Byte_3.No_Push_Mode   = 0
        BillAcceptor.Stat_Byte_3.Flash_Download = 0
        BillAcceptor.Stat_Byte_3.Reserved       = 1

        BillAcceptor.Model     = 24
        BillAcceptor.Revision  = 6
        BillAcceptor.BA_ETX    = ETX
        BillAcceptor.Check_Sum = 0

        # deposit 1 dollar

        display_string = BillAcceptor.giveAscii()
        print(display_string)
        serial1.write(display_string)
        message_received = serial1.read_until(expected='\x03',size=10)
        print(message_received)
        input("Press Enter to continue...")

        BillAcceptor.Stat_Byte_0.Escrowed       = 0
        BillAcceptor.Stat_Byte_0.Stacked        = 1
        BillAcceptor.Stat_Byte_2.Bill_Value     = 1
        display_string = BillAcceptor.giveAscii()
        print(display_string)
        serial1.write(display_string)
        message_received = serial1.read_until(expected='\x03',size=10)
        print(message_received)
        input("Press Enter to continue...")

        # deposit 2 dollars

        BillAcceptor.Stat_Byte_0.Escrowed       = 1
        BillAcceptor.Stat_Byte_0.Stacked        = 0
        BillAcceptor.Stat_Byte_2.Bill_Value     = 2
        display_string = BillAcceptor.giveAscii()
        print(display_string)
        serial1.write(display_string)
        message_received = serial1.read_until(expected='\x03',size=10)
        print(message_received)
        input("Press Enter to continue...")

        BillAcceptor.Stat_Byte_0.Escrowed       = 0
        BillAcceptor.Stat_Byte_0.Stacked        = 1
        BillAcceptor.Stat_Byte_2.Bill_Value     = 2
        display_string = BillAcceptor.giveAscii()
        print(display_string)
        serial1.write(display_string)
        message_received = serial1.read_until(expected='\x03',size=10)
        print(message_received)
        input("Press Enter to continue...")

        # deposit 2 dollars

        BillAcceptor.Stat_Byte_0.Escrowed       = 1
        BillAcceptor.Stat_Byte_0.Stacked        = 0
        BillAcceptor.Stat_Byte_2.Bill_Value     = 2
        display_string = BillAcceptor.giveAscii()
        print(display_string)
        serial1.write(display_string)
        message_received = serial1.read_until(expected='\x03',size=10)
        print(message_received)
        input("Press Enter to continue...")

        BillAcceptor.Stat_Byte_0.Escrowed       = 0
        BillAcceptor.Stat_Byte_0.Stacked        = 1
        BillAcceptor.Stat_Byte_2.Bill_Value     = 2
        display_string = BillAcceptor.giveAscii()
        print(display_string)
        serial1.write(display_string)
        message_received = serial1.read_until(expected='\x03',size=10)
        print(message_received)








