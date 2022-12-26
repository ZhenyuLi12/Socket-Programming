# Socket-Programming
CMPT 371 - 2021

Create a simple web server with socket programming, and HTTP protocol.
At first, the web server only handle one HTTP request at a time based on the following messages for all relevant methods to the client:

Code -  Message

200	 -   OK

304	 -  Not Modified

400	 -  Bad request

404	 -  Not Found

408	 -  Request Timed Out

Then test it with text.html

Second, extend the web server to multi-threaded version to handle multiple requests simultaneously where each TCP connection requested is handled in a separate thread.
