from constants import LETTER_MATRIX_SIZE
import numpy as np

def payoff_letter_form(underlying_price:float, support_intervals:list, letter_scaling:float, word_matrix:np.array) -> float:
    result = None
    for interval_idx in range(len(support_intervals)):
        if support_intervals[interval_idx][0] <= underlying_price <= support_intervals[interval_idx][1]:
            zero_collected = False
            for pixel_idx in range(LETTER_MATRIX_SIZE):
                result = word_matrix[LETTER_MATRIX_SIZE - (pixel_idx + 1), interval_idx] * (pixel_idx + 1)/LETTER_MATRIX_SIZE * letter_scaling
                if result == 0.:
                    if not zero_collected:
                        zero_collected = True
                        yield result
                else: 
                    yield result
            break
    if result is None:
        yield 0.

def payoff_aggregated_form(underlying_price:float, support_intervals:list, asset_payoff:np.array) -> float:
    result = 0
    i = 0
    while underlying_price > min(support_intervals[i]):
        result = asset_payoff[i]
        if i < len(support_intervals) -1: 
            i += 1
        else:
            result = 0
            break
    return result