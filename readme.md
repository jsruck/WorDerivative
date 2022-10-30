# WorDerivative
##### JSR | Oct-22
*How much would you pay for 'that'?*
Pricing textual derivative payoffs.

## Table of Contents
- Background and Concept
- Usage
- Settings and Options
- Libraries
- Current ToDos
- Sources

## Background and Concept
This tool is based on a result derived in a lecture on financial economics. In line with *Ross (1976)*, *Breeden and Litzenberger (1978)*, showed how to approximately determine the price of derivatives with payoff structures that take the form of a continuous function of their underlying asset's price. This is done by 'digitizing' the payoff function using  intervalls of arbitrary length with constant payoffs and pricing these intervalls, by replication using options. The section "The Ross–Breeden–Litzenberger result" in *Martin (2018)* provides a more rigorous summary and visual intuition of this idea

Applying the concept to the discrete digitization process allows to !!![any]
!!!formula
!!!

**Practical implications**
As of today, I have found neither any particularily useful nor financially reasonable application for this tool, except for constructing and pricing textual portfolios as a (personal, yet admittedly eccentric) gift for special occasions. 

## Usage
A demo of the core functionality, using a simple example, can be found in the *demo.ipynb* notebook. 
### Importing custom underlying assets
While the project includes some exemplary data for S&P 500 calls, it is possible to work with any preferred underlying asset with sufficiently liquid option markets. 
**The CallPriceTemplate**
To import custom call price data, simply insert strike and associated market prices for an arbitrary asset into the sheet 'Template' of the file *resources/CallPriceTemplate.xlsx*. Don't forget to update the information in the sheet 'Meta' to keep everything consistent. 

## Settings and Options
There are two main objects in this project. This section will describe their parameters and default values. 
### WorDerivative
This is !!!.
### Call
This will be included in a given WorDerivative as a background object and contain all relevant data on the provided call.
!!!
### Constants

## Current Limitations and Future Versions 
- While the current version only allows for the pricing of singular words in capital letters, an extension to lowercase letters, spaces, and multiline text is straightforward. When extending to the full unicode set, a different method for translating string inputs to their matrix form might be worthwhile.   
- Extensions could further include the pricing of any arbitrary 2D user input (e.g. directly, by requesting the matrix representation, or by pre-processing a given sketch on a chart of the underlying asset's price).
- Following the approach in Martin (2018), the tool could also be extended to work with multiple underlying assets and 3D (text-) objects.
## Current ToDos
- Implement error handling and input validation
  - No spaces non-letters in word-inputs
    - Ensure that word width is within acceptable range (larger than 0 and if strict: within call pricing thresholds)
    - ... (-> Remainder, see notes)
- Optimize letter payoff plot (most of the delay within 'plt.scatter' call)

## External Libraries
- Numpy
- Pandas
- Matplotlib

## Sources
- Breeden, D. T. and Litzenberger, R. H. (1978). Prices of state-contingent claims implicit in option prices. Journal of Business, 51(4):621–651.
- Martin, I. (2018) Options and the Gamma Knife, Journal of Portfolio Management, 44:6:47‒55
- Ross, S. A. (1976). Options and efficiency. Quarterly Journal of Economics, 90(1):75–89.