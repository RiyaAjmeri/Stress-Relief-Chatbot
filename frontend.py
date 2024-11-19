import tkinter as tk
from backend import get_bot_response, speak_text, setup_tts_engine
# , ask_user_location

# Tkinter GUI setup
root = tk.Tk()
root.title("Stress-Relief Chatbot")

chat_history = tk.Text(root, bg="lightgrey", fg="black", font=("Arial", 14), height=20, width=50)
chat_history.pack(pady=10)

user_input = tk.Entry(root, font=("Arial", 14), width=40)
user_input.pack(pady=5)



def quit_bot():
    """Handles quit action from the GUI"""
    farewell_message = "Goodbye, take care! I'm here whenever you need me."
    speak_text(farewell_message)  # Speak the farewell message
    root.quit() 

def send_message():
    """Handle sending user messages."""
    if user_input.lower() == "quit":
        quit_bot()  # Close the application
    else:user_message = user_input.get()

    if user_message.strip():
        chat_history.insert(tk.END, "You: " + user_message + "\n")
        bot_response = get_bot_response(user_message)
        chat_history.insert(tk.END, "Bot: " + bot_response + "\n")
        speak_text(bot_response)
        user_input.delete(0, tk.END)

# Set up the TTS engine initially
setup_tts_engine()

# Display the initial greeting message using TTS
greeting_message = "Hi! How can I help you today? Press 'quit' to exit."
speak_text(greeting_message)  # Speak the greeting message when the app starts

# # Add chat output root
# chat_output = tk.Text(root, height=20, width=50, state=tk.DISABLED)
# chat_output.pack(padx=10, pady=10)

# # Add text input field
# text_input = tk.Entry(root, width=40)
# text_input.pack(padx=10, pady=10)

# Add a button to send the message
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

# Add a quit button to exit the app
quit_button = tk.Button(root, text="Quit", command=quit_bot)
quit_button.pack(padx=10, pady=10)

# # Ask for user location (run only once)
# # ask_user_location()

# Start the Tkinter main loop
root.mainloop()


# import tkinter as tk
# from tkinter import messagebox
# import pyttsx3
# import threading
# import time

# # Function to handle the 'quit' functionality in the GUI
# def quit_bot():
#     """Handles quit action from the GUI"""
#     farewell_message = "Goodbye, take care! I'm here whenever you need me."
#     speak_text(farewell_message)  # Speak the farewell message
#     root.quit()  # Close the root

# # Function to handle user input from the GUI
# def send_message():
#     """Handle the user input and bot response"""
#     user_input = text_input.get()  # Get user input from the text field
#     if user_input.lower() == "quit":
#         quit_bot()  # Close the application
#     else:
#         response = get_bot_response(user_input)  # Get bot response
#         chat_output.config(state=tk.NORMAL)
#         chat_output.insert(tk.END, "You: " + user_input + '\n')  # Display user input
#         chat_output.insert(tk.END, "Bot: " + response + '\n')  # Display bot response
#         chat_output.config(state=tk.DISABLED)
#         text_input.delete(0, tk.END)  # Clear the text field
#         speak_text(response)  # Speak the response

# # Create the main root
# root = tk.Tk()
# root.title("Stress-Relief Chatbot")
# root.geometry("400x500")

# # Set up the TTS engine initially
# setup_tts_engine()

# # Display the initial greeting message using TTS
# greeting_message = "Hi! How can I help you today? Type 'quit' to exit."
# speak_text(greeting_message)  # Speak the greeting message when the app starts

# # Add chat output root
# chat_output = tk.Text(root, height=20, width=50, state=tk.DISABLED)
# chat_output.pack(padx=10, pady=10)

# # Add text input field
# text_input = tk.Entry(root, width=40)
# text_input.pack(padx=10, pady=10)

# Add a button to send the message
# send_button = tk.Button(root, text="Send", command=send_message)
# send_button.pack(padx=10, pady=10)

# Add a quit button to exit the app
# quit_button = tk.Button(root, text="Quit", command=quit_bot)
# quit_button.pack(padx=10, pady=10)

# # Start the Tkinter main loop
# root.mainloop()