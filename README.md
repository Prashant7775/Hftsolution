# Hftsolution Limit Order Book

Usage (All inputs will be prompted):
1. First create some Buy Listings and Sell Listings by giving intputs as:
l(for limit orders), 
s(for sell listing) / b(for buy listing), 
400(number of shares to buy or sell), 
11.38(price)
2. Now you can use m(for market orders), s / b , number of shares


You can also use functions instead of menu driven program it has following functions:
1. createMarketOrder( bORs,shares ) 
2. createLimitOrder( bORs,shares,price )
3. cancelOrder( bORs,shares,price )
4. showDetails( )

bORs takes "b" or "s" as input (b for buy / s for sell), shares takes integer as input (number of shares), prices takes float/integer as input
