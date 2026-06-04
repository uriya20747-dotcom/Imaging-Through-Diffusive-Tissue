import os
import numpy as np
from PIL import Image

"""
Method to Rename Images to Legal Names, Resize to 600x600, and Convert to 1bpp
Inputs:
Path to 24bpp images
List of 24bpp images
Directory to save the processed images
Outputs:
Images converted to 1bpp, resized to 600x600, and saved in .bmp format
"""
def change_name(path, photo_files, bmp_path):
    # Create bmp_path directory if it doesn't exist
    os.makedirs(bmp_path, exist_ok=True)

    for i, photo_file in enumerate(photo_files):
        old_name = os.path.basename(photo_file)
        old_path = os.path.join(path, old_name)
        img = Image.open(old_path)
        img = img.resize((600, 600)) #Resized to 600x600
        img_bw = img.convert(mode='1') # Images converted to 1bpp

        # Save the image as BMP format
        new_img = f"I{i}"
        new_path = os.path.join(bmp_path, new_img)

        img_bw.save(new_path + ".bmp") #Saved in .bmp format
        print(f"Converted '{old_name}' to '{new_img}.bmp'.")

if __name__ == "__main__":


    # for mnist picture work
    path = r"C:\Users\ilaig\PycharmProjects\mnist_convert\mnist_converted" 
    bmp_path = os.path.join(os.getcwd(), 'mnist_converted_1bpp_bmp' )    #'shapes_bpp1')
    # List to store the file names of photos
    photo_files = []

    # Iterate over files in the directory
    for filename in sorted(os.listdir(path)):
        # Check if the file is a photo (ends with .jpg) and starts with a digit
        if filename.lower().endswith('.jpg') and filename.split('.')[0].isdigit():
            photo_files.append(filename)

    # Sort filenames by their numeric value
    sorted_filenames = sorted(photo_files, key=lambda x: int(x.split('.')[0]))
    print(sorted_filenames)
    change_name(path, sorted_filenames, bmp_path)
