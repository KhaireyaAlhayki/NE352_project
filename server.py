import socket
import threading
import requests
import json
import pickle

# our group ID defined to be used later
GROUP_ID = "A15"

# Function to handle client communication
def handle_client(socket_conn, client_address):    
    try:
        # Welcoming message for each client
        username = socket_conn.recv(1024).decode('utf-8')
        socket_conn.send("Welcome to the server!".encode('utf-8'))
        
        while True:
            # Receive message from the client
            message = socket_conn.recv(1024).decode('utf-8')
            if not message:
                break
            
            # Process the request
            response, client_name, option = process_request(message)
            
            # Save the response to a JSON file
            if client_name and option:
                save_to_json(response, client_name, option)
            
            # Serialize the response and send it back to the client
            serialized_response = pickle.dumps(response)
            print(f"Sending {len(serialized_response)} bytes of data.")
            socket_conn.sendall(serialized_response)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        print("Client disconnected")
        socket_conn.close()

def process_request(request):
  
    parts = request.split('-')
    
    if len(parts) < 4:
        return [["Invalid request format"]], None, None

    request_type, option, key, client_name = parts[:4]
    detail_index = int(parts[4]) if len(parts) == 5 else None

    # Debugging
    #print(f"Received request: {request_type}-{option}-{key}-{client_name} with detail_index {detail_index}")

    # Check what the client wants (headlines or sources) and call the right function
    if request_type == '1':  # Headlines
        return retrieve_headlines(option, key, detail_index), client_name, option
    elif request_type == '2':  # Sources
        if key == "":  # Handle the "List all" case (when key is empty)
            return retrieve_all_sources(detail_index), client_name, option
        elif option == '1':  # Category
            return retrieve_sources_by_category(key, detail_index), client_name, option
        elif option == '2':  # Country
            return retrieve_sources_by_country(key, detail_index), client_name, option
        elif option == '3':  # Language
            return retrieve_sources_by_language(key, detail_index), client_name, option
        else:
            return [["Invalid option for sources"]], None, None
    else:
        return [["Invalid request type"]], None, None
    
    
 # This function gets the top headlines based on the client’s request
def retrieve_headlines(option, key, detail_index):
    url = "https://newsapi.org/v2/top-headlines?apiKey=4c4e729949bf494baeacabafe0d81b43"
    
    if option == '1':  # Search for keywords
        url += f"&q={key}"
    elif option == '2':  # Search by category
        url += f"&category={key}"
    elif option == '3':  # Search by country
        valid_countries = ['au', 'ca', 'jp', 'ae', 'sa', 'kr', 'us', 'ma']
        if key not in valid_countries:
            return [["Invalid country code. Valid options: " + ", ".join(valid_countries)]]
        url += f"&country={key}"
    elif option == '4':  # List all headlines
        # Set a default country to avoid API errors (e.g., US)
        url += "&country=us"
    else:
        return [["Invalid option for headlines"]]

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        #number of of articles retrieved will not exceed 15 article.
        articles = response.json().get('articles', [])[:15]  

        if not articles:
            return [["No headlines found."]]

        if detail_index is not None:
            if 0 <= detail_index < len(articles):
                return [format_article(articles[detail_index])]  
            else:
                return [["Detail index out of range"]]

        return [format_article(article) for article in articles]  
    except requests.exceptions.HTTPError as http_err:
        return [[f"Error fetching headlines: {http_err}"]]
    except Exception as e:
        return [[f"Error fetching headlines: {e}"]]

#Retrieves news sources filtered by category.
def retrieve_sources_by_category(category, detail_index):
    url = f"https://newsapi.org/v2/sources?apiKey=4c4e729949bf494baeacabafe0d81b43"
    
    valid_categories = ['business', 'general', 'health', 'science', 'sports', 'technology']
    if category not in valid_categories:
        return [["Invalid category"]]

    url += f"&category={category}"
    return get_sources_from_url(url, detail_index)

#Retrieves news sources filtered by country
def retrieve_sources_by_country(country, detail_index):
    url = f"https://newsapi.org/v2/sources?apiKey=4c4e729949bf494baeacabafe0d81b43"
    
    valid_countries = ['au', 'ca', 'jp', 'ae', 'sa', 'kr', 'us', 'ma']
    if country not in valid_countries:
        return [["Invalid country code"]]

    url += f"&country={country}"
    return get_sources_from_url(url, detail_index)

#Retrieves news sources filtered by language 
def retrieve_sources_by_language(language, detail_index):
    url = f"https://newsapi.org/v2/sources?apiKey=4c4e729949bf494baeacabafe0d81b43"
    
    valid_languages = ['ar', 'en']
    if language not in valid_languages:
        return [["Invalid language code"]]

    url += f"&language={language}"
    return get_sources_from_url(url, detail_index)

 #Fetches and formats news sources from the given URL
def get_sources_from_url(url, detail_index):
    try:
        response = requests.get(url)
        response.raise_for_status()
        #[:15]: number of of sourcses retrieved will not exceed 15 article.
        sources = response.json().get('sources', [])[:15]  

        if not sources:
            return [["No sources found."]]
        
        if detail_index is not None:
            if 0 <= detail_index < len(sources):
                return [format_source(sources[detail_index])]
            else:
                return [["Detail index out of range"]]

        return [format_source(source) for source in sources]
    except Exception as e:
        return [[f"Error fetching sources: {e}"]]

#Retrieves all available news sources from the API   
def retrieve_all_sources(detail_index):
    url = f"https://newsapi.org/v2/sources?apiKey=4c4e729949bf494baeacabafe0d81b43"
    return get_sources_from_url(url, detail_index)

# Formats sources into a structured dictionary.
def format_source(source):
    return {
        "Name": source.get("name", "N/A"),
        "Description": source.get("description", "N/A"),
        "URL": source.get("url", "N/A"),
        "Category": source.get("category", "N/A"),
        "Language": source.get("language", "N/A"),
        "Country": source.get("country", "N/A")
    }

#Formats headlines into a structured dictionary.
def format_article(article):
    return {
        "Name": article.get("source", {}).get("name", "N/A"),
        "Author": article.get("author", "N/A"),
        "Title": article.get("title", "N/A"),
        "URL": article.get("url", "N/A"),
        "Description": article.get("description", "N/A"),
        "Published At": article.get("publishedAt", "N/A")
    }

# Function to save the response into a JSON file
def save_to_json(data, client_name, option):
    filename = f"{client_name}_{option}_{GROUP_ID}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

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
        
        # Number of active threads for the clients connected
        print(f"Connection number: {threading.active_count() - 1}")

if __name__ == "__main__":
    server_setup()