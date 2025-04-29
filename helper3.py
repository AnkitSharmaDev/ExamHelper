import tkinter as tk
import threading
import keyboard
import requests
import json
import win32gui
import win32con
import pythoncom
import pywintypes
import re
from pythoncom import CoInitialize, CoUninitialize

# Gemini API setup
GEMINI_API_KEY = "AIzaSyB-tr6klD817HyD9nAEaSGrKmSUeU0ahH8"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

class DropTarget:
    _public_methods_ = ['DragEnter', 'DragOver', 'DragLeave', 'Drop']
    _com_interfaces_ = [pythoncom.IID_IDropTarget]

    def __init__(self, app):
        self.app = app

    def DragEnter(self, data_obj, key_state, point, effect):
        # Check if CF_TEXT is available
        if data_obj.IsDataAvailable(win32con.CF_TEXT):
            return pythoncom.DROPEFFECT_COPY
        return pythoncom.DROPEFFECT_NONE

    def DragOver(self, key_state, point, effect):
        return pythoncom.DROPEFFECT_COPY

    def DragLeave(self):
        pass

    def Drop(self, data_obj, key_state, point, effect):
        # Get text from CF_TEXT
        if data_obj.IsDataAvailable(win32con.CF_TEXT):
            data = data_obj.GetData(win32con.CF_TEXT)
            question = data.decode('utf-8').strip()
            self.app.question_box.delete("1.0", tk.END)
            self.app.question_box.insert(tk.END, question)
            self.app.process_question(question)

class App:
    def __init__(self, root):
        self.root = root
        self.visible = True
        self.alpha = 1.0
        self.last_question = ""  # Track last question to avoid duplicate API calls
        
        # Window style: no title bar, no border
        root.overrideredirect(True)
        root.geometry("400x300+100+100")
        root.attributes("-topmost", True)
        root.configure(bg="white")
        
        # Dragging
        self.start_x = None
        self.start_y = None
        root.bind('<Button-1>', self.start_move)
        root.bind('<B1-Motion>', self.do_move)

        # Info label
        self.label = tk.Label(root, text="Press F8 to hide/unhide, F9 for transparency.", bg="white", font=("Arial", 9))
        self.label.pack(pady=5)

        # Question Box
        self.question_box = tk.Text(root, height=7, width=50, font=("Arial", 10))
        self.question_box.pack(pady=5)
        self.question_box.bind('<KeyRelease>', self.on_text_change)  # Detect typing

        # Answer Box
        self.answer_box = tk.Text(root, height=7, width=50, font=("Arial", 10))
        self.answer_box.pack(pady=5)

        # Keyboard shortcuts
        threading.Thread(target=self.keyboard_listener, daemon=True).start()

        # Drag and Drop setup using pywin32
        self.setup_dnd()

    def setup_dnd(self):
        CoInitialize()
        hwnd = self.root.winfo_id()
        def drop_handler(hwnd, msg, wp, lp):
            if msg == win32con.WM_DROPFILES:
                # Handle file drops (optional, kept for compatibility)
                hdrop = wp
                count = win32gui.DragQueryFile(hdrop, 0xFFFFFFFF)
                if count > 0:
                    file_path = win32gui.DragQueryFile(hdrop, 0)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        question = f.read().strip()
                    self.question_box.delete("1.0", tk.END)
                    self.question_box.insert(tk.END, question)
                    self.process_question(question)
                win32gui.DragFinish(hdrop)
            elif msg == win32con.WM_NCHITTEST:
                # Allow dragging from anywhere
                return win32con.HTCLIENT
            return win32gui.CallWindowProc(oldWndProc, hwnd, msg, wp, lp)
        
        win32gui.DragAcceptFiles(hwnd, True)
        # Register for text drag-and-drop
        drop_target = DropTarget(self)
        com_object = pythoncom.WrapObject(drop_target, pythoncom.IID_IDropTarget)
        pythoncom.RegisterDragDrop(hwnd, com_object)
        oldWndProc = win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, drop_handler)

    def start_move(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root

    def do_move(self, event):
        x = event.x_root - self.start_x
        y = event.y_root - self.start_y
        self.root.geometry(f"+{x}+{y}")

    def on_text_change(self, event):
        question = self.question_box.get("1.0", tk.END).strip()
        if question and question != self.last_question:
            self.process_question(question)

    def process_question(self, question):
        self.last_question = question
        self.answer_box.delete("1.0", tk.END)
        self.answer_box.insert(tk.END, "Thinking...")
        threading.Thread(target=self.get_answer, args=(question,), daemon=True).start()

    def get_answer(self, question):
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {"parts": [{"text": question + "\n\nAnswer format: Check if MCQ then provide only the correct answer from the available options. Respond strictly in the format: option label (answer), e.g., c (4/3). If options are unlabeled, assign labels sequentially: (a) for the first option with the correct option value, (b) for the second with the correct option value, and so on. Display the correct option along with its corresponding value. Do not provide any explanations—only the final answer in the specified format."}]}
            ]
        }
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            answer = result['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Validate answer format
            if re.match(r'^[a-d]\s*\(.*\)$', answer):
                self.answer_box.delete("1.0", tk.END)
                self.answer_box.insert(tk.END, answer)
            else:
                self.answer_box.delete("1.0", tk.END)
                self.answer_box.insert(tk.END, "Invalid answer format")
        except Exception as e:
            self.answer_box.delete("1.0", tk.END)
            self.answer_box.insert(tk.END, f"Failed: {e}")

    def keyboard_listener(self):
        while True:
            if keyboard.is_pressed('F8'):
                self.toggle_visibility()
                keyboard.wait('F8')
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
        self.alpha = 0.7 if self.alpha == 1.0 else 1.0
        self.root.attributes('-alpha', self.alpha)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()