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