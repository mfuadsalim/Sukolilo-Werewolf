import tkinter as tk

class ChatWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.chat_messages = []
        self.create_widgets()

    def create_widgets(self):
        # Create the chat display text box
        self.chat_display = tk.Text(self, height=10, width=50)
        self.chat_display.pack()

        # Create the chat entry
        self.chat_entry = tk.Entry(self, width=50)
        self.chat_entry.pack()

        # Create the submit button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_chat)
        self.submit_button.pack()

    def submit_chat(self):
        # Get the chat message from the chat entry
        message = self.chat_entry.get()

        # Clear the chat entry
        self.chat_entry.delete(0, tk.END)

        # Add the chat message to the chat messages list
        self.chat_messages.append(message)

        # Update the chat display
        self.update_chat_display()

    def update_chat_display(self):
        # Clear the chat display
        self.chat_display.delete(1.0, tk.END)

        # Display the latest chat messages in reverse order (bottom to top)
        start_index = max(0, len(self.chat_messages) - 10)  # Limit the display to 10 messages
        for message in self.chat_messages[start_index:]:
            self.chat_display.insert(tk.END, message + "\n")

# Create the main window
root = tk.Tk()

# Create the chat window
chat_window = ChatWindow(root)
chat_window.pack()

# Start the Tkinter event loop
root.mainloop()
