import struct


def ntohs_array(data):
    # ! is used for big endian network byte order. Since C code simply sends intbuffer as is, no order has been defined => should expect without network order. 
    float_values = struct.unpack('fff', data)
    return float_values

