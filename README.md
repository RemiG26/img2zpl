<h4 align="center">
  Img2Zpl
</h4>

<div align="center">
  <a href="https://github.com/RemiG26/gavinr/actions"><img src="https://github.com/RemiG26/gavinr/workflows/ci/badge.svg?branch=main&event=push"></a>
</div>

## Description

Img2Zpl is a tool to convert an image to a zpl code so it can be included on an label.

## Features

- [x] Support ZPL V1 and V2
- [x] Convert to grayscale
- [x] Support PNG with alpha
- [x] The image can be resized

## Requirements

- Ubuntu / macOS / Windows
- Python3
- [Pillow](https://pillow.readthedocs.io/en/stable/#)

## Usage

Run `img2zpl --help` for details.

```bash

# Convert an image to zpl and output the result in stdout
img2zpl -i original.png

# Convert an image to zpl and save the result in a file
img2zpl -i original.png -o output_zpl.txt

# Resize and then convert to zpl
img2zpl -i original.png -o output_zpl.txt -w 800

# Specify a ZPL version
img2zpl -i original.png --zpl 1

```
