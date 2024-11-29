import socket


def main_menu():
    print("\nMain Menu: ")
    print("1-Search headlines")
    print("2-List of sources")
    print("3-Quit")
    
    
def headlines_menu():
    print("\nHeadlines Menu:")
    print("1-Search for keywords")
    print("2-Search by category")
    print("3-Search by country")
    print("4-List all new headlines")
    print("5-Back to the main menu")

def sources_menu():
    print("\nSources Menu:")
    print("1-Search by category")
    print("2-Search by country")
    print("3-Search by language")
    print("4-List all")
    print("5-Back to the main menu")


def client():
    try:
        socket_c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_c.connect("127.0.0.1", 8080)

        while True:
            main_menu()
            choice=int.input("Enter the number of your choice: ")
            if choice==1:
                headlines_menu()
                option=int(input("Enter the number of your option:"))
                while option not in range(1,6):
                    print("Invalid option. Please choose a number between 1 and 5.")
            elif choice==2:
                sources_menu()
                option=int(input("Enter the number of your option:"))
                while option not in range(1,6):
                    print("Invalid option. Please choose a number between 1 and 5.")
            elif choice==3:
                break
            else:
                print("it's an invalid number...Try Again")

    except ConnectionResetError:
        print("Connection lost.")
    except ConnectionRefusedError:
        print("Failed connect to the Server.")
    except Exception as error_msg:
        print("there error ocurred: {error_msg}")

if __name__ == "__main__":
    client()