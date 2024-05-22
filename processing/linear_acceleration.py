import numpy as np

accel = [3]

#! Acceleration readings in z axis is flipped when laying flat with screen on top.
# TODO figure out how to un flip only z axis.


def free_linear_acceleration(filtered_accel, filtered_orientation):
    
    # Accelerometer readings as a vector
    accel  = np.array([filtered_accel[0], filtered_accel[1], filtered_accel[2]])

    pitch, roll = deg_to_rad(filtered_orientation[0], filtered_orientation[1])

    r_x, r_y = get_rot_mats(pitch, roll)
    
    # Combine the rotation matrices
    R = np.dot(r_y, r_x)

    # Gravitational acceleration vector in the global coordinate system
    g_global = np.array([0, 0, -1])

    # Calculate the gravitational component in the device's coordinate system
    g_device = np.dot(R, g_global)

    # Subtract the gravitational component to get the linear acceleration
    a_linear = accel - g_device

    result = a_linear.tolist()

    return result

# Convert angles to radians
def deg_to_rad (pitch, roll):
    p = np.radians(pitch)
    r = np.radians(roll)
    return p, r

# Define the rotation matrices
def get_rot_mats(pitch, roll):

    r_x = np.array([
        [1, 0, 0],
        [0, np.cos(pitch), -np.sin(pitch)],
        [0, np.sin(pitch), np.cos(pitch)]
    ])

    r_y = np.array([
        [np.cos(roll), 0, np.sin(roll)],
        [0, 1, 0],
        [-np.sin(roll), 0, np.cos(roll)]
    ])
    return r_x, r_y