# TODO calibration


x_coeff = {
    "hpf": {
        "outputCoeff" : [0.93908194],
        "inputCoeff" : [ 0.96954097 , -0.96954097]
    },
    "lpf": {
        "outputCoeff": [0.8277396],
        "inputCoeff" : [0.0861302, 0.0861302]
    }
}

coeff = {
    "lpf_1": {
        "a1": 0.7767295765906806,
        "b0": 0.11163521170465973,
        "b1": 0.11163521170465973
    },
    "hpf_1": {
        "a1": 0.881765205116502,
        "b0": 0.9408826025582511,
        "b1": -0.940882602558251
    },
    "lpf_2": {
        "a1": 1.6492720915332548,
        "a2": -0.7021963599799214,
        "b0": 0.013231067111666661,
        "b1": 0.026462134223332878,
        "b2": 0.013231067111666994
    },
    "hpf_2": {
        "a1": 1.822926692375394,
        "a2": -0.8373769921169095,
        "b0": 0.004575379605615382,
        "b1": 2.220446049250313e-16,
        "b2": -0.004575379605615604
    }
}

temp_bandpass_input_output =  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
temp_size = len(temp_bandpass_input_output)

def bandpass_first_order(output, input, axis, n_out = 5000, n_in = 5000):
    current_input = first_order(temp_bandpass_input_output, input, axis, temp_size, n_in, filter = "hpf")

    temp_bandpass_input_output.append(temp_bandpass_input_output[2].copy())
    temp_bandpass_input_output.pop(0)
    temp_bandpass_input_output[2][axis] = current_input

    result = first_order(output, temp_bandpass_input_output, axis, n_out, temp_size, filter = "lpf")

    return result


def bandpass_second_order(output, input, axis, n_out = 5000, n_in = 5000):
    current_input = second_order(temp_bandpass_input_output, input, axis, temp_size, n_in, filter = "hpf")

    temp_bandpass_input_output.append(temp_bandpass_input_output[2].copy())
    temp_bandpass_input_output.pop(0)
    temp_bandpass_input_output[2][axis] = current_input

    result = second_order(output, temp_bandpass_input_output, axis, n_out, temp_size, filter = "lpf")

    return result

# output list, input list, size of both lists
def second_order(output, input, axis,  n_out = 5000, n_in = 5000, filter = "lpf"):

    f = "lpf_2"

    if filter == "hpf":
        f = "hpf_2"

    # output[n-1] is the previous output because n is size of list.
    # input[n-1] is the current input because raw signal values will be stored into the input list before running this filter.
    result = coeff.get(f).get("a1") * output[n_out - 1][axis] + coeff.get(f).get("a2") * output[n_out - 2][axis] + coeff.get(f).get("b0") * input[n_in - 1][axis] + coeff.get(f).get("b1") * input[n_in - 2][axis] + coeff.get(f).get("b2") * input[n_in - 3][axis]
    return result


def first_order(output, input, axis, n_out = 5000, n_in = 5000, filter = "lpf"):
    f = "lpf_1"

    if filter == "hpf":
        f = "hpf_1"

    # print(output[n_out - 1][axis])
    # print(input[n_in - 1][axis])
    # output[n-1] is the previous output because n is size of list.
    # input[n-1] is the current input because raw signal values will be stored into the input list before running this filter.
    result = coeff.get(f).get("a1") * output[n_out - 1][axis]  + coeff.get(f).get("b0") * input[n_in - 1][axis] + coeff.get(f).get("b1") * input[n_in - 2][axis]
    return result

def applyFilter_x(prev_out, curr_in, prev_in, hpf = False) :
    
    if hpf: 
        output = x_coeff.get("hpf").get("outputCoeff")[0] * prev_out + x_coeff.get("hpf").get("inputCoeff")[0] * curr_in + x_coeff.get("hpf").get("inputCoeff")[1] * prev_in
    else:
        output = x_coeff.get("lpf").get("outputCoeff")[0] * prev_out + x_coeff.get("lpf").get("inputCoeff")[0] * curr_in + x_coeff.get("lpf").get("inputCoeff")[1] * prev_in

    return output

def applyFilter(prev_out, curr_in, prev_in, inputCoeff = [1,0], outputCoeff = [0]):
# Filter the signal using the difference equation
    output = outputCoeff[0] * prev_out + inputCoeff[0] * curr_in + inputCoeff[1] * prev_in

    return output