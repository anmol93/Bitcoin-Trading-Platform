# Bitcoin-Trading-Platform
This program generates bitcoin trading quotes and calculates best trading prices for bitcoins based on bids and asks from users all around the world. To test-run the program quickly, I have used top 50 buys and top 50 asks.


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Instructions to run the code:

1. Download the entire folder at a location in the computer.

2. Install python 3 and Flask framework 

3. Execute the file flask_web_server.py to start the web server.

4. While the server is running, go to http://127.0.0.1:5000/. Scroll down to access the form to enter buy/sell action, base currency, quote currency, amount and click Submit. 

5. The output is computed through function imported from gdax.py and the result is displayed.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Description of the code-

1. python 3 and flask framework has been used to code the web service. The modules imported are Flask, requests, render_template and json.

2. I have used flask to create a web server. The server receives POST requests from a webpage with variables action, base currency, quote currency and amount. Another service I created is the function gdax_web_service inside the file gdax.py. It takes an object called "input_object" as input which provides the values - action, base_currency, quote_currency and amount. The gdax_web_service function checks if the base and quote currency pair exists in the gdax order book and calls function get_quote if it does, calls get_quote2 if it exist inversely or returns object containing the error message if the currencies cannot be traded. Functions get_quote and get_quote2 call functions buyorsell and buyorsell2 respectively. Functions buyorsell and buyorsell2 compute the aggregated orders to provide the the best value and return them to get_quote and get_quote2 respectively, which in turn return them back to gdax_web_service.

3. Instead of creating a class of these functions, I decided to create a separate file for storing the functions called gdax.py. To provide an input to this service, the function gdax_web_service is imported in the other python file called service_input.py

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Extra Comments:

1. I couldn’t use the values of  base_min_size and base_max_size from GDAX API(https://api.gdax.com/products) to limit the values of amount of base currency, because the order book I was asked to use for my web service had only 50 bids and 50 asks as a result of using a level 2 query parameter to fetch aggregated order information. And so in cases where the demand of base currency is more than available by aggregating those 50 orders at that moment, the web service returns an error message suggesting that the trade  cannot be possible and gives the maximum value of amount of base currency that can be bought. 

2. If the web_service receives any Input for which a trade cannot be executed, an error message is returned with the reason of failure.  

3. I definitely tried to be as elaborate as possible, by adding comments. This was done to make the code more understandable, ofcourse.
