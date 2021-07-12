import tkinter as tk
from tkinter import filedialog
from PIL import Image

#Define class I'll use to store methods related to the steganography
#TODO: Flesh out each of the methods.
class imageSteg:
    def __init__(self):
        pass

    #For the text to be inserted into the image, we first need to convert it to binary. 
    def toBinary(self, message):
        textArray = bytearray(message, 'utf-8')
        binArray = []
        for x in textArray:
            binArray.append(format(x, 'b'))
        return ''.join(binArray)

    def encryptData(self, message, password):
        pass

    def decryptData(self, message, password):
        pass

    def implantData(self, message):
        pass

    def extractData(self, message):
        pass


#Handle opening an image, and passing it to PIL
root = tk.Tk()
root.withdraw()

#filedialog deals with opening "Pick a file" window, whilst allowing for the restriction of file extensions.
file_path = filedialog.askopenfilename(
    title="Select an image.",
    filetypes=(
        ('All files', '*.*'),
        ('PNG', '*.png'),
        ('JPGs', '*.jpg *.jpeg')
    )
)

print(f'[LOG] Opening file: {file_path}')

#Use try/except to catch any file inputs which aren't an image.
try:
    img = Image.open(file_path)
    print("[LOG] Image opened.")

    #Calculate the numer of bytes in the image, so that we know how many last bits we can change.
    #This is done by: number of pixels * 3 (cause of RGB) / 8 (cause in one byte, we only have ONE bit we can change.)
    #If the message is bigger than the number of last bits in the image, we won't be able to store the entire message.
    height, width = img.size
    maxBytes = height * width * 3 / 8
    maxBytes = round(maxBytes)

    print(f'Total bytes available: {maxBytes}')

    userInput = input("Enter text to be hidden: ")

    #TODO: Implement encryption (if possible)

    if len(userInput) > 0 and len(userInput) < maxBytes:
        #Handle putting data into image
        pass
    else:
        print("[ERR] Message is too long, or empty")
except IOError:
    print("[ERR] Not a valid image.")