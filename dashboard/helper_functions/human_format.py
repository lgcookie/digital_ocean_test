import math
def human_format(num):

    if num == 0:
        return "0"

    magnitude = int(math.log(abs(num), 1000))

    mantissa = str(round(num / (1000 ** magnitude),2))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]
