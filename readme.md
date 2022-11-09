# WorDerivative - *How much would you pay for 'that'?*

##### JSR | Oct-2022

Pricing textual derivative payoffs.

## Table of Contents

- Background and Concept
- Usage
- Settings and Options
- Current Limitations and Future Versions
- Current ToDos
- External Libraries
- Sources

## Background and Concept
This tool is based on a result derived in a lecture on financial economics. In line with *Ross (1976)*, *Breeden and Litzenberger (1978)*, showed how to approximately determine the price of derivatives with payoff structures that take the form of a continuous function of their underlying asset's price. This is done by 'digitizing' the payoff function using  intervalls of arbitrary length with constant payoffs and pricing these intervalls, by option-based replication. The section "The Ross–Breeden–Litzenberger result" in *Martin (2018)* provides a more rigorous summary and visual intuition of this idea. </br>

Applying this discrete digitization process allows to price a wide range payoff claims that take the form of continuous functions of an underlying asset's price at a fixed point in time.
As described in the literature mentioned above, the price for the digital approximated payoff-structure can be found by applying:
$\sum_i^{\infty}{g(K_i)^*call''_{t,T}(K_i)}*\Delta K$,
where $g(K_i)$ is the of a generic derivative that would be payed out, if the price of the underlying asset ends up at $K_i$. $K_i$ is the midpoint of the $i$-th block, $call''_{t,T}(K_i)$ is the second derivative of a call option with a strike price at $K_i$ and $\Delta K = K_{i+1} - K_i$ is the (uniform) width of each block.

This project provides a simple application of this concept: it prices a claim that takes a discrete, textual payoff. For that, it aggregates all payout levels for each $K_i$ and prices the resulting payoff using the formula above.

**Practical implications** </br>
As of today, I have found neither any particularily useful nor financially reasonable application for this tool, except for constructing and pricing textual portfolios as a (personal, albeit admittedly eccentric) gift for special occasions.

## Usage

A simple example to demonstrate the basic functionality can be found in the *demo.ipynb* notebook.

### Importing custom underlying assets

While the project includes some exemplary data for S&P 500 calls, it is possible to work with any preferred underlying asset with sufficiently liquid option markets.

**The CallPriceTemplate** </br>
To import custom call price data, simply insert strike and associated market prices for an arbitrary asset into the sheet 'Template' of the file *resources/CallPriceTemplate.xlsx*. Don't forget to update the information in the sheet 'Meta' to keep everything consistent. 

## Settings and Options

There are two main objects in this project. This section will describe their parameters and default values. 

### WorDerivative

This is the derivative described above. 

**Settings/properties include:**

- .word - The word that was used to generate the derivative, i.e. the shape of the payoff. 
- .mid_price - The underlying price-midpoint of the word as displayed in the underlying price-payoff chart, i.e. the $K_i$ around which the word will be centered.
- .price_range - The "width" of the payoff word across the underlying's prices.
- .letter_scaling - The heigth of the payoff, used to scale the payoff itself.
- .price - Will contain the price of the derivative as approximated by the formula above. 
- .call_pricing_degree_of_approx - The polynomial degree used to approximate of the call price function from the provided sample prices.
- .call_pricing_strike_thresholds - Limits to the range of strike prices for which provided sample calls will be considered for approximation (useful to avoid outliers etc).
  
**Public methods include:**

- .plot_word_matrix() - Returns a figure of how the inserted word will be translated to payoff "markers".
- .plot_payoff(x_boundaries, aggregated) - Returns a figure that shows the (aggregated) payoffs across different prices for the underlying. This effectively communicates the main point of the whole WorDerivative. x_boundaries can be used to adjust the displayed range of underlying prices.

### Call

This will be contained within a given WorDerivative to provide the associated pricing background for reference. It contains all relevant data regarding the provided call options.

**Settings/properties include:**

- .data_path - Contains the path to the sample call price data.
- .strike_thresholds - Contains the range of calls that were included to approximate the call-price function.
- meta - Contains meta information about the sample call prices as listed in the template.
- .degree_of_approx - Contains the polynomial degree used for call price approximations.
- .approx_parameters - Displays the fitted polynomial coefficients.

**Public methods include:**

- .price(strike) - Returns the price of a call at the given strike price, using the internal approximation form sample data.
- .price_second_derivative(strike) - Returns the second derivative of the internal sample data approximation of the call price, evaluated at the given strike price.
- .plot_price_chart(range) - Displays the provided call prices and their approximation.

### Constants

- MARKER_WIDTH - Determines the "block width $\Delta K$ in the formula above.
- LETTER_MATRIX_SIZE - Related to the resolution of the schematic letter representation as provided in the *Letter_Reference.xlsx* file. Given in length units.
- LETTER SPACING - Determines the number of length units that will be inserted in between two letters.
- Densities - The number of points used to display the associated function in one of the plots.

## Current Limitations and Future Versions

- While the current version only allows for the pricing of single words in capital letters, an extension to lowercase letters, spaces, and multiline text is straightforward. When extending to the full unicode set, a different method for translating string inputs to their matrix form might be worthwhile.
- Extensions could further include the pricing of any arbitrary 2D user input (e.g. directly, by requesting the matrix representation, or by pre-processing a given sketch on a chart of the underlying asset's price).
- Following the approach in Martin (2018), the tool could also be extended to work with multiple underlying assets and 3D (text-) objects.

## Current ToDos

- Implement error handling and input validation
  - Ensure that call price approximation is convex in a relevant range (or at least warn the user if this is violated)
  - Ensure that there are no spaces or non-letter characters in word inputs
    - Ensure that word width is within acceptable range (larger than 0 and if strict: within call pricing thresholds)
    - ... (-> Remainder, see notes)
- Optimize letter payoff plot (most of the delay within 'plt.scatter' call)
- Implement an option to reach call prices for out-of-the-money calls via observed put prices and put-call-parity.
- Implement a method to price calls using Black-Scholes as a benchmark or to use underlyings without active option markets.

## External Libraries

- Numpy
- Pandas
- Matplotlib

## Sources

- Breeden, D. T. and Litzenberger, R. H. (1978). Prices of state-contingent claims implicit in option prices. Journal of Business, 51(4):621–651.
- Martin, I. (2018) Options and the Gamma Knife, Journal of Portfolio Management, 44:6:47‒55
- Ross, S. A. (1976). Options and efficiency. Quarterly Journal of Economics, 90(1):75–89.