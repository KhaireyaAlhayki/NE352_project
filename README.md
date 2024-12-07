# News API - Client GUI and Server python scripts

## Project Discription
This project requires two sides, the client which will send requests, and the server which will send responses to the client to be displayed then. Our client script utilizes GUI to display the requirements which are the main menu, followed by sub-menus/ The client here will interact with the choices displayed. For retrieveing the news data, the server uses an API (using our API key) based on the user's choices. This is the website it retrieves from: https://newsapi.org/ 


**Group**: A15

**Course code**: ITNE352

**Section**: 1

**Semester**: First semester 2024-2025

**Student names & IDs:**
1. Name: Khaireya Husain Khamis Alhaiki          ID: 202208539
2. Name: Zainab Abbas Isa Hasan                  ID: 202207120

## Table of Contents:
1. Requirements
2. How to run the system
3. Explanation of client.py 
4. Explanation of server.py 
5. Additional concepts
6. Acknowledgments
7. Conclusion

## Requirements:
1. Ensure you have Python 3 installed (https://www.python.org/downloads/).
2. Clone this project or download the provided client and server scripts.
3. Use any editor to write and run the scripts like Visual Studio Code.
4. Open a terminal (like powershell) in the project directory to test the client and server scripts.
5. Most of the libraries used are pre-installed libraries, however additional libraries were installed like: requests.
    All you need to do is write the following commands in your terminal
    pip install requests
    


## How to run the system:
First, open any editor that works for python such as Visual Studio Code.
Then, run the server first (by typing python server.py in your terminal)
After running the client (by typing python client.py in your terminal) you can see the GUI is running and is asking for your username.

## The scripts
Here are the client.py and server.py scripts:

### client.py
(Explain here)

### server.py
The server accept requests from the connected clients (up to 3 clients can be connected to the server) and process them and reply with the correct response.

1. What the Server Does
- Connects with clients (up to 3 clients at once).
- Processes requests in a specific format.
- Uses the NewsAPI to retrieve news headlines or sources based on the request.
- Sends the response back to the client.
- Saves the response in a .json file for later use.

2. Important Python Packages Used
- socket: Handles the connection between the server and clients.
- threading: Lets the server talk to multiple clients at the same time by creating different threads for each.
- requests: Helps the server send requests to the NewsAPI to ask for news and get the results back.
- json: Handles saving and loading data in JSON format.
- pickle: Converts (serializes) Python objects into bytes and sends them to the client.

3. Main Functions

a. server_setup
- What it does: Sets up the server and listens for client connections.
- How it works:
* Opens the server at a specific IP and port which in this project are (127.0.0.1, 49999).
* Accepts new client connections.
* Creates a thread for each client so multiple clients can connect at the same time (maximum of three).
* Prints how many clients are connected.

b. handle_client
- What it does: Handles communication with one client.
- How it works:
* Receives the client’s request.
* Passes the request to the process_request function to figure out what the client needs.
* Sends the response back to the client after converting it to bytes using pickle.
* Saves the response to a JSON file using the save_to_json function.

c. process_request
- What it does: Understands and validates the client’s request.
- How it works:
- Breaks the request into different parts (e.g., request type, category, client name).
- Calls the correct function (like retrieve_headlines or retrieve_all_sources) to handle the request.
- Checks for errors like invalid formats or unsupported options.

d. retrieve_headlines
- What it does: Gets news headlines based on the client’s preferences such as country, or category.
- How it works:
* Creates a URL based on the client’s request (it add the request to the URL) and sends it to the NewsAPI.
* Limits the number of articles to 15 maximum headlines retrieved to keep responses short.
* Converts each article into a readable format using format_article.

e. format_article and format_source
- What they do: Turn raw news data into easy-to-read dictionaries.
- Why it’s useful: Makes the data easier to send, read, and save.

f. save_to_json
- What it does: Saves the response data to a .json file.
- How it works:
* Names the file using the client’s name, request type, and group ID.
* Writes the response into the file in a structured desired way.

##  Additional concepts


## Acknowledgments
Big thanks to Dr. Mohamed Almeer and our team for the support and collaboration, which made the successful completion of this project possible with smooth progress and significant outcomes.


## Conclusion
