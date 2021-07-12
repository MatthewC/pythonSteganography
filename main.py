import tkinter as tk
from tkinter import filedialog
from PIL import Image

#Handle opening an image, and passing it to PIL
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select an image.",
    filetypes=(
        ('All files', '*.*'),
        ('PNG', '*.png'),
        ('JPGs', '*.jpg *.jpeg')
    )
)

print(f'[LOG] Opening file: {file_path}')