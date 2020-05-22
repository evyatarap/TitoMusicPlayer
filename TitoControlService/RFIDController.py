from pirc522 import RFID

class RFIDReader(object):
    
    @staticmethod
    def ReadTag():
        rdr = RFID()

        rdr.wait_for_tag()
        (error, data) = rdr.request()
        if not error:
            (error, uid) = rdr.anticoll()
            rdr.cleanup()
            if not error:
                return str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])

        return None
                
        