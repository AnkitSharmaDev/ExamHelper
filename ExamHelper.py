import tkinter as tk
from tkinter import filedialog
import threading
import keyboard
import requests
import json
from tkinterdnd2 import TkinterDnD, DND_TEXT
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Gemini API setup

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

class App:
    def __init__(self, root):
        root.attributes('-alpha', 0.5)
        # root.wm_attributes( 'white')

        self.root = root
        self.visible = True

        # Normal window style
        root.title("")  # No title bar
        root.geometry("300x200+100+100")  # Smaller window size (width x height)
        root.attributes("-topmost", True)  # Always on top
        root.configure(bg="white")
        root.overrideredirect(True)  # No border or title bar

        # Dragging
        self.start_x = None
        self.start_y = None
        root.bind('<Button-1>', self.start_move)
        root.bind('<B1-Motion>', self.do_move)

        # Question Box
        self.question_box = tk.Text(root, height=5, width=30, font=("Arial", 10))
        self.question_box.pack(pady=5)

        # Answer Box
        self.answer_box = tk.Text(root, height=5, width=30, font=("Arial", 10))
        self.answer_box.pack(pady=5)

        # Close Button (cross icon)
        self.close_button = tk.Button(root, text="X", command=self.close_window, font=("Arial", 12, "bold"), bd=0, fg="gray", bg="white", relief="flat")
        self.close_button.place(x=270, y=5)  # Position the button in the top-right corner

        # Keyboard shortcuts
        threading.Thread(target=self.keyboard_listener, daemon=True).start()

        # Register drag-and-drop functionality using tkinterdnd2
        self.register_drop()

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def do_move(self, event):
        x = event.x_root - self.start_x
        y = event.y_root - self.start_y
        self.root.geometry(f"+{x}+{y}")

    def on_drop(self, event):
        # Get the text dropped into the question box
        question = event.data.strip()  # This gets the text dropped
        if question:
            self.answer_box.delete("1.0", tk.END)  # Clear previous answer
            self.answer_box.insert(tk.END, "Thinking...")  # Show thinking message
            threading.Thread(target=self.get_answer, args=(question,), daemon=True).start()

    def get_answer(self, question):
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {"parts": [{"text": question + "\n\nAnswer format: Provide only the correct answer based on a thorough analysis of the question. Respond strictly in the format: option label (answer), e.g., c (4/3). If options are provided, choose the correct one based on the analysis. If no options are given, provide the correct answer directly. Always ensure a proper analysis of the question before choosing the correct answer, and do not provide any explanations—just the final, correct answer in the specified format. Make sure to carefully evaluate the question and ensure the answer is accurate."}]}
            ]
        }
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))
            result = response.json()
            answer = result['candidates'][0]['content']['parts'][0]['text']

            # Handle answer formatting based on your requirements
            self.answer_box.delete("1.0", tk.END)
            formatted_answer = self.format_answer(answer)
            self.answer_box.insert(tk.END, formatted_answer)
        except Exception as e:
            self.answer_box.delete("1.0", tk.END)
            self.answer_box.insert(tk.END, f"Failed: {e}")

    def format_answer(self, answer):
        # Check if the answer contains options and return only the correct answer
        if "a)" in answer or "b)" in answer or "c)" in answer:  # Simple check for MCQ options
            options = answer.split("\n")
            for i, option in enumerate(options):
                if 'correct' in option.lower():  # Assuming the answer text will contain "correct"
                    return f"{chr(97 + i)} ({option.strip()})"
        return answer.strip()  # Fallback if no MCQ options

    def keyboard_listener(self):
        while True:
            if keyboard.is_pressed('F10'):
                self.toggle_visibility()
                keyboard.wait('F10')
            if keyboard.is_pressed('F9'):
                self.toggle_transparency()
                keyboard.wait('F9')

    def toggle_visibility(self):
        if self.visible:
            self.root.withdraw()
        else:
            self.root.deiconify()
        self.visible = not self.visible

    def toggle_transparency(self):
        alpha = self.root.attributes('-alpha')
        self.root.attributes('-alpha', 0.7 if alpha == 1.0 else 1.0)

    def close_window(self):
        # Close the window when the close button is clicked
        self.root.quit()

    def register_drop(self):
        # Register drag-and-drop functionality for text
        self.root.drop_target_register(DND_TEXT)  # Register text drop
        self.root.dnd_bind('<<Drop>>', self.on_drop)  # Bind drop event to handler

# Main
if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD.Tk instead of tk.Tk for drag-and-drop
    app = App(root)
    root.mainloop()
