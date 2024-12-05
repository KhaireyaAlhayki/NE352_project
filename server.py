import socket
import threading
import requests
import json
# Function to handle client communication
def handle_client(socket_conn, client_address):    
    try:
        while True:
            # Receive message from the client
            message = socket_conn.recv(1024).decode('utf-8')
            if not message:
                break
                        
            # Process the request
            response = process_request(message)
            
            # Send the response back to the client
            socket_conn.send(response.encode('utf-8'))
    except ConnectionResetError:
        print("Connection Reset")
    finally:
        print("Client disconnected")
        socket_conn.close()

# check the client's request and send response
def process_request(request):
    parts = request.split('-')
    if len(parts) != 3:
        return "Invalid request format"
    request_type, option, key = parts
    if request_type == '1':  # Headlines
        return fetch_headlines(option, key)
    elif request_type == '2':  # Sources
        return fetch_sources(option, key)
    else:
        return "Invalid request type"
def fetch_headlines(option, key):
    #--> function get headlines related information from NewsAPI <--
    url = f"https://newsapi.org/v2/top-headlines?apiKey=4c4e729949bf494baeacabafe0d81b43"
    if option == '1':
        url += f"&q={key}" # search based on key
    elif option == '2':
        url += f"&category={key}"  # search based on category
    elif option == '3':
        url += f"&country={key}"  #search based on country
    else:
        return "Invalid option for headlines."
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return json.dumps(articles) if articles else "No articles found."
    except requests.exceptions.RequestException as error:
        return f"Error fetching headlines: {error}"
#--> function to get sources related information from NewsAPI <--    
def fetch_sources(option, key):
    url = f"https://newsapi.org/v2/sources?apiKey=4c4e729949bf494baeacabafe0d81b43"
    if option == '1':
        url += f"&category={key}"  # search based on category
    elif option == '2':
        url += f"&country={key}"  # earch based on country
    elif option == '3':
        url += f"&language={key}"  #earch based on language
    else:
        return "Invalid option for sources."
    try:
        response = requests.get(url)
        response.raise_for_status()
        sources = response.json().get('sources', [])
        return json.dumps(sources) if sources else "No sources found"
    except requests.exceptions.RequestException as error:
        return f"Error fetching sources: {error}"
# setting up the server
def server_setup(host='127.0.0.1', port=49999):
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind((host, port))
    s_sock.listen()
    print("Server started listening to connections")
    
    while True:
        socket_conn, client_address = s_sock.accept()
        print("Server accepted the connection..!")


        # create and start a new thread for the client
        client_thread = threading.Thread(target=handle_client, args=(socket_conn, client_address))
        client_thread.start()
        
        # number of active threads for the clients connected
        print(f"connection number: {threading.active_count() - 1}")

if __name__ == "__main__":
    server_setup()
