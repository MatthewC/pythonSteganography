import tkinter as tk
from tkinter import filedialog
from PIL import Image

#Define class I'll use to store methods related to the steganography
#TODO: Flesh out each of the methods.
class imageSteg:
    #Define variables that should be shared between each method.
    def __init__(self, image, height, width):
        self.image = image
        self.height = height
        self.width = width
        self.binary = ""

    #For the text to be inserted into the image, we first need to convert it to binary. 
    def toBinary(self, message, isPixel = False):
        if isPixel:
            binArray = []
            for pix in message:
                #Use bin to convert number into binary, whilst using [2:] to get rid of the "0b" Python puts in.
                binary = bin(pix)[2:]
                #Use zfill to make sure it is 8 integers long.
                binArray.append(binary.zfill(8))
            return binArray
        else:
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
        #Load image
        img = self.image.load()

        #Convert message to binary
        self.binary = self.toBinary(message)

        #We need to two variables to store the progress of how much of the message we've gone through
        currentPos = 0
        endPos = len(self.binary)

        for pixels in range(self.height):
            for pixel in range(self.width):
                """
                PIL allows for image manipulation. By using the height and width in the two for loops, 
                we can access each pixel individual. PIL stores each pixel as a tuple, with three values,
                one for each of the RGB colors.

                pixel[0] would be red
                pixel[1] would be green
                pixel[2] would be blue
                """

                r, g, b = self.toBinary(img[pixel, pixels], True)

                #Modify RED binary.
                if endPos > currentPos:
                    #In the code below, we get the last bit of the byte, and add the first bit of our data. 
                    #The '2' is used to denote the fact we want it in Base-2 (Binary)
                    img[pixel, pixels] = int(r[:-1] + self.binary[currentPos], 2)
                    currentPos += 1
                
                #Modify GREEN binary.
                if endPos > currentPos:
                    img[pixel, pixels] = int(g[:-1] + self.binary[currentPos], 2)
                    currentPos += 1

                #Modify BLUE binary.
                if endPos > currentPos:
                    img[pixel, pixels] = int(b[:-1] + self.binary[currentPos], 2)
                    currentPos += 1

                #Base case (We finished going through our message)
                if endPos < currentPos:
                    break
        return img

    def extractData(self, message):
        pass

userChoice = ""

while not userChoice == ".exit":
    #Ask user whether he wants to encode a message, or a decode a message. 
    userChoice = input('Type 1 to encode an image | Type 2 to decode an image | Type .exit to leave: ')

    while not (userChoice == "1" or userChoice == "2"):
        userChoice = input('Not a valid choice, try again: ')

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

        #Get image dimensions. 
        height, width = img.size
        
        #Pass image to class.
        image = imageSteg(img, height, width)

        if userChoice == "1":
            #Calculate the numer of bytes in the image, so that we know how many last bits we can change.
            #This is done by: number of pixels * 3 (cause of RGB) / 8 (cause in one byte, we only have ONE bit we can change.)
            #If the message is bigger than the number of last bits in the image, we won't be able to store the entire message.
            maxBytes = height * width * 3 / 8
            maxBytes = round(maxBytes)

            print(f'[MSG] Total bytes available: {maxBytes}')

            userInput = input("Enter text to be hidden: ")

            #TODO: Implement encryption (if possible)

            if len(userInput) > 0 and len(userInput) < maxBytes:
                image.implantData(userInput)
                pass
            else:
                print("[ERR] Message is too long, or empty")
    except IOError:
        print("[ERR] Not a valid image.")
