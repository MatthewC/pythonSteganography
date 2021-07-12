# pythonSteganography

## Project Outline

Using python, implement a method to hide data within images. Should allow for you to select an image via the filedialog method.

## Steps to work on:
- [x] Deal with importing image from file directory.
- [ ] (Optional) Allow for 'encrypting' data with passkey.
- [ ] Implement steganography algorithm
- [ ] Output image to a GUI, and/or export the image to the same directory.

## Notes on steganography
There are different ways to implement steganography, but the most common one seems to be LSB (Least Significant Bit).
LSB works by looking at each byte, and changing the last bit. We change the last bit as it is the one which when changed 
doesn't produce a change that is too noticable. It is important to note that depending on the image size, there is a max number of bytes we can store within the image. 