import socket
import json
import pickle
import tkinter as tk
from tkinter import messagebox
#creat tab
root=tk.Tk()
root.geometry("500x400")
root.title("EchoNews")
#create label for username and entry
label = tk.Label(root, text="Enter your username:")
label.pack(padx=10,pady=10)
username=tk.Entry(root)
username.pack(padx=10)
#main menu label
main_m=tk.Label(root,text="MAIN MENU:")
main_m.pack(padx=20)
#create headlines menu
headlines_m=tk.Button(root,text="Search by Headlines" )
headlines_m.pack(padx=20,pady=20)
#create source menu
source_m=tk.Button(root,text="Search by sources")
source_m.pack(padx=20,pady=20)
#create Quit button
button=tk.Button(root, text="Quit App", command=quit)
button.pack(padx=20,pady=20)





root.mainloop()


parameter={}
categories={
    '1':'business',
    '2':'general',
    '3':'health',
    '4':'science',
    '5':'sports',
    '6':'technology'                        
}
countries={
    '1':'au',
    '2':'ca',
    '3':'jp',
    '4':'ae',
    '5':'sa',
    '6':'kr',
    '7':'us',
    '8':'ma'  
} 
languages={
    '1':'ar',
    '2':'en'
}

def main_menu():
    print("\nMain Menu: ")
    print("""
    1-Search headlines
    2-List of sources
    3-Quit
    """)
    choice = int(input("Enter the number of your choice: "))
    return choice

def headlines_menu(socket_c, client_name):
    print("\nHeadlines Menu:")
    print("""
    1-Search for keywords
    2-Search by category
    3-Search by country
    4-List all new headlines
    5-Back to the main menu
    """)

    option = int(input("Enter the number of your option: "))
    while option not in range(1, 6):
        print("Invalid option. Please choose a number between 1 and 5.")
        option = int(input("Enter the number of your option: "))

    request = ""  # Initialize request variable
    detail_index = None  # Initialize detail index

    if option == 1:  # Search for keywords
        keyword = input("Enter the keywords: ")
        request = f"1-1-{keyword}-{client_name}"
    elif option == 2:  # Search by category
        print("\nAvailable Categories:")
        for key, value in categories.items():
            print(f"{key}-{value}")
        category_o = input("Enter the category number (1-6): ")
        if category_o in categories:
            category = categories[category_o]
            request = f"1-2-{category}-{client_name}"
    elif option == 3:  # Search by country
        print("\nAvailable Countries:")
        for key, value in countries.items():
            print(f"{key}-{value}")
        country_o = input("Enter the country number (1-8): ")
        if country_o in countries:
            country = countries[country_o]
            request = f"1-3-{country}-{client_name}"
        else:
            print("Invalid country selection.")
            return
    elif option == 4:  # List all new headlines
        request = f"1-4--{client_name}"
    elif option == 5:  # Back to the main menu
        return

    print("Sending request:", request)
    socket_c.send(request.encode())

    response = receive_full_data(socket_c)  # Receive full response
    try:
        data_list = pickle.loads(response)  # Deserialize the binary data
        if data_list:
            print("\nHeadlines Received:")
            for idx, article in enumerate(data_list, 1):
                print(f"{idx}. {article}")
        else:
            print("No headlines found.")
    except Exception as e:
        print(f"Error deserializing response: {e}")

def sources_menu(socket_c, client_name):
    print("\nSources Menu:")
    print("""
    1-Search by category
    2-Search by country
    3-Search by language
    4-List all
    5-Back to the main menu
    """)
    option = int(input("Enter the number of your option:"))
    
    # Handle invalid options
    while option not in range(1, 6):
        print("Invalid option. Please choose a number between 1 and 5.")
        option = int(input("Enter the number of your option: "))

    request = ""  # Initialize request variable
    detail_index = None  # Initialize detail index

    if option == 1:
        print("""
        1-business
        2-general
        3-health
        4-science
        5-sports
        6-technology
        """)
        category_o = input("Enter the category number (1-6): ")
        if category_o in categories:
            category = categories[category_o]
            request = f"2-1-{category}-{client_name}"
    elif option == 2:
        print("""
        1-au
        2-ca
        3-jp
        4-ae
        5-sa
        6-kr
        7-us
        8-ma
        """)
        country_o = input("Enter the country number (1-8): ")
        if country_o in countries:
            country = countries[country_o]
            request = f"2-2-{country}-{client_name}"
    elif option == 3:
        print("""
        1-ar
        2-en 
        """)
        languages_o = input("Enter the language number (1-2): ")
        if languages_o in languages:
            language = languages[languages_o]
            request = f"2-3-{language}-{client_name}"
    elif option == 4:
        request = f"2-4--{client_name}"
    elif option == 5:
        return

    
    print("Sending request:", request)
    socket_c.send(request.encode())

    # Receive and process the server response
    try:
        response = receive_full_data(socket_c)
        data_list = pickle.loads(response)  # Deserialize the binary data
        if data_list:
            print("\nSources Received:")
            for idx, source in enumerate(data_list, 1):
                print(f"{idx}. {source}")
        else:
            print("No sources found.")
    except Exception as e:
        print(f"Error deserializing response: {e}")

def receive_full_data(socket_c):
    response = b""
    while True:
        data = socket_c.recv(4096)
        response += data
        if len(data) < 4096:
            break
    return response

def client():
    try:
        socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_c.connect(("127.0.0.1", 49999))
        print("Connected to the server.")
        
        client_name = input("Enter username: ")
        socket_c.send(client_name.encode())
        
        welcome_message = socket_c.recv(1024).decode('utf-8')
        print(welcome_message)

        while True:
            choice = main_menu()
            if choice == 1:
                headlines_menu(socket_c, client_name)
            elif choice == 2:
                sources_menu(socket_c, client_name)
            elif choice == 3:
                print("Quitting...")
                break
            else:
                print("Invalid option. Try again.")
        socket_c.close()

    # Handle errors
    except ConnectionResetError:
        print("Connection lost.")
    except ConnectionRefusedError:
        print("Failed to connect to the server.")
    except Exception as error_msg:
        print(f"An error occurred: {error_msg}")

if __name__ == "__main__":
    client()