import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext

# Set up your Gemini API key
GEMINI_API_KEY = "AIzaSyCEjZA2bQpHdNkTEDhn9FDmC_3UroaN33Q"

genai.configure(api_key=GEMINI_API_KEY)

def chat_with_gemini(prompt):
    # Define specific puzzle-related keywords
    puzzle_keywords = [
        'puzzle', 'Rubik\'s Cube', 'Sudoku', 'N-Queens', 'maze', 
        'Tic-Tac-Toe', 'game', 'solve', 'algorithm', 'evolutionary algorithm', 'genetic algorithm'
    ]
    
    # Check if the prompt contains any puzzle-related keywords
    if any(keyword in prompt.lower() for keyword in puzzle_keywords):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            
            # Clean up any unwanted '*' or other symbols
            cleaned_response = response.text.strip().replace("*", "")  # Remove asterisks if they appear
            
            return cleaned_response
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "I'm sorry, I can only answer questions related to Puzzles."

# GUI Application
def send_message():
    user_input = user_entry.get()
    if user_input.strip():
        # Display user input
        chat_display.insert(tk.END, "You: " + user_input + "\n", "user")
        user_entry.delete(0, tk.END)
        
        # Get and display the chatbot's response
        response = chat_with_gemini(user_input)
        chat_display.insert(tk.END, "Chatbot: " + response + "\n", "bot")
        chat_display.yview(tk.END)

# Create main window
root = tk.Tk()
root.title("Gemini AI Chatbot")
root.geometry("500x600")
root.configure(bg="cornsilk2")

# Chat display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#ffffff", font=("Arial", 12))
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.tag_config("user", foreground="blue")
chat_display.tag_config("bot", foreground="green")

# Entry field
user_entry = tk.Entry(root, font=("Arial", 14))
user_entry.pack(padx=10, pady=5, fill=tk.X)

# Send button
send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12), bg="#4CAF50", fg="black")
send_button.pack(pady=5)

# Run the app
root.mainloop()
