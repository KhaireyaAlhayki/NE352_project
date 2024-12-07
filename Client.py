import socket
import pickle
import tkinter as tk
from tkinter import messagebox

# variables for categories, countries, and languages
categories = {
    '1': 'business',
    '2': 'general',
    '3': 'health',
    '4': 'science',
    '5': 'sports',
    '6': 'technology'
}
countries = {
    '1': 'au',
    '2': 'ca',
    '3': 'jp',
    '4': 'ae',
    '5': 'sa',
    '6': 'kr',
    '7': 'us',
    '8': 'ma'
}
languages = {
    '1': 'ar',
    '2': 'en'
}

def receive_full_data(socket_c):
    """handle all the receiving data from the server"""
    response = b""
    while True:
        data = socket_c.recv(4096)
        response += data
        if len(data) < 4096:
            break
    return response

# Main Client Application
class main:
    def __init__(self, root):
        self.root = root
        self.root.title("News Application")
        self.root.geometry("800x600")
        self.root.configure(background="#a3c1e3")
        
        # Socket connection
        self.socket_c = None
        self.username = None

        # Initialize login screen
        self.create_login_screen()

    def connect_to_server(self):
        """Attempt to connect to the server."""
        try:
            self.socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_c.connect(("127.0.0.1", 49999))
            print("Connected to the server.")
        # Handle the error  
        except ConnectionRefusedError:
            messagebox.showerror("Error", "Failed to connect to the server.")
            self.root.destroy()

    def create_login_screen(self):
        """Create the login screen for username entry."""
        self.clear_screen()
        tk.Label(self.root, text="Welcome to the News liabrary",bg="#a3c1e3",font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Enter your username:",bg="#a3c1e3",font=("Arial", 16)).pack(pady=20)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=10)

        tk.Button(self.root, text="Submit", command=self.handle_login, font=("Arial", 14)).pack(pady=20)

    def handle_login(self):
        """Send the username to the server and get a welcome message."""
        username = self.username_entry.get().strip()
        if username:
            self.username = username
            self.connect_to_server()
            self.socket_c.send(self.username.encode())
            welcome_message = self.socket_c.recv(1024).decode("utf-8")
            messagebox.showinfo("Welcome", welcome_message)
            self.create_main_menu()
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid username.")

    def create_main_menu(self):
        """Create the main menu screen."""
        self.clear_screen()

        tk.Label(self.root, text="Main Menu",bg="#a3c1e3", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Search Headlines", font=("Arial", 14), command=self.headlines_menu).pack(pady=10)
        tk.Button(self.root, text="List of Sources", font=("Arial", 14), command=self.sources_menu).pack(pady=10)
        tk.Button(self.root, text="Quit", font=("Arial", 14), command=self.root.quit).pack(pady=10)

    def headlines_menu(self):
        """Create the headlines menu."""
        self.clear_screen()

        tk.Label(self.root, text="Headlines Menu",bg="#a3c1e3", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Search for Keywords", font=("Arial", 14),
                  command=lambda: self.input_prompt("Enter Keywords:", "1-1")).pack(pady=10)
        tk.Button(self.root, text="Search by Category", font=("Arial", 14),
                  command=lambda: self.select_from_list("Select Category", categories, "1-2")).pack(pady=10)
        tk.Button(self.root, text="Search by Country", font=("Arial", 14),
                  command=lambda: self.select_from_list("Select Country", countries, "1-3")).pack(pady=10)
        tk.Button(self.root, text="List All Headlines", font=("Arial", 14),
                  command=lambda: self.send_request("1-4", "")).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)

    def sources_menu(self):
        """Create the sources menu."""
        self.clear_screen()

        tk.Label(self.root, text="Sources Menu",bg="#a3c1e3", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Search by Category", font=("Arial", 14),
                  command=lambda: self.select_from_list("Select Category", categories, "2-1")).pack(pady=10)
        tk.Button(self.root, text="Search by Country", font=("Arial", 14),
                  command=lambda: self.select_from_list("Select Country", countries, "2-2")).pack(pady=10)
        tk.Button(self.root, text="Search by Language", font=("Arial", 14),
                  command=lambda: self.select_from_list("Select Language", languages, "2-3")).pack(pady=10)
        tk.Button(self.root, text="List All Sources", font=("Arial", 14),
                  command=lambda: self.send_request("2-4", "")).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)

    def input_prompt(self, prompt_text, request_type):
        """Prompt the user to enter keyword."""
        self.clear_screen()

        tk.Label(self.root, text=prompt_text,bg="#a3c1e3", font=("Arial", 16)).pack(pady=20)
        input_entry = tk.Entry(self.root, font=("Arial", 14))
        input_entry.pack(pady=10)

        tk.Button(self.root, text="Submit", font=("Arial", 14),
                  command=lambda: self.send_request(request_type, input_entry.get().strip())).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.headlines_menu).pack(pady=10)

    def select_from_list(self, title, options, request_type):
        """Display a list for the user to select from."""
        self.clear_screen()

        tk.Label(self.root, text=title,bg="#a3c1e3", font=("Arial", 16)).pack(pady=20)

        for key, value in options.items():
            tk.Button(self.root, text=value.capitalize(), font=("Arial", 14),
                      command=lambda value=value: self.send_request(request_type, value)).pack(pady=5)

        tk.Button(self.root, text="Back to the main menu", font=("Arial", 14), command=self.create_main_menu).pack(pady=5)

    def send_request(self, request_type, parameter):
        """Send a request to the server."""
        request = f"{request_type}-{parameter}-{self.username}"
        print("Sending request:", request)
        self.socket_c.send(request.encode())

        # Receive and process the response
        response = receive_full_data(self.socket_c)
        try:
            data_list = pickle.loads(response)
            # For headlines requests
            if request_type.startswith("1"):  
                self.display_headlines(data_list)
            # For sources requests
            elif request_type.startswith("2"):  
                self.display_sources(data_list)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing response: {e}")

    def display_headlines(self, headlines_list):
      """Display the list of headlines."""
      self.clear_screen()

      tk.Label(self.root, text="Headlines Received",bg="#a3c1e3", font=("Arial", 16)).pack(pady=20)

      if not headlines_list:
          # Handling of empty data
          tk.Label(self.root, text="No headlines found.",bg="#a3c1e3", font=("Arial", 14)).pack(pady=10)
          tk.Button(self.root, text="Back to the main menu", font=("Arial", 14), command=self.create_main_menu).pack(pady=2)
          return

      results_box = tk.Text(self.root, font=("Arial", 14), wrap="word", height=20)
      results_box.pack(padx=10, pady=10)

      for idx, article in enumerate(headlines_list, 1):
          # Check if the entry is a dictionary
          if isinstance(article, dict):  
              source_name = article.get('Name', 'Unknown Source')
              author = article.get('Author', 'Unknown Author')
              title = article.get('Title', 'No Title')
              results_box.insert("end", f"{idx}. Author: {author} | Title: {title} | (Source: {source_name})\n")
           # Entry is not a dictionary, handle it as plain text
          else: 
              results_box.insert("end", f"{idx}. {article}\n")

      tk.Label(self.root, text="Enter headline numbers for details (comma-separated):",bg="#a3c1e3", font=("Arial", 14)).pack(pady=10)
      detail_entry = tk.Entry(self.root, font=("Arial", 14))
      detail_entry.pack(pady=5)

      tk.Button(
          self.root,
          text="View Details",
          font=("Arial", 12),
          command=lambda: self.display_detailed_headlines(headlines_list, detail_entry.get())).pack(pady=5)

      tk.Button(self.root, text="Back to the main menu", font=("Arial", 12), command=self.create_main_menu).pack(pady=10)

    def display_detailed_headlines(self, headlines_list, indices):
        """Display detailed information for selected headlines."""
        try:
            selected_indices = [int(i.strip()) - 1 for i in indices.split(",") if i.strip().isdigit()]
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
            return

        self.clear_screen()

        tk.Label(self.root, text="Detailed Headline Information", font=("Arial", 16)).pack(pady=20)
        details_box = tk.Text(self.root, font=("Arial", 14), wrap="word", height=20)
        details_box.pack(padx=10, pady=10)

        for idx in selected_indices:
            if 0 <= idx < len(headlines_list):
                article = headlines_list[idx]
                details_box.insert("end", f"Source: {article.get('Name', 'Unknown Source')}\n")
                details_box.insert("end", f"Author: {article.get('Author', 'Unknown Author')}\n")
                details_box.insert("end", f"Title: {article.get('Title', 'No Title')}\n")
                details_box.insert("end", f"URL: {article.get('URL', 'No URL')}\n")
                details_box.insert("end", f"Description: {article.get('Description', 'No Description')}\n")
                published_at = article.get('Published At', 'Unknown Date/Time')
                if published_at != 'Unknown Date/Time':
                    details_box.insert("end", f"Published Date: {published_at[:10]}\n")
                    details_box.insert("end", f"Published Time: {published_at[11:19]}\n")
                details_box.insert("end", "\n" + "-" * 50 + "\n\n")
            else:
                details_box.insert("end", f"Invalid index: {idx + 1}\n")

        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)

    def display_sources(self, sources_list):
      """Display the list of sources."""
      self.clear_screen()

      tk.Label(self.root, text="Sources Received",bg="#a3c1e3", font=("Arial", 16)).pack(pady=20)

      if not sources_list:
          # Handling the empty data
          tk.Label(self.root, text="No sources found.",bg="#a3c1e3", font=("Arial", 14)).pack(pady=10)
          tk.Button(self.root, text="Back to the main menu", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)
          return

      results_box = tk.Text(self.root, font=("Arial", 14), wrap="word", height=20)
      results_box.pack(padx=10, pady=10)

      for idx, source in enumerate(sources_list, 1):
          # Check if the entry is a dictionary
          if isinstance(source, dict):  
              name = source.get('Name', 'Unknown Source')
              results_box.insert("end", f"{idx}. Source Name: {name}\n")
          # Entry is not a dictionary, handle it as plain text
          else:  
              results_box.insert("end", f"{idx}. {source}\n")

      tk.Label(self.root, text="Enter source numbers for details (comma-separated):",bg="#a3c1e3", font=("Arial", 14)).pack(pady=10)
      detail_entry = tk.Entry(self.root, font=("Arial", 14))
      detail_entry.pack(pady=5)

      tk.Button(
          self.root,
          text="View Details",
          font=("Arial", 12),
          command=lambda: self.display_detailed_sources(sources_list, detail_entry.get())).pack(pady=5)

      tk.Button(self.root, text="Back to the main menu", font=("Arial", 12), command=self.create_main_menu).pack(pady=10)
      
    def display_detailed_sources(self, sources_list, indices):
        """Display detailed information for selected sources."""
        try:
            selected_indices = [int(i.strip()) - 1 for i in indices.split(",") if i.strip().isdigit()]
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
            return

        self.clear_screen()

        tk.Label(self.root, text="Detailed Source Information",bg="#a3c1e3", font=("Arial", 16)).pack(pady=20)
        details_box = tk.Text(self.root, font=("Arial", 14), wrap="word", height=20)
        details_box.pack(padx=10, pady=10)

        for idx in selected_indices:
            if 0 <= idx < len(sources_list):
                source = sources_list[idx]
                details_box.insert("end", f"Name: {source.get('Name', 'Unknown Source')}\n")
                details_box.insert("end", f"Country: {source.get('Country', 'Unknown Country')}\n")
                details_box.insert("end", f"Description: {source.get('Description', 'No Description')}\n")
                details_box.insert("end", f"URL: {source.get('URL', 'No URL')}\n")
                details_box.insert("end", f"Category: {source.get('Category', 'No Category')}\n")
                details_box.insert("end", f"Language: {source.get('Language', 'Unknown Language')}\n")
                details_box.insert("end", "\n" + "-" * 50 + "\n\n")
            else:
                details_box.insert("end", f"Invalid index: {idx + 1}\n")

        tk.Button(self.root, text="Back to the main menu", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)

    def clear_screen(self):
        '''Clear the screen for the next UI interaction'''
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    root.mainloop()