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
#! third order filter unstable, too much oscillation
coeff = {
    "lpf_1": {
        "a1": 0.8277396009129062,
        "b0": 0.08613019954354695,
        "b1": 0.08613019954354684
    },
    "hpf_1": {
        "a1": 0.881765205116502,
        "b0": 0.9408826025582511,
        "b1": -0.940882602558251
    },
    "lpf_2": {
        "a1": 1.7355001604915916,
        "a2": -0.7666081416523297,
        "b0": 0.007776995290184496,
        "b1": 0.01555399058036877,
        "b2": 0.007776995290184718
    },
    "hpf_2": {
        "a1": 1.822926692375394,
        "a2": -0.8373769921169095,
        "b0": 0.004575379605615382,
        "b1": 2.220446049250313e-16,
        "b2": -0.004575379605615604
    },
    "lpf_3": {
        "a1": 2.921851076865978,
        "a2": -2.8540995334053227,
        "a3": 0.9258007854025219,
        "b0": 0.0008059588921028871,
        "b1": 0.002417876676306552,
        "b2": 0.0024178766763141013,
        "b3": 0.0008059588920995564
    },
    "hpf_3": {
        "a1": 2.949043286563117,
        "a2": -2.901479294223616,
        "a3": 0.9505009621056156,
        "b0": 0.9751279428615438,
        "b1": -2.92538382858463,
        "b2": 2.9253838285846285,
        "b3": -0.9751279428615425
    }
}
temp_bandpass_input_output =  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
temp_size = len(temp_bandpass_input_output)

def bandpass_first_order(output, input, axis, n_out = 5000, n_in = 5000):
    current_input = first_order(temp_bandpass_input_output, input, axis, temp_size, n_in, filter = "hpf")

    temp_bandpass_input_output.append(temp_bandpass_input_output[temp_size - 1].copy())
    temp_bandpass_input_output.pop(0)
    temp_bandpass_input_output[temp_size - 1][axis] = current_input

    result = first_order(output, temp_bandpass_input_output, axis, n_out, temp_size, filter = "lpf")

    return result


def bandpass_second_order(output, input, axis, n_out = 5000, n_in = 5000):
    current_input = second_order(temp_bandpass_input_output, input, axis, temp_size, n_in, filter = "hpf")

    temp_bandpass_input_output.append(temp_bandpass_input_output[temp_size - 1].copy())
    temp_bandpass_input_output.pop(0)
    temp_bandpass_input_output[temp_size - 1][axis] = current_input

    result = second_order(output, temp_bandpass_input_output, axis, n_out, temp_size, filter = "lpf")

    return result

def bandpass_third_order(output, input, axis, n_out = 5000, n_in = 5000):
    current_input = third_order(temp_bandpass_input_output, input, axis, temp_size, n_in, filter = "hpf")

    temp_bandpass_input_output.append(temp_bandpass_input_output[temp_size - 1].copy())
    temp_bandpass_input_output.pop(0)
    temp_bandpass_input_output[temp_size - 1][axis] = current_input

    result = third_order(output, temp_bandpass_input_output, axis, n_out, temp_size, filter = "lpf")

    return result



def third_order(output, input, axis,  n_out = 5000, n_in = 5000, filter = "lpf"):

    f = "lpf_3"

    if filter == "hpf":
        f = "hpf_3"

    # output[n-1] is the previous output because n is size of list.
    # input[n-1] is the current input because raw signal values will be stored into the input list before running this filter.
    result = coeff.get(f).get("a1") * output[n_out - 1][axis] + coeff.get(f).get("a2") * output[n_out - 2][axis] + coeff.get(f).get("a3") * output[n_out - 3][axis] + coeff.get(f).get("b0") * input[n_in - 1][axis] + coeff.get(f).get("b1") * input[n_in - 2][axis] + coeff.get(f).get("b2") * input[n_in - 3][axis] + coeff.get(f).get("b3") * input[n_in - 4][axis]
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