from PIL import Image
import re
import math
import getopt, sys

__VERSION__='0.0.3'

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
        opts, args = getopt.getopt(argv, 'i:o:vhw:', ['input=', 'output=', 'version', 'help', 'width='])
    except(getopt.GetoptError, e):
        usage()
        sys.exit(2)

    imgPath = ''
    zplPath = ''
    resizedWidth = 0
    for opt, arg in opts:
        if opt in ('--input', '-i'):
            imgPath = arg
        elif opt in ('--output', '-o'):
            zplPath = arg
        elif opt in ('--version', '-v'):
            print(VERSION)
            sys.exit(2)
        elif opt in ('--width', '-w'):
            if arg.isnumeric():
                resizedWidth = int(arg)
            else:
                usage()
                sys.exit(2)
        else:
            usage()
            sys.exit(2)

    if imgPath == '':
        usage()
        sys.exit(2)

    # Open the file and clears it if the output need to save in a file
    if zplPath != '':
        output = open(zplPath, "w")
        output.truncate(0)

    # Open the image
    image = Image.open(imgPath).convert('RGBA')

    # Get image size
    width,height = image.size

    if resizedWidth == 0:
        resizedWidth = width

    # Make sure the width is a mutiple of 8
    if resizedWidth % 8 != 0:
        resizedWidth += (8 - (resizedWidth % 8))

    # Resize the image if needed
    if width != resizedWidth:
        wpercent = (resizedWidth/float(width))
        hsize = int((float(height)) * float(wpercent))
        image = image.resize((resizedWidth, hsize), Image.Resampling.LANCZOS)
        width, height = image.size

    # The image should be under 2000x2000
    if width > 2000 or height > 2000:
        raise Exception('Image too big (max: 2000, 2000): ' + width + ',' + height)

    # Convert to RGB
    temp = image
    image = Image.new('RGB', (width, height), 'white')
    image.paste(temp, mask=temp.split()[3])

    # Convert to grayscale
    image.convert('L')

    # Get the ZPL code
    zpl = img2zplAscii(image, width, height)

    if zplPath != '':
        # Write the output file
        output.write('^GF')
        output.write(zpl)

        # Close the file
        output.close()
    else:
        print('^GF' + zpl)


if __name__ == '__main__':
    main(sys.argv[1:])
