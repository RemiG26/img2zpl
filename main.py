from PIL import Image
import math
import getopt, sys
from Img2zpl import Img2zpl

__VERSION__='0.0.3'

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

    # Get the ZPL code
    img2zpl = Img2zpl()
    zpl = img2zpl.convert(image)

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
