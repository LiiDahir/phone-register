import socket
import threading
import customtkinter as ctk

class ManageServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket Server/Client")
        self.root.geometry("400x300")
        
        # Set appearance mode
        ctk.set_appearance_mode("dark")  # Modes: "dark", "light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

        # Dropdown menu for selecting Server or Client
        self.mode_var = ctk.StringVar(value="server")
        self.mode_menu = ctk.CTkOptionMenu(root, values=["server", "client"], variable=self.mode_var, command=self.update_mode)
        self.mode_menu.pack(pady=10)

        # IP address entry for the client
        self.ip_entry = ctk.CTkEntry(root, placeholder_text="Server IP (default: 192.168.1.13)")
        self.ip_entry.insert(0, '192.168.1.13')  # Default IP address

        # Port entry for both server and client
        self.port_entry = ctk.CTkEntry(root, placeholder_text="Port (default: 65363)")
        self.port_entry.pack(pady=10)
        self.port_entry.insert(0, '65363')  # Default port number

        # Button to start the server or client
        self.start_button = ctk.CTkButton(root, text="Start", command=self.start)
        self.start_button.pack(pady=10)

        # Textbox to display logs
        self.log_text = ctk.CTkTextbox(root, height=10)
        self.log_text.pack(pady=10, padx=10, fill='both', expand=True)

        # Set initial mode (Server mode by default)
        self.update_mode(self.mode_var.get())

    def update_mode(self, mode):
        """Update GUI components based on the selected mode."""
        if mode == "client":
            self.ip_entry.pack(pady=10)
        else:
            self.ip_entry.pack_forget()

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.yview("end")

    def start(self):
        state = self.mode_var.get()
        port = int(self.port_entry.get())
        
        if state.lower() == "server":
            threading.Thread(target=self.start_server, args=(port,)).start()
        else:
            host = self.ip_entry.get()
            threading.Thread(target=self.start_client, args=(host, port)).start()

    def start_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)

        ip_address = self.get_ip_address()
        self.log(f"Server is listening on {ip_address}:{port}...")

        while True:
            client_socket, addr = server_socket.accept()
            self.log(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def start_client(self, host, port):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            self.log(f"Connected to {host}:{port}")
            message = client_socket.recv(1024)
            self.log(f"Received: {message.decode('ascii')}")
            client_socket.close()
        except Exception as e:
            self.log(f"Failed to connect: {e}")

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.254.254.254', 1))
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = '127.0.0.1'
        finally:
            s.close()
        return ip_address

    def handle_client(self, client_socket, addr):
        message = 'Thank you for connecting' + "\r\n"
        client_socket.send(message.encode('ascii'))
        client_socket.close()

# Create the GUI application
root = ctk.CTk()
app = ManageServerGUI(root)
root.mainloop()
