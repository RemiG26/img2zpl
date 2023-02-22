from PIL import Image
import re
import math
import getopt, sys

VERSION='0.0.2'

# Start the conversion
def img2zplAscii(img, w, h):
    if w % 8 != 0:
        raise Exception("Invalid width, not a modulo of 8: " + w)
    lastRow = ''
    n = (w * h) / 8
    dataLength=f'{n:01}'
    n = w / 8
    rowLength=f'{n:01}'
    out = ''
    for y in range(h):
        currentLine = ''
        for x in range(w):    
            r, g, b = img.getpixel((x, y))
            if r == 0 and g == 0 and b == 0:
                currentLine += '1'
            else:
                currentLine += '0'
        
        currentBytes = []
        for i in range(0, len(currentLine), 8):
            currentBytes.append(currentLine[i:i+8])

        # Add leading zeros to the last byte in < 8
        n = currentBytes.pop()
        currentBytes.append(f'{int(n):08}')

        row = ''
        for b in currentBytes:
            row += format(int(b,2), '02x')

        out += compressZplAsciiLine(row, lastRow)
        # out += row
        lastRow = row

    return 'A,' + str(len(out.encode('utf-8'))) + ',' + str(dataLength) + ',' + str(rowLength) + ',' + out 

def compressZplAsciiLine(current, last):
    if current == last:
        return ':'
    
    outline = re.sub(r'0+$', ',', current)
    outline = re.sub(r'F+$', '!', outline)

    def callback(match):
        original = match.group(0)
        repeat = len(original)
        count = ""

        if repeat > 400:
            count += "z" * (repeat // 400)
            repeat %= 400

        if repeat > 19:
            count += chr(ord('f') + (repeat // 20))
            repeat %= 20

        if repeat > 0:
            count += chr(ord('F') + repeat)

        return count + original[1]

    outline = re.sub(r'(.)(\1{2,})', callback, outline)

    return outline

def usage():
    print("Usage:")
    print("\timg2zpl -i <img path> -o <zpl result path>\n")
    print("Options:\n")
    print("\t-h --help\tShow this screen")
    print("\t-v --version\tShow version")
    print("\t-i --input\tImage path to convert")
    print("\t-o --output\tFile containing the zpl")

def main(argv):

    try:
        opts, args = getopt.getopt(argv, 'i:o:vh', ['input=', 'output=', 'version', 'help'])
    except(getopt.GetoptError, e):
        print(e)
        usage()
        sys.exit(2)

    imgPath = ''
    zplPath = ''
    for opt, arg in opts:
        if opt in ('--input', '-i'):
            imgPath = arg
        elif opt in ('--output', '-o'):
            zplPath = arg
        elif opt in ('--version', '-v'):
            print(VERSION)
            sys.exit(2)
        else:
            usage()
            sys.exit(2)

    if imgPath == '' or zplPath == '':
        usage()
        sys.exit(2)

    # Open the file and clears it
    output = open(zplPath, "w")
    output.truncate(0)

    # Open the image
    image = Image.open(imgPath).convert('RGBA')

    # Get image size
    width,height = image.size

    # Resize the image to have a width multiple of 8
    mis = width % 8
    if mis != 0:
        width += (8 - mis)

    # The image should be under 2000x2000
    if width > 2000 or height > 2000:
        raise Exception('Image too big (max: 2000, 2000): ' + width + ',' + height)

    imgfinal=Image.new('RGB', (width, height), 'white')

    imgfinal.paste(image, mask=image.split()[3])

    imgfinal.save('foo.png')

    # Convert to grayscale
    imgfinal.convert('L')

    # Get the ZPL code
    zpl = img2zplAscii(imgfinal, width, height)

    # Write the output file
    output.write('^GF')
    output.write(zpl)

    # Close the file
    output.close()


if __name__ == '__main__':
    main(sys.argv[1:])
