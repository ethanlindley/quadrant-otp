import struct
from .Datagram import Datagram


class DatagramIterator:
    def __init__(self, dg, index=0):
        self.dg = dg

        # let's keep track of our postition in the datagram
        self.index = index

    def get_bool(self):
        return self.get_uint8() != 0

    def get_string(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = data[self.index]
            self.index += 1
            return temp

    def get_string32(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = data[self.index]
            self.index += 1
            return temp

    def get_z_string(self):
        # TODO
        pass

    def get_fixed_string(self, size):
        # TODO
        pass

    def get_wstring(self):
        # TODO
        pass

    # little endian numeric packing
    def get_int8(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<i', data[self.index])
            self.index += 1
            return temp[0]

    def get_int16(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<i', data[self.index])
            self.index += 1
            return temp[0]

    def get_int32(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<i', data[self.index])
            self.index += 1
            return temp[0]

    def get_int64(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<i', data[self.index])
            self.index += 1
            return temp[0]

    def get_uint8(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<I', data[self.index])
            self.index += 1
            return temp[0]

    def get_uint16(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<I', data[self.index])
            self.index += 1
            return temp[0]

    def get_uint32(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<I', data[self.index])
            self.index += 1
            return temp[0]

    def get_uint64(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<I', data[self.index])
            self.index += 1
            return temp[0]

    def get_float32(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<f', data[self.index])
            self.index += 1
            return temp[0]

    def get_float64(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('<f', data[self.index])
            self.index += 1
            return temp[0]
    
    def get_be_int16(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>i', data[self.index])
            self.index += 1
            return temp[0]

    def get_be_int32(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>i', data[self.index])
            self.index += 1
            return temp[0]

    def get_be_int64(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>i', data[self.index])
            self.index += 1
            return temp[0]      

    def get_be_uint16(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>I', data[self.index])
            self.index += 1
            return temp[0]

    def get_be_uint32(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>I', data[self.index])
            self.index += 1
            return temp[0]

    def get_be_uint64(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>I', data[self.index])
            self.index += 1
            return temp[0]

    def get_be_float32(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>f', data[self.index])
            self.index += 1
            return temp[0]

    def get_be_float64(self):
        if self.index < self.dg.get_length():
            data = self.dg.get_data()
            temp = struct.unpack('>f', data[self.index])
            self.index += 1
            return temp[0]

    def get_remaining_size(self):
        if self.index < self.dg.get_length():
            temp = self.dg.get_data()
            data = []
            i = self.index
            while(i < self.dg.get_length()):
                data.append(temp[i])
                i += 1
            return bytes(data)
