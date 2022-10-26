import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from constants import *


class Call():
    def __init__(self, data_path, degree_of_approx=4, strike_thresholds:list=None) -> None:
        self.data_path = data_path
        self._data = pd.read_excel(self.data_path, sheet_name=OPTION_PRICE_DATA_TEMPLATE_SHEET_NAME)
        self.meta = pd.read_excel(self.data_path, sheet_name=OPTION_PRICE_DATA_META_SHEET_NAME, header=1 ,usecols=[1,2]).set_index("Key")["Value"].to_dict()
        self.degree_of_approx = degree_of_approx
        if strike_thresholds is None:
            self.strike_thresholds = [self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE].min(), self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE].max()]
        else:
            self.strike_thresholds = strike_thresholds
        self._data = self._data[(self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE] >= self.strike_thresholds[0]) & (self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE] <= self.strike_thresholds[1])]
        self.approx_parameters = np.polyfit(self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE], self._data[OPTION_PRICE_DATA_PRICE_COLUMN_TITLE], self.degree_of_approx)
        
    def price(self, strike:float) -> float:
        return np.poly1d(self.approx_parameters)(strike)
    
    def price_second_derivative(self, strike:float) -> float:
        if not hasattr(self, "_derivative_coefficients"):
            self._derivative_coefficients = np.array([np.math.factorial(i)/np.math.factorial(i-2) for i in range(self.degree_of_approx, 1, -1)])
            self._derivative_matrix = self._derivative_coefficients.T @ np.diag(self.approx_parameters[:self.degree_of_approx - 1])
        strike_powers = np.array([strike**i for i in range(self.degree_of_approx - 2, -1, -1)])
        return self._derivative_matrix @ strike_powers

    def plot_price_chart(self, range:list=None) -> None:
        if not range:
            range = self.strike_thresholds
        
        # Plot real price points in grey and a vertical line, that indicates the trading price of the underlying at the time of the snapshot
        x_real = self._data["strike"]
        y_real = self._data["price"]
        plt.scatter(x_real, y_real, c="grey")
        plt.axvline(x=self.meta["Underlying price during call snapshot"], c="grey")

        # Overlay approximated call price function in blue
        x = np.linspace(range[0], range[1], CALL_PRICE_PLOT_DENSITY)
        y = np.fromiter(map(self.price, x), dtype=np.float64)
        plt.xlabel("Strike price")
        plt.ylabel("Approximated call price")
        plt.plot(x, y)

