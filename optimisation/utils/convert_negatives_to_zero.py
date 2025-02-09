def convert_negatives_to_zero(lst):
    return [x if x >= 0 else 0 for x in lst]