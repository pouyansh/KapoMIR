def variable_byte_encode(m):
    bytes_list = ""
    if m == 0:
        bytes_list += chr(128)
        return bytes_list
    binary = int_to_binary(m)
    while len(binary) >= 7:
        num = 0
        temp = 1
        for i in range(7):
            num += binary[i] * temp
            temp *= 2
        if bytes_list == "":
            num += 128
        bytes_list = chr(num) + bytes_list
        for i in range(7):
            binary.pop(0)
    if len(binary) > 0:
        num = 0
        temp = 1
        if bytes_list == "":
            num += 128
        for i in range(len(binary)):
            num += binary[i] * temp
            temp *= 2
        bytes_list = chr(num) + bytes_list
    return bytes_list


def variable_byte_decode(byte_list):
    output = []
    counter = 0
    temp_int = 0
    while counter < len(byte_list):
        temp_int = temp_int * 128 + ord(byte_list[counter])
        if ord(byte_list[counter]) >= 128:
            temp_int -= 128
            output.append(temp_int)
            temp_int = 0
        counter += 1
    return output


def gamma_encode(m):
    binary = int_to_binary(m)
    length = len(binary) - 1
    output_binary = [1 for _ in range(length)]
    output_binary.append(0)
    for i in range(len(binary) - 1):
        output_binary.append(binary[len(binary) - 2 - i])
    return binary_to_str(output_binary)


def int_to_binary(m):
    binary = []
    while m >= 1:
        binary.append(m % 2)
        m = int(m / 2)
    return binary


def str_to_int(s):
    output = 0
    for c in s:
        output = output * 128 + ord(c)
    return output


def binary_to_str(binary):
    s = ""
    while len(binary) > 8:
        byte = [binary[i] for i in range(8)]
        for i in range(8):
            binary.pop(0)
        num = 1
        out = 0
        for i in range(8):
            out += num * byte[i]
            num *= 2
        s = chr(out) + s
    if len(binary) > 0:
        num = 1
        out = 0
        for i in range(len(binary)):
            out += num * binary[i]
            num *= 2
        s = chr(out) + s
    return s
