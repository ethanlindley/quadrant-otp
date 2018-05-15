import struct

int_8 = [-128, 127]
int_16 = [-32768, 32767]
int_32 = [-2147483648, 2147483647]
int_64 = [-9223372036854775808, 9223372036854775807]

uint_8 = [0, 255]
uint_16 = [0, 65535]
uint_32 = [0, 4294967295]
uint_64 = [0, 18446744073709551615]


class Datagram:
    """
    An ordered list of data elements, formatted in memory for transmission over a socket or writing data to a file.

    Data elements should be added one at a time, in order, to the datagram. The nature and contents of the
    data elements are completely up to the user.

    When a datagram has been transmitted and received, its data elements may be extracted using a
    DatagramIterator; it is up to the caller to know the correct tpye of each data element in order.

    A datagram is itself headerless; it is simple a collection of data elements.    
    """

    def __init__(self, data=None):
        self.dg = data if data is not None else []

    def reset(self):
        self.dg = []

    def append_data(self, data):
        if len(str(data)) >= 0:
            self.dg.append(data)
    
    def get_message(self):
        return ''.join(self.dg)
    
    def get_data(self):
        return self.dg

    def get_array(self):
        # generally, this method won't ever be called
        # although it serves the same purpose as the get_data method,
        # it seems that the C++ implementation never really has a use for 
        # this method... but, we'll leave it here anyways
        return self.dg
    
    def get_length(self):
        return len(self.get_message())

    def add_bool(self, bool):
        if int(bool) == 0 or int(bool) == 1:
            self.add_uint8(int(bool))

    def add_string(self, string):
        if len(string) <= uint_16[1]:
            self.add_uint16(len(string))
            self.append_data(string)

    def add_string32(self, string32):
        if len(string) <= uint_32[1]:
            self.add_uint32(len(string))
            self.append_data(string)

    def add_z_string(self, z_string):
        # TODO
        pass

    def add_fixed_string(self, string, size):
        if len(string) < size:
            while(len(string) < size):
                # pad the string out with zeroes until fulfilling desired length
                string = string + '0'
        elif len(string) > size:
            # truncate the string
            string = string[:size]
        
        # i'm not entirely sure if this implementation is correct or not
        if size >= int_8[0] and size <= int_8[1]:
            self.add_int8(len(string))
            self.append_data(string)
        elif size >= int_16[0] and size <= int_16[1]:
            self.add_int16(len(string))
            self.append_data(string)
        elif size >= int_32[0] and size <= int_32[1]:
            self.add_int32(len(string))
            self.append_data(string)
        elif size >= int_64[0] and size <= int_64[1]:
            self.add_int64(len(string))
            self.append_data(string)
        elif size >= uint_8[0] and size <= uint_8[1]:
            self.add_uint8(len(string))
            self.append_data(string)
        elif size >= uint_16[0] and size <= uint_16[1]:
            self.add_string(string)
        elif size >= uint_32[0] and size <= uint_32[1]:
            self.add_string32(string)
    
    def add_wstring(self, wstring):
        # TODO
        pass

    # little endian numeric packing
    def add_int8(self, int8):
        if int8 >= int_8[0] and int8 <= int_8[1]:
            data = struct.pack('<i', int8)
            self.append_data(data)

    def add_int16(self, int16):
        if int16 >= int_16[0] and int16 <= int_16[1]:
            data = struct.pack('<i', int16)
            self.append_data(data)

    def add_int32(self, int32):
        if int32 >= int_32[0] and int32 <= int_32[1]:
            data = struct.pack('<i', int32)
            self.append_data(data)

    def add_int64(self, int64):
        if int64 >= int_64[0] and int64 <= int_64[1]:
            data = struct.pack('<i', int64)
            self.append_data(data)

    def add_uint8(self, uint8):
        if uint8 >= uint_8[0] and uint8 <= uint_8[1]:
            data = struct.pack('<I', uint8)
            self.append_data(data)

    def add_uint16(self, uint16):
        if uint16 >= uint_16[0] and uint16 <= uint_16[1]:
            data = struct.pack('<I', uint16)
            self.append_data(data)

    def add_uint32(self, uint32):
        if uint32 >= uint_32[0] and uint32 <= uint_32[1]:
            data = struct.pack('<I', uint32)
            self.append_data(data)

    def add_uint64(self, uint64):
        if uint64 >= uint_64[0] and uint64 <= uint_64[1]:
            data = struct.pack('<I', uint64)
            self.append_data(data)

    def add_float32(self, float32):
        data = struct.pack('<f', float32)
        self.append_data(data)

    def add_float64(self, float64):
        data = struct.pack('<f', float64)
        self.append_data(data)

    def add_stdfloat(self, stdfloat):
        # TODO
        pass

    # big endian numeric packing
    def add_be_int16(self, int16):
        if int16 >= int_16[0] and int16 <= int_16[1]:
            data = struct.pack('>i', int16)
            self.append_data(data)

    def add_be_int32(self, int32):
        if int32 >= int_32[0] and int32 <= int_32[1]:
            data = struct.pack('>i', int32)
            self.append_data(data)

    def add_be_int64(self, int64):
        if int64 >= int_64[0] and int64 <= int_64[1]:
            data = struct.pack('>i', int64)
            self.append_data(data)

    def add_be_uint16(self, uint16):
        if uint16 >= uint_16[0] and uint16 <= uint_16[1]:
            data = struct.pack('>I', uint16)
            self.append_data(data)

    def add_be_uint32(self, uint32):
        if uint32 >= uint_32[0] and uint32 <= uint_32[1]:
            data = struct.pack('>I', uint32)
            self.append_data(data)

    def add_be_uint64(self, uint64):
        if uint64 >= uint_64[0] and uint64 <= uint_64[1]:
            data = struct.pack('>I', uint64)
            self.append_data(data)

    def add_be_float32(self, float32):
        data = struct.pack('>f', float32)
        self.append_data(data)

    def add_be_float64(self, float64):
        data = struct.pack('>f', float64)
        self.append_data(data)
