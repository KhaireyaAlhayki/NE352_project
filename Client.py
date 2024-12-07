import socket
import json
import pickle
import tkinter as tk
import customtkinter as ctk

# Global UI elements
user_entry = None
send_button = None
scroll_frame = None
scroll_active = False
displayed_labels = []

def get_text():
    '''take the text input from user'''
    global user_input
    user_input = user_entry.get()
    clear_screen()
    root.quit()

def setup_input():
    '''add entry to enter the choice and button to send the text'''
    global user_entry, send_button
    user_entry = ctk.CTkEntry(
        root,
        placeholder_text="Type here...",
        width=400,
        height=50,
        fg_color="white",
        text_color="black",
        font=("Arial", 16),
    )
    user_entry.pack(anchor=tk.CENTER, pady=10)

    send_button = ctk.CTkButton(
        root,
        text="Submit",
        fg_color="white",
        text_color="black",
        command=get_text,
    )
    send_button.pack(anchor=tk.CENTER, pady=10)
    root.mainloop()

def show_message(message, padding=(10, 10)):
    '''Displays messages on the screen'''
    if not scroll_active:
        label = tk.Label(root, text=message, bg="#E8E8E8", font=("Arial", 14))
        label.pack(pady=padding)
        displayed_labels.append(label)
    else:
        create_scrollable_area(message)

def create_scrollable_area(content):
    ''' create a frame inside it a textbox '''
    global scroll_frame
    scroll_frame = ctk.CTkFrame(root, width=800, height=300)
    scroll_frame.pack(pady=10)
    text_box = ctk.CTkTextbox(
        scroll_frame,
        wrap=tk.WORD,
        font=("Arial", 14),
        fg_color="white",
        text_color="black",
    )
    text_box.insert(tk.END, content)
    text_box.configure(state=tk.DISABLED)
    text_box.pack(fill=tk.BOTH, expand=True)

def clear_screen():
    '''Clear the screen for the next UI interaction'''
    global displayed_labels, user_entry, send_button, scroll_frame
    for label in displayed_labels:
        label.destroy()
    displayed_labels.clear()
    user_entry.destroy()
    send_button.destroy()
    if scroll_active:
       scroll_frame.destroy()

def main():
    '''Main application '''
    try:
        global root, scroll_active

        # Initialize the GUI
        root = tk.Tk()
        root.geometry("800x600")
        root.configure(background="#E8E8E8")
        root.title("News Application")

        # Establish connection to the server
        HOST= "127.0.0.1"
        PORT= 49999
        socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        show_message("Welcome to the News Application", padding=(150, 20))
        show_message("Please enter your username:")
        setup_input()
        username = user_input

        try:
            socket_c.connect((HOST, PORT))
            socket_c.send(username.encode('utf-8'))
            
        # Handle the error 
        except:
            show_message("Unable to connect to the server. Please try again later.")
            root.update()
        
        # The types
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

        # Main menu loop
        while True:
            clear_screen()
            show_message("Main Menu", padding=(20, 10))
            show_message("""
            1-Search headlines
            2-List of sources
            3-Quit
            """)
            setup_input()
            user_choice = user_input

            # Search Headlines
            if user_choice == "1":  
                scroll_active = False
                while True:
                    clear_screen()
                    show_message("Headline Menu", padding=(20, 10))
                    show_message("""
                    1-Search for keywords
                    2-Search by category
                    3-Search by country
                    4-List all new headlines
                    5-Back to the main menu
                    """)
                    setup_input()
                    choice = user_input

                    if choice=='1':
                        show_message("Enter a keyword: ")
                        show_message("enter 0 to go back in menu")
                        setup_input()
                        option=user_input
                        if option=='0':
                            break
                    elif choice=='2':
                        while True:
                            show_message("Enter a category: ")
                            show_message("""
                                1-business
                                2-general
                                3-health
                                4-science
                                5-sports
                                6-technology
                                """)
                            show_message("enter 0 to go back in menu")
                            setup_input()
                            option=user_input
                            if option=='0' or option in categories:
                                break
                            else:
                                show_message("no such category...try again")
                    elif choice=='3':
                        while True:
                            show_message("Enter a country: ")
                            show_message("""
                                1-au
                                2-ca
                                3-jp
                                4-ae
                                5-sa
                                6-kr
                                7-us
                                8-ma
                                """)
                            show_message("enter 0 to go back in menu")
                            setup_input()
                            option=user_input
                            if option=='0' or option in countries:
                                break
                            else:
                                show_message("no such country...try again")
                    elif choice=='4':
                        pass
                    
                    elif choice == "5":
                        break
                    else:
                        show_message("Invalid choice. Please try again.", padding=(5, 5))

        socket_c.close()
        root.quit()
    except Exception as e:
        print("An error occurred:", str(e))


# Run the program
if __name__ == "__main__":
    main()






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
                # Display each headline with names of details
                source_name = article.get('Name', 'Unknown Source')
                author = article.get('Author', 'Unknown Author')
                title = article.get('Title', 'No Title')
                print(f"{idx}. Author: {author} | Title: {title} | (Source: {source_name})")

             # Allow user to view detailed information
            print("\nEnter headline numbers to display more info, separated by commas (# -1 to go back):")
            selected = input("Enter your choice: ").strip()
            if selected == "-1":
                return
            selected_indices = [int(i) - 1 for i in selected.split(",") if i.isdigit()]
            for idx in selected_indices:
                if 0 <= idx < len(data_list):
                    article = data_list[idx]
                    print("\nDetailed Info:")
                    print(f"Source: {article.get('Name', 'Unknown Source')}")
                    print(f"Author: {article.get('Author', 'Unknown Author')}")
                    print(f"Title: {article.get('Title', 'No Title')}")
                    print(f"URL: {article.get('URL', 'No URL')}")
                    print(f"Description: {article.get('Description', 'No Description')}")
                    published_at = article.get('Published At', 'Unknown Date/Time')
                    if published_at != 'Unknown Date/Time':
                        print(f"Published Date: {published_at[:10]}")
                        print(f"Published Time: {published_at[11:19]}")
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
    response = receive_full_data(socket_c)
    try:
        data_list = pickle.loads(response)  # Deserialize the binary data
        if data_list:
            print("\nSources Received:")
            for idx, source in enumerate(data_list, 1):
                name = source.get('Name', 'Unknown Source')
                print(f"{idx}. {name}")

            # Allow user to view detailed information
            selected = input("Enter source numbers to display more info, separated by commas (# -1 to go back): ").strip()
            if selected == "-1":
                return
            selected_indices = [int(i) - 1 for i in selected.split(",") if i.isdigit()]
            for idx in selected_indices:
                if 0 <= idx < len(data_list):
                    source = data_list[idx]
                    print("\nDetailed Info:")
                    print(f"Name: {source.get('Name', 'Unknown Source')}")
                    print(f"Country: {source.get('Country', 'Unknown Country')}")
                    print(f"Description: {source.get('Description', 'No Description')}")
                    print(f"URL: {source.get('URL', 'No URL')}")
                    print(f"Category: {source.get('Category', 'No Category')}")
                    print(f"Language: {source.get('Language', 'Unknown Language')}")
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