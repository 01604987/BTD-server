import numpy as np
from scipy import signal
import json

# low-pass filter parameters based on sampling and cutoff frequencies (fs, fc)
def lpfParams_first_order (fc, fs):
    w0 = 2*np.pi*fc;    # cutoff frequency (in rad/s)
    num = w0            # transfer function numerator coefficients
    den = [1,w0]        # transfer function denominator coefficients
    lowPass = signal.TransferFunction(num,den) # transfer function
    dt = 1.0/fs                                # time between samples
    result = lowPass.to_discrete(dt,method='gbt',alpha=0.5) # coefficients in numerator/denominator
    b = result.num  # will become coefficients of current and previous input samples
    a = -result.den # will become coefficients of previous output sample
    return a,b

# high-pass filter parameters based on sampling and cutoff frequencies (fs, fc)
def hpfParams_first_order (fc, fs):
    w0 = 2*np.pi*fc;    # cutoff frequency (in rad/s)
    num = [1,0]         # transfer function numerator coefficients
    den = [1,w0]        # transfer function denominator coefficients
    lowPass = signal.TransferFunction(num,den) # transfer function
    dt = 1.0/fs                                # time between samples
    result = lowPass.to_discrete(dt,method='gbt',alpha=0.5) # coefficients in numerator/denominator
    b = result.num  # will become coefficients of current and previous input samples
    a = -result.den # will become coefficients of previous output sample
    return a,b

def second_order_lpf_params(fc, fs, zeta=np.sqrt(2)/2):
    w0 = 2 * np.pi * fc  # cutoff frequency (in rad/s)
    
    # Define the second-order transfer function numerator and denominator coefficients
    num = [w0**2]  # Transfer function numerator coefficients (second-order)
    den = [1, 2*zeta*w0, w0**2]  # Transfer function denominator coefficients (standard second-order)

    lowPass = signal.TransferFunction(num, den)  # Transfer function
    dt = 1.0 / fs  # time between samples

    # Convert to discrete time using bilinear transformation
    result = lowPass.to_discrete(dt, method='gbt', alpha=0.5)

    # Extract the coefficients
    b = result.num  # numerator coefficients
    a = -result.den  # denominator coefficients

    return a, b

def second_order_hpf_params(fc, fs, zeta=np.sqrt(2)/2):
    w0 = 2 * np.pi * fc  # cutoff frequency (in rad/s)
    
    # Define the second-order transfer function numerator and denominator coefficients
    num = [1, 0]  # Transfer function numerator coefficients (second-order)
    den = [1, 2*zeta*w0, w0**2]  # Transfer function denominator coefficients (standard second-order)

    lowPass = signal.TransferFunction(num, den)  # Transfer function
    dt = 1.0 / fs  # time between samples

    # Convert to discrete time using bilinear transformation
    result = lowPass.to_discrete(dt, method='gbt', alpha=0.5)

    # Extract the coefficients
    b = result.num  # numerator coefficients
    a = -result.den  # denominator coefficients

    return a, b

# Example usage
cutoff_freq_lpf = 4  # 10 Hz cutoff frequency
cutoff_freq_hpf = 2
sampling_rate = 100  # 100 Hz sampling rate


c = {


}

a, b = lpfParams_first_order(cutoff_freq_lpf, sampling_rate)
# Print coefficients
c["lpf_1"] = {
    "a1" : a[1],
    "b0" : b[0],
    "b1" : b[1]
}

print("first order lpf")
print("Denominator coefficients (a):", a)
print("Numerator coefficients (b):", b)

a, b = hpfParams_first_order(cutoff_freq_hpf, sampling_rate)
# Print coefficients

c["hpf_1"] = {
    "a1" : a[1],
    "b0" : b[0],
    "b1" : b[1]
}

print("first order hpf")
print("Denominator coefficients (a):", a)
print("Numerator coefficients (b):", b)

a, b = second_order_lpf_params(cutoff_freq_lpf, sampling_rate)
# Print coefficients

c["lpf_2"] = {
    "a1" : a[1],
    "a2" : a[2],
    "b0" : b[0],
    "b1" : b[1],
    "b2" : b[2]
}

print("second order lpf")
print("Denominator coefficients (a):", a)
print("Numerator coefficients (b):", b)

a, b = second_order_hpf_params(cutoff_freq_hpf, sampling_rate)
# Print coefficients

c["hpf_2"] = {
    "a1" : a[1],
    "a2" : a[2],
    "b0" : b[0],
    "b1" : b[1],
    "b2" : b[2]
}

print("second order hpf")
print("Denominator coefficients (a):", a)
print("Numerator coefficients (b):", b)

print(json.dumps(c, sort_keys=False, indent=4))