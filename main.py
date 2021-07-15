import tkinter as tk
from tkinter import filedialog
from PIL import Image

#Define class I'll use to store methods related to the steganography
#TODO: Flesh out encryption methods.
class imageSteg:
    #Define variables that should be shared between each method.
    def __init__(self, image, height, width):
        self.image = image
        self.height = height
        self.width = width
        self.binary = ""
        self.seperator = "|||"

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
                #Make sure byte is 8-bits lone :)
                binArray.append(format(x, 'b').zfill(8))
            return ''.join(binArray)

    def toText(self, binary):
        #Convert binary into a base-2 integer
        binary = int(binary, 2)
        return chr(binary)


    def encryptData(self, message, password):
        pass

    def decryptData(self, message, password):
        pass

    def implantData(self, message):
        print("[LOG] Reading image...")
        #Load image
        img = self.image.load()

        #To know when we reach the end of the message, we need a placeholder at the end.
        message += self.seperator

        #Convert message to binary
        self.binary = self.toBinary(message)

        #We need to two variables to store the progress of how much of the message we've gone through
        currentPos = 0
        endPos = len(self.binary)

        print("[LOG] Looping through pixels...")
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

                #Because it is a tuple, we cannot directly edit it. Instead, we create a temporary array.
                tempArray = []

                r, g, b = self.toBinary(img[pixel, pixels], True)

                #Modify RED binary.
                if endPos > currentPos:
                    #In the code below, we replace the last bit of the byte, and add the first bit of our data. 
                    #The '2' is used to denote the fact we want it in Base-2 (Binary)
                    tempArray.append(int(r[:-1] + self.binary[currentPos], 2))
                    currentPos += 1
                else:
                    tempArray.append(img[pixel, pixels][0])
                
                #Modify GREEN binary.
                if endPos > currentPos:
                    tempArray.append(int(g[:-1] + self.binary[currentPos], 2))
                    currentPos += 1
                else:
                    tempArray.append(img[pixel, pixels][1])

                #Modify BLUE binary.
                if endPos > currentPos:
                    tempArray.append(int(b[:-1] + self.binary[currentPos], 2))
                    currentPos += 1
                else:
                    tempArray.append(img[pixel, pixels][2])

                #With the array full, we turn it's values into a tuple and replace the RGB pixels in the original image.
                img[pixel, pixels] = (tempArray[0], tempArray[1], tempArray[2])

                #Base case (We finished going through our message)
                if endPos < currentPos:
                    break
        print("[LOG] Message implanted successfully.")
        return img

    def extractData(self):
        img = self.image.load()
        message = ""

        #Variable we'll use to store the last bits. 
        dataExtract = ""

        #Do the same loop we did to hide the data, as we need to get every 'least-significant bit' from the image.
        for pixels in range(self.height):
            for pixel in range(self.width):
                r, g, b = self.toBinary(img[pixel, pixels], True)

                dataExtract += r[-1:]
                dataExtract += g[-1:]
                dataExtract += b[-1:]

        #With all the binary values in a single variable, we can loop through them an convert them into bytes.
        byteExtract = []
        currentByte = ""

        for bit in dataExtract:
            if len(currentByte) <= 7:
                currentByte += bit
            else:
                byteExtract.append(currentByte)
                currentByte = bit

        #Now with each byte, we covert it back to ASCII and append it to our message variable.
        for byte in byteExtract:
            message += self.toText(byte)

            #Check if we've reached the end of the message.
            if message[-3:] == self.seperator:
                print("[LOG] End of message reached.")
                break
        
        #Return message whilst removing the seperator placeholder from the end. 
        return message[:-(len(self.seperator))]

userChoice = ""



while not userChoice == ".exit":
    #Ask user whether he wants to encode a message, or a decode a message. 
    userChoice = input('Type 1 to encode an image | Type 2 to decode an image | Type .exit to leave: ')

    #Make sure program actually exits.
    if not (userChoice == "1" or userChoice == "2"):
        continue

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

    #Use try/except to catch any file inputs which aren't an image, or if no file was selected at all.
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

                print("[LOG] Saving image...")

                img.save('encoded.png')

                print("[DONE] Image saved.")
            else:
                print("[ERR] Message is too long, or empty")
        elif userChoice == "2":
            messageExtract = image.extractData()
            
            print(f'[DONE] Message extracted: {messageExtract}')
    except IOError:
        print("[ERR] Not a valid image.")
    except AttributeError:
        print('[ERR] No file selected.')
