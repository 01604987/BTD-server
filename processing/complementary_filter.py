import math
from processing.data_collection import AccelGyroData

# https://www.geekmomprojects.com/wp-content/uploads/2022/03/filter.pdf
# http://www.geekmomprojects.com/gyroscopes-and-accelerometers-on-a-chip/

# This complimentary filter can quickly and semi robustly estimate orientation for pitch and roll with accelerometer and gyroscope data.
# This filter is not suitable for accurately estimating the z axis because gravitational force does not influence yaw.
# The goal is to use the orientation data to subtract gravitational influence within the accelerometer signal for linear accelerometer data.

#! acceleration and gyroscope calibration not considered.
# TODO implement acceleration scaling and offsets


ag = AccelGyroData()
ALPHA = 0.97
DT = 0.01

RADIANS_TO_DEG = 180/3.14159

def calculate_accel_angles(current_accel_xyz:list):
    try:
        accel_angle_x = math.atan(current_accel_xyz[1] / math.sqrt(math.pow(current_accel_xyz[0], 2) + math.pow(current_accel_xyz[2], 2))) * RADIANS_TO_DEG
    except ZeroDivisionError:
        accel_angle_x = 0
    try:
        accel_angle_y = math.atan(-1 * current_accel_xyz[0] / math.sqrt(math.pow(current_accel_xyz[1], 2) + math.pow(current_accel_xyz[2], 2))) * RADIANS_TO_DEG
    except ZeroDivisionError:
        accel_angle_y = 0
    accel_angle_z = 0

    return [accel_angle_x, accel_angle_y, accel_angle_z]

def calculate_gyro_angles(current_gyro_xyz:list, last_angle_xyz:list, dt):
    gyro_angle_x = current_gyro_xyz[0] *dt + last_angle_xyz[0]
    gyro_angle_y = current_gyro_xyz[1] *dt + last_angle_xyz[1]
    gyro_angle_z = current_gyro_xyz[2] *dt + last_angle_xyz[2]

    return [gyro_angle_x, gyro_angle_y, gyro_angle_z]
    
def calculate_drifting_gyro_agnles(current_gyro_xyz:list, last_gyro_angle_xyz:list, dt):
    unfiltered_gyro_angle_x = current_gyro_xyz[0] *dt + last_gyro_angle_xyz[0]
    unfiltered_gyro_angle_y = current_gyro_xyz[1] *dt + last_gyro_angle_xyz[1]
    unfiltered_gyro_angle_z = current_gyro_xyz[2] *dt + last_gyro_angle_xyz[2]

    return [unfiltered_gyro_angle_x, unfiltered_gyro_angle_y, unfiltered_gyro_angle_z]
    
def apply_complimentary_filter(alpha, gyro_angles:list, accel_angles:list):
    angle_x = alpha * gyro_angles[0] + (1.0 - alpha) * accel_angles[0]
    angle_y = alpha * gyro_angles[1] + (1.0 - alpha) * accel_angles[1]
    angle_z = gyro_angles[2]

    return [angle_x, angle_y, angle_z]



def estimate_orientation(current_accel_xyz:list, current_gyro_xyz:list):
    accel_angles = calculate_accel_angles(current_accel_xyz)
    filtered_gyro_angles = calculate_gyro_angles(current_gyro_xyz, ag.last_angle_xyz, DT)
    orientation = apply_complimentary_filter(ALPHA, filtered_gyro_angles, accel_angles)
    ag.update_last_values(orientation,filtered_gyro_angles)

    return orientation