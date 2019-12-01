def barray_to_int(barray):
    return sum(v<<i for i, v in enumerate(reversed(barray)))


def int_to_barray(integer, size):
    return list(map(lambda x: True if x == '1' else False, list(bin(integer)[2:].zfill(size))))

def build_instruction(params):
    result = []
    for i in range(len(params) -1, -1, -1):
        result += list((params[i]))
    print("formatted: {}".format(result))
    return result