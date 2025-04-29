# **ExamHelper**

**ExamHelper** is a lightweight, cross-platform overlay dialog box designed for seamless question input via typing or drag-and-drop, delivering instant answers. It operates discreetly over any application, making it suitable for productivity, research, or accessibility purposes. The tool is crafted to be unobtrusive and undetectable by most applications, but users are urged to use it responsibly.

⚠️ **Warning:** This tool is intended for ethical use only. Using **ExamHelper** to cheat (e.g., on platforms like CodeTantra), bypass security, or violate policies is strictly prohibited and may lead to serious consequences, including academic or legal penalties. Use at your own risk.

## **Features**

- **Seamless Overlay:** Operates over any application without interference.
- **Flexible Input:** Type questions or drag-and-drop text/files for answers.
- **Toggle Visibility:** Press F10 to hide/unhide the dialog box.
- **Lightweight:** Minimal system resource usage for smooth performance.
- **Windows Support:** Distributed as a standalone `.exe` for easy use.

## **Installation**

### **Download the Executable:**

1. Navigate to the [Releases page](https://github.com/AnkitSharmaDev/ExamHelper/releases).
2. Download the latest `ExamHelper.exe` file.

### **Run the Application:**

1. Double-click `ExamHelper.exe` to launch.
2. No additional setup is required.
   - **Note:** Windows Defender or antivirus software may flag the `.exe` as it’s unsigned. You may need to allow it manually. Only download from trusted sources.

## **Usage**

### **Start the Application:**

- Launch `ExamHelper.exe`. The overlay dialog box will appear.

### **Input Questions:**

- **Type:** Click the dialog box and type your question.
- **Drag-and-Drop:** Drag text or files with questions into the box.

### **View Answers:**

- Answers are displayed instantly within the overlay.

### **Toggle Visibility:**

- Press F10 to hide or show the overlay. When hidden, it’s undetectable.

### **Exit:**

- Right-click the system tray icon (if implemented) and select "Exit," or use Task Manager to close.

## **Ethical Use Guidelines**

### **Permitted Uses:**

- **Productivity:** Quick research, note-taking, or reference lookup.
- **Accessibility:** Assisting users with disabilities in accessing information.

### **Prohibited Uses:**

- **Cheating:** Cheating on exams, assignments, or platforms like CodeTantra.
- **Bypassing Security:** Bypassing security measures or violating terms of service.
- **Unethical Activities:** Any unethical or illegal activities.

**Responsibility:** Misuse may result in academic penalties, account bans, or legal consequences. You are solely responsible for your actions.

## **Building from Source**

To build **ExamHelper** yourself:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AnkitSharmaDev/ExamHelper.git
   ```
2. **Open the ExamHelper.py file**:

Navigate to the directory where you cloned the repo and open ExamHelper.py in your preferred editor.

You can modify the transparency level, appearance, or any other functionality by adjusting the code as needed.

3. **Modify the Application**:

Change the app name or customize any settings according to your preferences in the ExamHelper.py file.

For more transparency or visual changes, you can adjust the settings within the script.

4. **Create the Executable**:

Once you're happy with the changes, use PyInstaller to create an .exe file:

bash
Copy
Edit
pyinstaller --onefile --windowed ExamHelper.py
This will generate an ExamHelper.exe file inside the dist/ directory.

5. **Enjoy: You now have a customized version of ExamHelper!**

## **Contributing**
Fork the repository: Feel free to fork this repository to make your own modifications.

**Star this repository: If you find the tool useful, please give it a star ⭐**.

Create a Pull Request: If you have any improvements or fixes, create a pull request, and we will review it.

Collaborate: If you want to collaborate on this project, open an issue to discuss new features or improvements.
   
