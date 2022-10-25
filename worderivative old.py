import numpy as np
import pandas as pd
import string
import matplotlib.pyplot as plt

from constants import *
from optionpricing import Call


class WorDerivative():
    def __init__(self, word:str, mid_price:float, price_range:float, letter_height_scaling:float=1., call_data_path:str=OPTION_PRICE_DATA_PATH, call_pricing_degree_of_approx:int=4, call_pricing_strike_thresholds:list=None) -> None:
        self.word = word.upper()
        self.mid_price = mid_price # Determines the underlying price around which the price will be centered
        self.price_range = price_range # Determines the width of the text across underlying prices
        self.letter_scaling = letter_height_scaling # Determines the height of the letter payoffs
        
        self._letters = pd.read_excel(LETTER_REF_FILE_PATH, header=None)
        self.call = Call(call_data_path, call_pricing_degree_of_approx, call_pricing_strike_thresholds)

        self._word_matrix = self._build_word_matrix()
        self._asset_payoff = (self.letter_scaling * np.diag(np.array(np.linspace(1, 0, LETTER_MATRIX_SIZE))) @ self._word_matrix).sum(axis=0) # Aggregates the payoff at each point to a sum of the payoffs and multiplies that by the scaling factor
        self._price_points = self._generate_support_point_range(len(self.word), self.mid_price, self.price_range) # Determines the width of the text
        self.price = self._get_derivative_price(self._asset_payoff, self._price_points) # add self._build_word_matrix

    def _get_letter_matrix(self, letter:str) -> np.array:
        letter_idx = string.ascii_lowercase.index(letter.lower())
        df = self._letters.iloc[:, LETTER_MATRIX_SIZE * letter_idx:LETTER_MATRIX_SIZE * letter_idx + LETTER_MATRIX_SIZE]
        return df.to_numpy()

    def _build_word_matrix(self) -> np.array:
        target_array = np.zeros((LETTER_MATRIX_SIZE, (LETTER_MATRIX_SIZE + LETTER_SPACING) * len(self.word) - LETTER_SPACING))
        for letter_idx in range(len(self.word)):
            target_array[:, (LETTER_MATRIX_SIZE + LETTER_SPACING) * letter_idx : \
                            (LETTER_MATRIX_SIZE + LETTER_SPACING) * letter_idx + LETTER_MATRIX_SIZE] \
                                = self._get_letter_matrix(list(self.word)[letter_idx]) #add .lower() at the end if this crashes
        return target_array

    def _generate_support_point_range(self, no_of_letters:int, current_price:float, price_range:float) -> np.array:
        return np.linspace(current_price - price_range / 2, \
                            current_price + price_range / 2, (LETTER_MATRIX_SIZE + LETTER_SPACING) * no_of_letters - LETTER_SPACING)

    def _get_derivative_price(self, payoff_structure:np.array, price_points:np.array) -> float:
        return MARKER_WIDTH * (payoff_structure @ np.fromiter(map(self.call.price_second_derivative, price_points), dtype=np.float64)) 

    def plot_word_matrix(self) -> None:
        plt.spy(self._word_matrix)

    def plot_payoff(self, x_boundaries:list=None, aggregated=True) -> None:
        def payoff_letter_form(underlying_price:float) -> float:
            result = None
            for interval_idx in range(len(support_intervals)):
                if support_intervals[interval_idx][0] <= underlying_price <= support_intervals[interval_idx][1]:
                    zero_collected = False
                    for pixel_idx in range(LETTER_MATRIX_SIZE):
                        result = self._word_matrix[LETTER_MATRIX_SIZE - (pixel_idx + 1), interval_idx] * (pixel_idx + 1)/LETTER_MATRIX_SIZE * self.letter_scaling
                        if result == 0.:
                            if not zero_collected:
                                zero_collected = True
                                yield result
                        else: 
                            yield result
                    break
            if result is None:
                yield 0.

        def payoff_aggregated_form(underlying_price:float) -> float:
            result = 0
            i = 0
            while underlying_price > min(support_intervals[i]):
                result = self._asset_payoff[i]
                if i < len(support_intervals) -1: 
                    i += 1
                else:
                    result = 0
                    break
            return result

        if x_boundaries is None:
            x_boundaries = [self.mid_price - self.price_range/2, self.mid_price + self.price_range/2]
        support_intervals = [[self._price_points[i] - MARKER_WIDTH / 2, self._price_points[i] + MARKER_WIDTH /2] for i in range(len(self._price_points))]

        x = np.linspace(x_boundaries[0], x_boundaries[1], DERIVATIVE_PAYOFF_PLOT_DENSITY)

        if not aggregated:
            y = []
            for i in x:
                y.append(list(payoff_letter_form(i)))
            for xe, ye in zip(x, y):
                plt.scatter([xe] * len(ye), ye, c='black')
        else:
            y = np.fromiter(map(payoff_aggregated_form, x), dtype=np.float64)
            plt.scatter(x, y)

        plt.xlabel(f"Price of the underlying {self.call.meta['Underlying asset']} on {self.call.meta['Call expiration date']}")
        plt.ylabel("Derivative payoff" if not aggregated else "Derivative payoff (aggregated)")
        