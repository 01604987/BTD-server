import struct


def ntohs_array(data):
    # ! is used for big endian network byte order. Since C code simply sends intbuffer as is, no order has been defined => should expect without network order. 
    float_values = struct.unpack('fff', data)
    return float_values

def ntohs_array_imu(data):
    int_values = struct.unpack('HHHHHH', data)
    return int_values

def ntohs_array_imu_float(data):
    float_values = struct.unpack('ffffff', data)
    return float_values