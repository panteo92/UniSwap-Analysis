# UniSwap P/L with Market Making Analysis

This is a numerical model used to calculate percentage P/L for a Market Maker in the UniSwap Exchange, including the effect of the exchange trading fees.
It performes an analysis to estimate what is the P/L of providing liquidity on Uniswap at an initial market price of $130 per ETH. The analysis assumes a MM who is providing a $100 of liquidity (50% as ETH and 50% as DAI) and calculates the P/L as the difference between the dollar value of the MM’s liquidity tokens after a certain amount of time and the dollar value of initial ETH/DAI without market making. To calculate the former, the model:

1. Estimates the final ETH and DAI pool sizes after a price movement using the constant product formula of Uniswap AMM.
2. Estimates the fees that are added to the liquidity pool due to the trading activity. These are simply 0.3% of the trading volume. The model assumes a uniform trading volume over the period of the price movement.
3. Calculate the MM share of the ETH/DAI liquidity pool based on the ratio of their liquidity tokens to the total number of liquidity tokens. For simplicity, it was assumed that the liquidity pool size didn’t change, by adding or removing liquidity, during the price move.
