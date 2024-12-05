import socket
import threading
import requests
import json

# our group Id defined to be used later
GROUP_ID = "A15"

# Function to handle client communication
def handle_client(socket_conn, client_address):    
    try:
        # welcoming message for each client
        username = socket_conn.recv(1024).decode('utf-8')
        socket_conn.send("Welcome to the server!".encode('utf-8'))
        
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
    
    # ensure the request has the right format to be processed
    if len(parts) != 3 and len(parts) != 4:
        return "Invalid request format"
    
    request_type, option, key = parts[:3]
    detail_index = int(parts[3]) if len(parts) == 4 else None
    
    print(f"Processing request - Type: {request_type}, Option: {option}, Key: {key}, Detail Index: {detail_index}")
    # Process the request based on type and option
    if request_type == '1':  # Headlines
        return retrieve_headlines("client_name", option, key, detail_index)
    elif request_type == '2':  # Sources
        return retrieve_sources("client_name", option, key, detail_index)
    else:
        return "Invalid request type."
    
 #--> function get headlines related information from NewsAPI <--   
def retrieve_headlines(client_name, option, key, detail_index):
    url = f"https://newsapi.org/v2/top-headlines?apiKey=4c4e729949bf494baeacabafe0d81b43"
    if option == '1':
        url += f"&q={key}"  # search based on key
    elif option == '2':
        url += f"&category={key}"  # search based on category
    elif option == '3':
        url += f"&country={key}"  # search based on country
    else:
        return "Invalid option for headlines."
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        
        # number of of headlines retrieved will not exceed 15 article.
        max_articles = articles[:15]
        
        # Save articles to JSON file
        if max_articles:
            save_to_json(max_articles, client_name, option)
            
            # If detail_index is provided, return details of the selected article
            if detail_index is not None and 0 <= detail_index < len(max_articles):
                return json.dumps(max_articles[detail_index], indent=4)
            
            return json.dumps(max_articles, indent=4)
        else:
            return "No articles found."
    except requests.exceptions.RequestException as error:

        return f"Error fetching headlines: {error}"
    
 #--> function to get sources related information from NewsAPI <--       
def retrieve_sources(client_name, option, key, detail_index):
    url = f"https://newsapi.org/v2/sources?apiKey=4c4e729949bf494baeacabafe0d81b43"
    if option == '1':
        url += f"&category={key}"  # search based on category
    elif option == '2':
        url += f"&country={key}"  # search based on country
    elif option == '3':
        url += f"&language={key}"  # search based on language
    else:
        return "Invalid option for sources"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        sources = response.json().get('sources', [])
        
        # number of of sources retrieved will not exceed 15 article.
        max_sources = sources[:15]
        
        # Save sources to JSON file
        if max_sources:
            save_to_json(max_sources, client_name, option)
            
            # If detail_index is provided, return details of the selected source
            if detail_index is not None and 0 <= detail_index < len(max_sources):
                return json.dumps(max_sources[detail_index], indent=4)
            
            return json.dumps(max_sources, indent=4)
        else:
            return "No sources found."
    except requests.exceptions.RequestException as error:
        return f"Error fetching sources: {error}"
    
 #function to save the data results to a JSON file in this way: <client_name>_<option>_<group_ID>.json
def save_to_json(data, client_name, option):
    filename = f"{client_name}_{option}_{GROUP_ID}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Setting up the server
def server_setup(host='127.0.0.1', port=49999):
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind((host, port))
    s_sock.listen()
    print("Server started listening to connections")
    
    while True:
        socket_conn, client_address = s_sock.accept()
        print(f"Server accepted connection from {client_address}")
        
        # Create and start a new thread for the client
        client_thread = threading.Thread(target=handle_client, args=(socket_conn, client_address))
        client_thread.start()
        
        # number of active threads for the clients connected
        print(f"connection number: {threading.active_count() - 1}")
if __name__ == "__main__":
    server_setup()
