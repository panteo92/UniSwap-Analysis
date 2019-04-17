# Written by Matteo Pandolfi, 17/04/2019
# Market Making P/L Analysis in UniSwap ETH/DAI market

import numpy as np
from numpy import zeros
import math
import matplotlib
import matplotlib.pyplot as plt

initial_committed_capital = 100
ETH_price_t0 = 130

# Source: https://etherscan.io/address/0x09cabec1ead1c0ba254b09efb3ee13841712be14
initial_ETH_pool_size = 5211
initial_DAI_pool_size = 710951

initial_pool_size = initial_DAI_pool_size + initial_ETH_pool_size * ETH_price_t0

UniSwap_constant_product = initial_ETH_pool_size * initial_DAI_pool_size
ownership_percentage = initial_committed_capital / initial_pool_size

# ETH_price = committed_DAI / committed_ETH
# initial_committed_capital = committed_DAI + committed_ETH * ETH price

committed_DAI_t0 = 0.5 * initial_committed_capital
committed_ETH_t0 = 0.5 * initial_committed_capital/ETH_price_t0

"""
Assuming a change of ETH price without any external change of the liquidity pool size
"""

price_change_ratio = np.arange(0.5, 1.5, 0.01)
trading_vol = np.linspace(10000, 10000000) # volume between 10k-10MM

MM_new_ETH_share = zeros((len(price_change_ratio), len(trading_vol)))
MM_new_DAI_share = zeros((len(price_change_ratio), len(trading_vol)))

PL = zeros((len(price_change_ratio), len(trading_vol)))

for i in range(len(price_change_ratio)):
    for j in range(len(trading_vol)):
        ETH_price_change_ratio = price_change_ratio[i]
        new_ETH_price = ETH_price_t0 * ETH_price_change_ratio

        trading_volume = trading_vol[j]
        trading_fees = 0.003 * trading_volume
        # Fees added to the pool assuming average price
#        avg_price_of_move = (ETH_price_t0 + new_ETH_price)/2  
#        ETH_added_to_pool = 0.5*trading_fees/avg_price_of_move
#        DAI_added_to_pool = 0.5*trading_fees

        # Fees added assuming uniform volume segments during the price move
        number_of_price_steps = 10
        fees_per_price = trading_fees / number_of_price_steps
        intermediate_price_steps = np.linspace(ETH_price_t0, new_ETH_price, num=number_of_price_steps) # assuming linear price increase
        ETH_added_to_pool = sum(0.5*fees_per_price/intermediate_price_steps)
        DAI_added_to_pool = 0.5*trading_fees

        DAI_pool_size = math.sqrt(UniSwap_constant_product * new_ETH_price) + DAI_added_to_pool
        ETH_pool_size = DAI_pool_size / new_ETH_price + ETH_added_to_pool

        Check = (DAI_pool_size*ETH_pool_size)/UniSwap_constant_product

        MM_new_ETH_share[i,j] = ownership_percentage * ETH_pool_size
        MM_new_DAI_share[i,j] = ownership_percentage * DAI_pool_size

        MM_new_position = MM_new_DAI_share[i,j] + MM_new_ETH_share[i,j] * new_ETH_price
        position_without_MM = committed_DAI_t0 + committed_ETH_t0 * new_ETH_price

        PL[i,j] = MM_new_position - position_without_MM



# print("PL: ",PL)
# print("trad_vol: ", trading_vol)
# print("price_change: ", price_change_ratio)
# print("initial_comm_cap: ", initial_committed_capital)

X = trading_vol/1000000
Y = (price_change_ratio-1)*100
data = PL/initial_committed_capital*100

def extents(f):
  delta = f[1] - f[0]
  return [f[0] - delta/2, f[-1] + delta/2]


plt.figure()
plt.imshow(data, aspect='auto', interpolation='none',
           extent=extents(X) + extents(Y), origin='lower')
plt.show()