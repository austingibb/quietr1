import re
import threading
import ollama
import tkinter as tk
from tkinter import scrolledtext

# Store conversation history
conversation_history = []
MODEL="deepseek-r1:14b"

def run_ollama_chat(input_text, callback):
    """
    Run Ollama in a separate thread to keep UI responsive.
    """
    global conversation_history

    # Append user input to conversation history
    conversation_history.append({"role": "user", "content": input_text})

    try:
        # Run the model in the background
        response = ollama.chat(model=MODEL, messages=conversation_history)

        # Extract raw response text
        ollama_response = response['message']['content']

        # Remove the <think>...</think> section
        cleaned_response = re.sub(r'<think>.*?</think>', '', ollama_response, flags=re.DOTALL).strip()

        # Append cleaned response to conversation history
        conversation_history.append({"role": "assistant", "content": cleaned_response})

        # Send the response back to the UI using the callback function
        callback(cleaned_response)

    except Exception as e:
        callback(f"Error: {e}")

def send_message():
    """
    Handle user input, display in UI, and run Ollama in a separate thread.
    """
    user_input = user_entry.get("1.0", tk.END).strip()
    if not user_input:
        return
    
    chat_display.insert(tk.END, f"You: {user_input}\n", "user")
    chat_display.see(tk.END)

    # Disable input while waiting for response
    user_entry.config(state=tk.DISABLED)
    send_button.config(state=tk.DISABLED)

    # Callback function to update UI after response
    def update_ui(response):
        chat_display.insert(tk.END, f"Ollama: {response}\n", "bot")
        chat_display.see(tk.END)

        # Re-enable input after response
        user_entry.config(state=tk.NORMAL)
        send_button.config(state=tk.NORMAL)

    # Run Ollama in a separate thread to prevent UI freezing
    threading.Thread(target=run_ollama_chat, args=(user_input, update_ui), daemon=True).start()

    # Clear input box
    user_entry.delete("1.0", tk.END)

# GUI Setup
root = tk.Tk()
root.title("{} Chat GUI".format(MODEL))

# Chat Display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
chat_display.pack(padx=10, pady=10)
chat_display.tag_configure("user", foreground="blue")
chat_display.tag_configure("bot", foreground="green")

# User Input Box
user_entry = tk.Text(root, height=3, width=50, font=("Arial", 12))
user_entry.pack(padx=10, pady=5)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12))
send_button.pack(pady=5)

# Run the application
root.mainloop()
