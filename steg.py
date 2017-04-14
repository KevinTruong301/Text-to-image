from __future__ import print_function
from PIL import Image
import binascii
import sys

#turn ASCII text to binary
def text2bin(text):
    binary = ''.join(format(ord(x), 'b').zfill(8) for x in text)
    return binary

#turn binary to ASCII text
def bin2text(bin):
    a = int(bin, 2)
    hex_string = '%x' % a
    n = len(hex_string)
    z = binascii.unhexlify(hex_string.zfill(n + (n & 1)))
    text=z.decode('ascii')
    return text

#Binary to integer
def bin2int(bin):
    return int(bin,2)

#Ingeger to binary but also fills in 0 till the length of the binary is 32
def int2bin(integer):
        bin = "{0:b}".format(integer)
        while(len(bin) < 32):
            bin = '0' + bin
        return bin

#DECODE
#d flag will trigger decode
if sys.argv[1] == '-d':
    #if there are less then 3 arguments or flags program will assume it is missing
    if len(sys.argv) < 3:
        print("Missing argument or flag")
        sys.exit()
    
    #Open image and save to object
    im = Image.open(sys.argv[2])
    #load pixel data to px
    px = im.load()

    #getting the width and hieght in pixels
    im_w, im_h = im.size


    #Decode the text length. First 11 pixles from the bottom right
    #Text length will be stored into three sets of 8 bits (32bits)
    text_len = ''
    count = 0
    for j in range(im_h - 1, 0, -1):
        for i in range(im_w-1,0,-1):
            #Get RGB at specified pixel
            R,G,B = px[i,j]

            #RED
            #turn R value to binary
            bin_R = text2bin(str(R))
            #Get the least significant value
            text_len = text_len + bin_R[len(bin_R)-1:]
            count +=1

            #GREEN
            bin_G = text2bin(str(G))
            text_len = text_len + bin_G[len(bin_G)-1:]
            count +=1
            #Will always stop at B because the text length will only be 32 bits long
            if count == 32 :
                break

            #BLUE
            bin_B = text2bin(str(B))
            text_len = text_len + bin_B[len(bin_B)-1:]
            count +=1
        #break outer loop
        if count == 32:
            break
    
    #Turn binary text_len into integer text_len
    text_len = bin2int(text_len)

    #Decode the hidden message
    count = 0
    #skip_count to skip the first 33 bits
    skip_count = 0
    hidden_msg =''
    for j in range(im_h -1, 0, -1):
        for i in range(im_w - 1, 0, -1):
            #get RGB at specified pixel
            R,G,B = px[i,j]

            #if count isn't = text length and is not one of the 1st 33 bits
            if count != text_len and skip_count >= 33:
                bin_R = text2bin(str(R))
                #get least significant digit
                hidden_msg = hidden_msg + bin_R[len(bin_R)-1:]
                count+=1
            skip_count += 1

            if count != text_len and skip_count >= 33:
                bin_G = text2bin(str(G))
                hidden_msg = hidden_msg + bin_G[len(bin_G)-1:]
                count+=1
            skip_count += 1

            if count != text_len and skip_count >= 33:
                bin_B = text2bin(str(B))
                hidden_msg = hidden_msg + bin_B[len(bin_B)-1:]
                count+=1
            skip_count += 1
            
            #this works because when count is equal to text_len count will not update
            if count == text_len:
                break
        if count == text_len:
            break

    #turn binary hidden_msg into ASCII text
    hidden_msg = bin2text(hidden_msg)

    #Output the message
    print(hidden_msg)
#ENCODE
#-e flag will trigger encode
elif sys.argv[1] == '-e':

    #if number of arguments is less than 7 then program will assume flag or argument is missing 
    if len(sys.argv) < 7:
        print("Missing argument or flag")
        sys.exit()
    #load image into object
    im = Image.open(sys.argv[4])
    #load message into variable msg
    msg = sys.argv[2]
    #load pixel data into variable px
    px = im.load()
    #load image width and height
    im_w, im_h = im.size
    #turn msg into binary
    msg_bin = text2bin(msg)
    #get number of binary values in msg
    msg_len = len(msg_bin)
    #turn the number of binary values in msg into binary for encoding
    msg_len_bin = int2bin(msg_len)
    
    #calculate maximum # of bits the image can handle(RGB)
    max_px = (im_w * im_h)* 3

    #if image is to small warn and exit
    if max_px < 33:
        print("Image length will not fit in Image")
        sys.exit()
    if max_px - 33 <= msg_len:
        print("Supplied data will not fit image")
        sys.exit()
    


    #Encode image length
    count = 0
    for j in range(im_h-1, 0, -1):
        for i in range(im_w-1,0,-1):
            #get RGB at specified pixel
            R,G,B = px[i,im_h-1]
            
            
            bin_R = text2bin(str(R))
            #remove original least sig bit and append the message length bit 
            bin_R = bin_R[:len(bin_R)-1] + msg_len_bin[count]
            R = bin2text(bin_R)
            count +=1

            bin_G = text2bin(str(G))
            bin_G = bin_G[:len(bin_G)-1] + msg_len_bin[count]
            G = bin2text(bin_G)     
            count+=1

            if count != 32:
                bin_B = text2bin(str(B))
                bin_B = bin_B[:len(bin_B)-1] + msg_len_bin[count]
                B = bin2text(bin_B)    
                count+=1
            #load new RGB
            px[i,j] = (int(R),int(G),int(B))
            if count == 32:
                break
        if count == 32: 
            break
    

    count = 0
    #skip_count to skip 1st 3 bits
    skip_count = 0
    for j in range(im_h -1, 0, -1):
        for i in range(im_w - 1, 0, -1):
            #load RGB from specified Pixel
            R,G,B = px[i,j]

            #if count isn't = text length and is not one of the 1st 33 bits
            if count != msg_len and skip_count >= 33:
                bin_R = text2bin(str(R))
                #replace least sig bit
                bin_R = bin_R[:len(bin_R)-1] + msg_bin[count]
                #load R number into R
                R = bin2text(bin_R)
                count +=1
            skip_count += 1

            if count != msg_len and skip_count >= 33:
                bin_G = text2bin(str(G))
                bin_G = bin_G[:len(bin_G)-1] + msg_bin[count]
                G = bin2text(bin_G)  
                count+=1
            skip_count += 1

            if count != msg_len and skip_count >= 33:
                bin_B = text2bin(str(B))
                bin_B = bin_B[:len(bin_B)-1] + msg_bin[count]
                B = bin2text(bin_B)   
                count+=1
            skip_count += 1

            #load in new RGB into pixel
            px[i,j] = (int(R),int(G),int(B))
            if count == msg_len:
                break
        if count == msg_len:
            break


    im.save(sys.argv[6])
else:
    #if 1st flag is wrong
    print("-d for decrypt")
    print("-e for encrypt")