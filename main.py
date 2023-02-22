import sys 
from PIL import Image
from argparse import ArgumentParser
from Img2zpl import Img2zpl

__VERSION__ = '0.0.4'

def main(argv):

    # Parse input arguments
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Path of the image file')
    parser.add_argument('-o', '--output', help="Path of the result file, default stdout", default="stdout")
    parser.add_argument('-w', '--width', help="Width of the zpl image", type=int)
    parser.add_argument('--zpl', help="Version of ZPL, default 2", type=int, default=2)
    parser.add_argument('-v', '--version', help="Show the version", action="version", version='%(prog)s {version}'.format(version=__VERSION__))

    args = parser.parse_args()

    # Open the file and clears it if the output need to save in a file
    if args.output != 'stdout':
        output = open(args.output, "w")
        output.truncate(0)

    # Open the image
    image = Image.open(args.input).convert('RGBA')

    # Get image size
    width,height = image.size

    resizedWidth = args.width
    if resizedWidth == None:
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

    # Get the ZPL code
    img2zpl = Img2zpl(args.zpl)
    zpl = img2zpl.toZPL(image, True)

    if args.output != 'stdout':
        # Write the output file
        output.write(zpl)

        # Close the file
        output.close()
    else:
        print(zpl)


if __name__ == '__main__':
    main(sys.argv[1:])
