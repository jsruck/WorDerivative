import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from constants import *


class Call():
    def __init__(self, data_path, degree_of_approx=4, strike_thresholds:list=None) -> None:
        # Import provided call data
        self.data_path = data_path
        if strike_thresholds is None:
            self.strike_thresholds = [self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE].min(), self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE].max()]
        else:
            self.strike_thresholds = strike_thresholds
        self._data = pd.read_excel(self.data_path, sheet_name=OPTION_PRICE_DATA_TEMPLATE_SHEET_NAME)
        self._data = self._data[(self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE] >= self.strike_thresholds[0]) & (self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE] <= self.strike_thresholds[1])]
        self.meta = pd.read_excel(self.data_path, sheet_name=OPTION_PRICE_DATA_META_SHEET_NAME, header=1, usecols=[1, 2]).set_index("Key")["Value"].to_dict()
        self.degree_of_approx = degree_of_approx
       # Ensure to limit the functional approximation to specified degree and sample range
        self.approx_parameters = np.polyfit(self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE], self._data[OPTION_PRICE_DATA_PRICE_COLUMN_TITLE], self.degree_of_approx)
        
    def price(self, strike:float) -> float:
        """Returns the approximated call price for a given input strike price.

        Args:
            strike (float): A non-negative strike price for which the price of an associated 
            call is requested. It is recommended to stay within the strike_threshold boundaries.

        Returns:
            float: The approximated price of a call with this strike price. 
        """
        return np.poly1d(self.approx_parameters)(strike)
    
    def price_second_derivative(self, strike:float) -> float:
        """This function returns the second derivative of the polynomial defined by the approx parameters, evaluated at a given strike price.

        Args:
            strike (float): A non-negative float that is interpreted as the strike price for which 
            the second derivative of the price of an associated call is requested. It is recommended 
            to stay within the strike_threshold boundaries.

        Returns:
            float: The second derivative of the call price approximation, evaluated at a given strike price.
        """
        if not hasattr(self, "_derivative_coefficients"):
            #  Store the constant pre-multiplication matrix for the second derivative of the price function upon first call to optimize runtime
            self._derivative_coefficients = np.array([np.math.factorial(i) / np.math.factorial(i-2) for i in range(self.degree_of_approx, 1, -1)])
            self._derivative_matrix = self._derivative_coefficients.T @ np.diag(self.approx_parameters[:self.degree_of_approx - 1])
        strike_powers = np.array([strike**i for i in range(self.degree_of_approx - 2, -1, -1)])
        return self._derivative_matrix @ strike_powers

    def plot_price_chart(self, range:list=None) -> None:
        """Returns a plot of the provided call price data and the approximated polynomial price function.

        Args:
            range (list, optional): A list of two floats to limit the strike price axis. 
            Can be used to conduct a rough visual assessment of the approximated price function. 
            Defaults to None, which will then draw on the strike_thresholds.
        """
        if not range:
            range = self.strike_thresholds
        
        # Plot real price points in grey and a vertical line, that indicates the trading price of the underlying at the time of the snapshot
        x_real = self._data[OPTION_PRICE_DATA_STRIKE_COLUMN_TITLE]
        y_real = self._data[OPTION_PRICE_DATA_PRICE_COLUMN_TITLE]
        plt.scatter(x_real, y_real, c="grey")
        plt.axvline(x=self.meta[CALL_PRICE_TEMPLATE_UNDERLYING_PRICE_AT_SNAPSHOT_KEY], c="grey")

        # Overlay approximated call price function in blue
        x = np.linspace(range[0], range[1], CALL_PRICE_PLOT_DENSITY)
        y = np.fromiter(map(self.price, x), dtype=np.float64)
        plt.xlabel(CALL_PRICE_CHART_XLABEL)
        plt.ylabel(CALL_PRICE_CHART_YLABEL)
        plt.plot(x, y)

