import re
import threading
import ollama
import tkinter as tk
from tkinter import scrolledtext

# Store conversation history
conversation_history = []
MODEL = "deepseek-r1:14b"

def run_ollama_chat(input_text, callback, update_status):
    """
    Run Ollama in a separate thread with live streaming updates.
    """
    global conversation_history

    # Append user input to conversation history
    conversation_history.append({"role": "user", "content": input_text})

    try:
        update_status("R1 is thinking...")

        # Start streaming response
        stream = ollama.chat(model=MODEL, messages=conversation_history, stream=True)

        full_response = ""
        word_count = 0
        inside_think_tag = False  # Track if inside <think>...</think>

        for chunk in stream:
            text_chunk = chunk["message"]["content"]
            if text_chunk:
                # Count words in full response (including <think> content)
                word_count += len(text_chunk.split())
                update_status(f"Words output: {word_count}")

                # Remove <think> tags and ignore their content
                processed_text = ""
                for part in re.split(r"(<think>|</think>)", text_chunk):
                    if part == "<think>":
                        inside_think_tag = True
                    elif part == "</think>":
                        inside_think_tag = False
                    elif not inside_think_tag:
                        processed_text += part

                # Append processed text to full response (excluding <think> content)
                full_response += processed_text
                callback(processed_text, append=True)

        # Append cleaned response to conversation history
        conversation_history.append({"role": "assistant", "content": full_response.strip()})

        # Final word count update
        update_status(f"Words output: {word_count}")

    except Exception as e:
        callback(f"Error: {e}", append=False)
        update_status("Error occurred")

def send_message():
    """
    Handle user input, display in UI, and run Ollama in a separate thread.
    """
    user_input = user_entry.get("1.0", tk.END).strip()
    if not user_input:
        return

    # Add a separator before each new user input
    chat_display.insert(tk.END, "\n----------------\n", "separator")
    chat_display.insert(tk.END, f"You: {user_input}\n", "user")
    chat_display.see(tk.END)

    # Clear input field immediately
    user_entry.delete("1.0", tk.END)

    # Disable input while waiting for response
    user_entry.config(state=tk.DISABLED)
    send_button.config(state=tk.DISABLED)

    # Callback function to update UI incrementally
    def update_ui(response_chunk, append=True):
        if append:
            chat_display.insert(tk.END, response_chunk, "bot")
        else:
            chat_display.insert(tk.END, f"Ollama: {response_chunk}\n", "bot")
        chat_display.see(tk.END)

    # Function to update status label
    def update_status(text):
        status_label.config(text=text)

    # Run Ollama in a separate thread with streaming
    threading.Thread(target=run_ollama_chat, args=(user_input, update_ui, update_status), daemon=True).start()

    # Re-enable input after response
    user_entry.config(state=tk.NORMAL)
    send_button.config(state=tk.NORMAL)

# GUI Setup
root = tk.Tk()
root.title("{} Chat GUI".format(MODEL))

# Chat Display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
chat_display.pack(padx=10, pady=10)
chat_display.tag_configure("user", foreground="blue")
chat_display.tag_configure("bot", foreground="green")
chat_display.tag_configure("separator", foreground="gray")

# User Input Box
user_entry = tk.Text(root, height=3, width=50, font=("Arial", 12))
user_entry.pack(padx=10, pady=5)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12))
send_button.pack(pady=5)

# Status Label (Bottom Right)
status_label = tk.Label(root, text="Ready", font=("Arial", 10), fg="gray", anchor="e")
status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

# Run the application
root.mainloop()
