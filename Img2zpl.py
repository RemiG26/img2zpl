import re

class Img2zpl:

    def __init__(self, zpl_version = 2):
        self.zpl_version = zpl_version

    def convert(self, image):
        # Convert to grayscale
        image = image.convert('L')

        w,h = image.size

        # The width of the image must be multiple of 8
        if w % 8 != 0:
            raise Exception("Invalid width, not a multiple of 8: " + w)
        
        # Size in bytes of the image
        dataLength=f'{(w * h) / 8:01}'
        
        # Size in bytes of an image's row
        rowLength=f'{w / 8:01}'

        lastRow = ''
        out = ''

        for y in range(h):

            # Convert each image row to binary
            currentLine = ''
            for x in range(w):    
                grayscale = image.getpixel((x, y))
                if grayscale == 255:
                    currentLine += '0'
                else:
                    currentLine += '1'
            
            currentBytes = []
            for i in range(0, len(currentLine), 8):
                currentBytes.append(currentLine[i:i+8])

            # Add leading zeros to the last byte if < 8
            n = currentBytes.pop()
            currentBytes.append(f'{int(n):08}')

            # Convert the row in hexadecimal
            row = ''
            for b in currentBytes:
                row += format(int(b,2), '02x')

            out += self.compressRow(row, lastRow)
            lastRow = row

        return 'A,' + str(len(out.encode('utf-8'))) + ',' + str(dataLength) + ',' + str(rowLength) + ',' + out 
    
    
    def compressRow(self, current, last):
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

        if self.zpl_version == 2:
            return re.sub(r'(.)(\1{2,})', callback, outline)
        
        return outline
