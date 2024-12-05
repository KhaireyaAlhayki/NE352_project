import socket
import json

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
    choice=int(input("Enter the number of your choice: "))
    return choice
    
def headlines_menu(socket_c):
    print("\nHeadlines Menu:")
    print("""
    1-Search for keywords
    2-Search by category
    3-Search by country
    4-List all new headlines
    5-Back to the main menu
    """)
    option=int(input("Enter the number of your option:"))
    # Handle non-existent options
    while option not in range(1, 6):
        print("Invalid option. Please choose a number between 1 and 5.")
        option = int(input("Enter the number of your option: "))
    
    request = ""  # Initialize request variable
    if option == 1:
        keyword = input("Enter the keywords: ")
        request = f"1-1-{keyword}" 
    elif option == 2:
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
            request = f"1-2-{category}"  
    elif option == 3:
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
            request = f"1-3-{country}"  
    elif option == 4:
        request = "1-4-"  
    elif option == 5:
        return  # Back to the main menu

    print("Sending request:", request)
    socket_c.send(request.encode())
    
    # Receiving the response from the server
    response = socket_c.recv(4096).decode()
    print("The received response:", response)

def sources_menu(socket_c):
    print("\nSources Menu:")
    print("""
    1-Search by category
    2-Search by country
    3-Search by language
    4-List all
    5-Back to the main menu
    """)
    option = int(input("Enter the number of your option:"))
    
    # Handle non-existent options
    while option not in range(1, 6):
        print("Invalid option. Please choose a number between 1 and 5.")
        option = int(input("Enter the number of your option: "))
    
    request = ""  # Initialize request variable
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
            request = f"2-1-{category}"  
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
            request = f"2-2-{country}"  
    elif option == 3:
        print("""
        1-ar
        2-en 
        """)
        languages_o = input("Enter the category number (1-2): ")
        if languages_o in languages:
            language = languages[languages_o]
            request = f"2-3-{language}"  
    elif option == 4:
        request = "2-4-"  
    elif option == 5:
        return  
    
    print("Sending request:", request)
    socket_c.send(request.encode())
    
    # Receiving the response from the server
    response = socket_c.recv(4096).decode()
    print("The received response:", response)


def client():
    try:
        socket_c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_c.connect(("127.0.0.1", 49999))
        print("Connected to the server.")
        client_name=input("Enter username: ")
        socket_c.send(client_name.encode())
        while True:
            choice=main_menu()
            if choice==1:
                headlines_menu(socket_c)
            elif choice==2:
                sources_menu(socket_c)
            elif choice==3:
                print("Quitting...")
                break
            else:
                print("it's an invalid number...Try Again")
        socket_c.close()
    #handle the errors
    except ConnectionResetError:
        print("Connection lost.")
    except ConnectionRefusedError:
        print("Failed connect to the Server.")
    except Exception as error_msg:
        print(f"there error ocurred: {error_msg}")

if __name__ == "__main__":
    client()

