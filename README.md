### Purpose:
The code is a script for an automated trading strategy using the Interactive Brokers (IB) API. The strategy involves trading cryptocurrencies (Bitcoin and Ethereum) based on a simple moving average (SMA) crossover strategy and incorporates elements like market orders, stop orders, and trailing stops.

### Components:

1. **IB Connection:**
   - Establishes a connection to the Interactive Brokers API.

2. **Ticker Initialization:**
   - Initializes a list of cryptocurrency tickers (BTC and ETH) and sets an initial capital amount.

3. **Contract Initialization:**
   - Creates contract objects for each cryptocurrency using the IB API.

4. **Data Retrieval:**
   - Defines functions for fetching real-time stock prices and historical data for a specified duration.

5. **Trading Functions:**
   - `trade_buy_stocks` and `trade_sell_stocks` functions place market orders and corresponding stop loss orders.

6. **Trailing Stop Functions:**
   - `trail_buy_stock` and `trail_sell_stock` functions modify stop orders based on a trailing condition.

7. **Strategy Function:**
   - The `strategy` function implements a simple SMA crossover strategy to determine whether to buy, sell, or do nothing.

8. **Main Function:**
   - Retrieves open orders and positions using the IB API.
   - Iterates through each ticker and executes the strategy accordingly.
   - Includes logic to handle different scenarios like having no positions, having positions, or having open orders.

9. **Time Management:**
   - Sets a start and end time for running the strategy during the day.
   - Uses a loop to wait until the start time is reached.
   - Continuously runs the main function within a specified time frame.

### Execution Flow:

1. **Initialization:**
   - Establishes a connection to the IB API.
   - Initializes tickers and contracts.

2. **Main Loop:**
   - Waits until the specified start time.

3. **Trading Loop:**
   - Runs the main trading logic repeatedly until the specified end time.
   - Retrieves real-time data, checks trading conditions, and executes orders accordingly.

4. **Time Management:**
   - Handles waiting for the start time and continuously runs the strategy until the end time.

### Important Points for Readme.md:

1. **Dependencies:**
   - Specify the libraries and modules required for the script to run, such as `ib_insync`, `pandas_ta`, and `pandas`.

2. **Interactive Brokers API:**
   - Mention that the script relies on the Interactive Brokers API for real-time data and order execution.

3. **Configuration:**
   - Users need to configure their IB API connection parameters.

4. **Risk Warning:**
   - Include a disclaimer about the risks involved in automated trading and the importance of understanding and testing the strategy thoroughly.

5. **Time Constraints:**
   - Highlight that the script is designed to run during specific time intervals defined by `start_time` and `end_time`.

6. **Strategy Overview:**
   - Provide a brief overview of the trading strategy employed in the script, such as the SMA crossover strategy and the use of stop and trailing stop orders.

7. **Usage Instructions:**
   - Explain how users can customize the script, modify tickers, adjust parameters, and run the script on their own systems.

8. **License:**
   - Specify the license under which the code is shared.

Make sure to keep your readme clear, concise, and user-friendly. Users should be able to understand the purpose of the script, how to use it, and any important considerations or customization options.
