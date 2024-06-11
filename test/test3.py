import math

# Constants
c = 1
b = math.log(6) / 80

# Exponential transfer function
def normalize_input(input, in_min= 10, in_max = 90):

    out = (abs(input) - in_min) / (in_max - in_min)

    return out

def normalize_output(input, in_min= 1, in_max =  math.e, out_min = 1, out_max = 10):
    out = out_min + (input - in_min) * ((out_max - out_min)/(in_max - in_min))
    return out

def exponential_transfer(x):
    return math.exp(x)

# Map the movement to the range 1 to 5 pixels
def map_to_pixels(movement, max_movement):
    return 1 + ((movement - 0) * (5 - 1) / (max_movement - 0))

# Angle input
angle_input = float(input("Enter the angle in degrees (between 10 and 90): "))

# Check if the input angle is within the valid range
if abs(angle_input) < 5:
    print("Angle must be between 10 and 90 degrees.")
else:
    m = normalize_input(angle_input)
    print(m)
    m_2 = exponential_transfer(m)
    m_3 = round(normalize_output(m_2))

    if angle_input < 0:
        m_3 = -m_3

    print(f"At angle {angle_input} degrees, mouse movement: {m_3} pixels")