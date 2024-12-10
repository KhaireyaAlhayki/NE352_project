# News API - Client GUI and Server python scripts

## Project Discription
This project requires two sides, the client which will send requests, and the server which will send responses to the client to be displayed then. Our client script utilizes GUI to display the requirements which are the main menu, followed by sub-menus/ The client here will interact with the choices displayed. For retrieveing the news data, the server uses an API (using our API key) based on the user's choices. This is the website it retrieves from: https://newsapi.org/ 


**Group**: A15

**Course code**: ITNE352

**Section**: 1

**Semester**: First semester 2024-2025

**Student names & IDs:**
1. Name: Khaireya Husain Khamis Alhaiki          ID: 202208539
2. Name: Zainab Abbas Isa Jasim Hasan            ID: 202207120

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
4. Open a terminal (such as powershell or any other terminal) in the project directory to test the client and server scripts.
5. Most of the libraries used are pre-installed libraries, however additional libraries were installed like: requests.
    All you need to do is write the following commands in your terminal
    pip install requests
    


## How to run the system:
First, open any editor that works for python such as Visual Studio Code.
Then, run the server first (by typing python server.py in your terminal)
After that, run the client (by typing python client.py in your terminal) so you can see the GUI running and is asking for your username.

## The scripts
Here are the client.py and server.py scripts:

### client.py
The client establish a connection with server, send requests for specific data, and remain connected until the user decides to quit.

1. What the Client Does
- Requests to the server
- Display the main menu
- Enables users to interactively explore news headlines and sources menu
- Display the responses

2. Important Python Packages Used
- socket: Handles the connection between the server and clients.
- pickle: Deserialize Data Received from the Server
- tkinter: Python's standard library for creating graphical user interfaces (GUIs) 
  * as tk: for make the code shorter and easier to read
  * messagebox : from the tkinter library will import messagebox to use a message box for displaying alerts

3. Main Functions
First we have class for encapsulates logic in a class for better organization which called main that content the most of the functions such as :
a. __init__ 
- What it does: Sets up the application window, Initializes the networking variables for later use and Displays the login screen 
- How it works:
* Accepts a root Parameter represents the main window object
* stores the root window in the instance so it can be accessed throughout the class
* Sets the title, the size, and changes the background color
* Initializes Socket and User Variables
* Initializes the Login Screen by call create_login_screen function

b. connect_to_server
- What it does: stablishing a connection between the client and a server using a socket
- How it works:
* Create a Socket Object that use IPv4 addressing and TCP connection
* Connect to the Server 
* Confirmation on Success by printing message
* Handle the error by pop a messagebox 
* application then terminates 

c. create_login_screen
- What it does:setting up the initial login screen of the GUI application
- How it works:
* Clears any existing UI elements from the screen by call clear_screen function
* Displays a welcome message at the top of the login screen
* Displays the prompt asking the user to enter their username
* Creates an input field where the user can type their username
* Displays a button labeled "Submit" to allow the user to submit their username after entering it and will call handle_login function to deal with the username

d. handle_login
- What it does: Send the username to the server and get a welcome message.
- How it works:
* Get and Validate Username so will retrieves the text entered in the username input field and remove the spaces
* Checks if the username field is not empty
* Connect to the Server by Calls the connect_to_server function to establish a connection with the server
* Sends the entered username to the server using the socket connection and converts the string to bytes
* Receive the Welcome Message by Waits to receive data from the server then converts message from bytes to string
* Displays a popup message box with server response
* Transition to Main Menu by call create_main_menu function
* Warns the user with a popup message if there no username

e. create_main_menu
- What it does: Create the main menu screen and allows the user to choose different actions
- How it works:
* Clears any existing UI elements from the screen
* Displays a title at the top of the menu
* Create a search Headlines Button and call headlines_menu function for display the option of Headlines
* Create a search Sources Button and call sources_menu function for display the option of Sources
* Create Quit Button 

f. headlines_menu
- What it does: Create the headlines menu
- How it works:
* Clears any existing UI elements from the screen 
* Displays the menu's title
* Create search by keyword Button that call input_prompt function to cheack the keyword
* Create Search by Category Button that call select_from_list function 
* Create Search by Country Button that call select_from_list function
* Create List All Headlines Button that call send_request function
* Create Back to Main Menu Button that call create_main_menu

g. sources_menu
- What it does: creating a menu screen where users can search for news sources
- How it works: 
* Clears any existing UI elements from the screen
* Displays the Sources Menu title.
* Create Search by Category button that called select_from_list to display a list of categories 
* Create Search by Country button that called select_from_list to display a list of countries 
* Create Search by language button that called select_from_list to display a list of  Languages 
* Create List All Sources button that called send_request to Sends a request to the server to retrieve and display all available news sources 
* Create Back to the menu button called create_main_menu to display main menu 

h. input_prompt
- What it does: creates a screen for users to input text 
- How it works: 
* Clears any existing UI elements from the screen
* Display the Prompt Label text 
* Creates a text input field for user entry
* Create Submit Button that called send_request function to send request to the server 
* Create Back Button that called headlines_menu to display headlines menu

i. select_from_list
- What it does: generates a selection screen where users can choose an option from a list
- How it works: 
* Clears all existing widgets
* Displays a title for the selection screen.
* Iterates over the options dictionary to create buttons for each choice. After clicking the button it will  calls send_request function to send request to the server
* Create Back to the menu button called create_main_menu function to display main menu

j. send_request
- What it does: communicates with the server to send a user request, receive its response, and process it 
- How it works:  
* Constructing the Request by indicate the type of choice, the name of the option and associated the username 
* Print “Sending request”
* Encodes the constructed request as bytes and sends it through the socket connection
* Receiving the Response from the server by calling receive_full_data function which ensure complete response 
* Processing the Response by using pickle.loads which decodes the response into a Python object list
* Hadling request base on request type if its start with 1 call display_headlines function and if start with 2 will call display_sources function and both will display the results
* Catches and displays any errors that occur during response processing

k. display_headlines
- What it does: show a list of news headlines received from the server
- How it works:
* Clears all existing widgets
* Display headlines received 
* handling empty results by display message, and a button to return to the main menu
* Displaying the Headlines in scrollable text box by use tk.Text
* Iterating through headlines and if the article is a dictionary,extracts details (Name, Author, Title) and formats them and if it’s plain text,displays it as-is
* Prompt for details by Displays a label and input box for users to specify the headline numbers 
* Create a view details button that calls the display_detailed_headlines function 
* Create Back to the menu button called create_main_menu to display main menu 

l. display_detailed_headlines
- What it does: display detailed information about selected headlines
- How it works:
* Converts the user input (comma-separated indices) into a list of integers and Adjusts for zero-based indexing by subtracting 1 from each value
* Error handling by display error message
* Clears all existing widgets
* Displays a title and creates a Text widget to show the detailed information
* For valid indices: Fetches and displays details from the headline dictionary using get() and formats date and time from the 'Published At' field,if available and Separates entries with a horizontal line
* For invalid indices: Adds a message indicating that the index is out of range
* Create Back to the menu button called create_main_menu to display main menu 

m. display_sources 
- What it does: displays a list of sources received from the server
- How it works:
* Clears all existing widgets
* Display sources received 
* handling empty results by display message, and a button to return to the main menu
* Displaying the sources in scrollable text box by use tk.Text
* Iterating through sources and if the article is a dictionary,extracts (Name) and formats it and if it’s plain text,displays it as-is
* Prompt for details by Displays a label and input box for users to specify the sources numbers 
* Create a view details button that calls the display_detailed_sources function 
* Create Back to the menu button called create_main_menu to display main menu 

n. display_detailed_sources
- What it does: display detailed information about selected sources
- How it works: 
* Converts the user input (comma-separated indices) into a list of integers and Adjusts for zero-based indexing by subtracting 1 from each value
* Error handling by display error message
* Clears all existing widgets
* Displays a title and creates a Text widget to show the detailed information
* For valid indices: Fetches and displays details from the sources dictionary using get()
* For invalid indices: Adds a message indicating that the index is out of range
* Create Back to the menu button called create_main_menu to display main menu

o. clear_screen
- What it does: Clear the screen for the next UI interaction
- How it works: 
* Retrieve all widgets as list by root.winfo_children() currently attached to the root window
* For each widget in the list, remove it from the window by destroy()

receive_full_data Function it's outside the class, it becomes clearer that this function is a helper and not an integral part of the class's responsibilities. 
- What it does: handle all the receiving data from the server
- How it works:
* Initialize an empty bytes object to accumulate the data
* Receive up to 4096 bytes from the server
* Append the received chunk to the response
* Break if less data is received than the buffer size
* Return the complete response

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
- What it does: Handles communication with each (one) client.
- How it works:
* Receives the client’s request.
* Passes the request to the process_request function to figure out what the client needs.
* Sends the response back to the client after converting it to bytes using pickle.
* Saves the response to a JSON file using the save_to_json function.

c. process_request
- What it does: Understands and validates the client’s request.
- How it works:
- Breaks the request into different parts such as request type, category, and client name.
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
- Why it is useful: Makes the data easier to send, read, and save.

f. save_to_json
- What it does: Saves the response data to a .json file.
- How it works:
* Names the file using the client’s name, request type, and group ID.
* Writes the response into the file in a structured desired way.

##  Additional concepts
* GUI:
- The project allows users to interact with a news server through a Graphical User Interface (GUI) that created using the Tkinter library.By offering a simple and engaging method of accessing news headlines and sources.
- The original project relied on a command-line interface, which can be less engaging and user-friendly.The GUI adds: Buttons, labels, and input fields which easy to use
- The Core Components of the GUI:
1. Login Screen
2. Main Menu
3. Headlines Menu
4. Sources Menu
5. Detailed Views
- The GUI sends requests to the server by using :
* Input fields
* Buttons 
- Server responses are processed and displayed in text boxes.
- For future Improvements:
* To improve the application's visual attractiveness, add unique themes.
* Enhanced adaptability to various screen sizes.

## Acknowledgments
Big thanks to Dr. Mohamed Almeer and our team for the support and collaboration, which made the successful completion of this project possible with smooth progress and significant outcomes.


## Conclusion
- By completing this project, we improved our understanding of programming and networking concepts in Python. We learned a lot by adding client-server communication and using external APIs. Moreover, we added a GUI to make the project look better and easier to use. With our team's support and encouragement, we overcame the challenges we faced along the way. Overall, we are happy with the result and grateful for everything we learned during this project.
