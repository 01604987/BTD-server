import numpy as np
from scipy.signal import butter

def butterworth_lowpass_coefficients(cutoff_freq, sampling_rate):
    # Calculate the normalized cutoff frequency
    nyquist_freq = 0.5 * sampling_rate
    normalized_cutoff_freq = cutoff_freq / nyquist_freq
    
    # Get the filter coefficients using scipy's butter function
    b, a = butter(N=2, Wn=normalized_cutoff_freq, btype='low', analog=False)
    
    # Extract coefficients
    b0, b1, b2 = b
    a0, a1, a2 = a
    
    # Normalize coefficients
    b0, b1, b2 = b0 / a0, b1 / a0, b2 / a0
    a1, a2 = a1 / a0, a2 / a0
    
    return a1, a2, b0, b1, b2

# Example usage
cutoff_freq = 3  # 10 Hz cutoff frequency
sampling_rate = 100  # 100 Hz sampling rate

a1, a2, b0, b1, b2 = butterworth_lowpass_coefficients(cutoff_freq, sampling_rate)

print("a1:", a1)
print("a2:", a2)
print("b0:", b0)
print("b1:", b1)
print("b2:", b2)