import tkinter as tk
from gui import MedicalChatbotGUI

def main():
    root = tk.Tk()
    app = MedicalChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()