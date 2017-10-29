# Text-to-image

This program uses python and python pillow. The program takes user input from console and outputs to console as well.

INSTRUCTIONS

This program requires python and python pillow
Python pillow: https://python-pillow.org/

To execute encoding:.
python steg.py -e [message] -i [image] -o [output]

message: The message you want to embed
image: The path to the image you want to embed the message into
output: The path you want to output your embedded message 

WARNING! Make sure your image is big enough to encode the message into.

(Image_pixel_height * Image_pixel_width * 3) - 33 >= message_length * byte_size(8)

To execute Decoding:

python steg.py -d [image]

image: path to image you want to decode
