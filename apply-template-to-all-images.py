#!/usr/bin/env python

#
# place-all-images-from-dir-into-database.py
#
# Exports a directory full of font awesome icons into database.
#
# Copyright (c) 2014-2014 Andrew Allbright (http://andrewallbright.com)
#
#  - http://andrewallbright.com
#

import sys, argparse, re, glob, os
from PIL import Image

# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def uchr(x):
        return unichr(x)
else:
    def u(x):
        return x

    def uchr(x):
        return chr(x)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description="Puts in all font awesome icons PNGs into database")

    parser.add_argument("--directory", type=str, default="images",
            help="read this directory (default directory)")
    parser.add_argument("--template", type=str, default="marker_images",
            help="read this directory (default directory)")



    args      = parser.parse_args()
    directory = args.directory

    # Create list of objects with filename and file size
    print(os.getcwd())
    # os.chdir("marker_templates")
    print(os.getcwd())
    small_template_loc  = "32_blue_template.png"
    medium_template_loc = "48_blue_template.png"
    large_template_loc  = "64_blue_template.png"
    small_template  = Image.open("32_blue_template_outline.png")
    medium_template = Image.open("48_blue_template_outline.png")
    large_template  = Image.open("64_blue_template_outline.png")
    print "The size of the Image is: "
    print(small_template.format, small_template.size, small_template.mode)
    file_list    = []
    small_files  = []
    medium_files = []
    large_files  = []
    os.chdir(directory)
    for file in glob.glob("*.png"):
        file_list.append(file)
        filesize, color, filename = file.split("_")
        filename = filename.replace('.png', '')
        image    = Image.open(file).convert('RGBA')
        print(image)
        print("Filesize: %s" % filesize)
        if filesize == "32":
            small_template_cp = small_template.copy().convert('RGBA')
            small_template_cp.paste(image, (9, 9), image)
            small_template_cp.save("tmp_" + "_".join([filesize, color, filename]) + ".png")
            small_files.append(file)
        elif filesize == "48":
            medium_template_cp = medium_template.copy().convert('RGBA')
            medium_template_cp.paste(image, (13, 13), image)
            medium_template_cp.save("tmp_" + "_".join([filesize, color, filename]) + ".png")
            medium_files.append(file)
        elif filesize == "64":
            large_template_cp = large_template.copy().convert('RGBA')
            large_template_cp.paste(image, (16, 16), image)
            large_template_cp.save("tmp_" + "_".join([filesize, color, filename]) + ".png")
            large_files.append(file)
        image.close()

    count = 0
    for data_structure in file_list:
        count += 1

    print("\n\n There are %s images in %s directory" % (count, directory))

    print("\n\nScript Complete!")    
