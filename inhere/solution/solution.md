# build challenge

The challenge consists of an executable that shows some text.
The program has an image embedded which stores the font.
Extract the image to read the flag.

- make an image as a font file
- use `toData.py` to convert it to a C header
- `gcc version1.c -lraylib -o inhere`

# solution

- use reversing tool to examine executable
- there are some readable symbols
- the program loads an image as a texture
- image = obj.ImageData
- use a hexdump to extract obj.ImageData
- convert hex (which is RGB) to an image