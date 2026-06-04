import os
from PIL import Image
import re

# Specify the directories
source_dir = r'C:\project final\crop_images\pythonProject\Images_exp\mnist_converted_1bpp_bmp'
dest_dir = os.path.join(os.getcwd(), 'org')

# Ensure the destination directory exists
os.makedirs(dest_dir, exist_ok=True)

# Function to extract numerical parts of filenames for custom sorting
def custom_sort_key(filename):
    number_part = re.search(r'\d+', filename).group()  # Find the numerical part of the filename
    return int(number_part)  # Sort by numerical value only

# Get the list of image files, ensuring they are BMP files
image_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.bmp')]
print("Unsorted files sample:", image_files[:10])


sorted_files=image_files
# Determine the number of digits to use for zero padding based on the total number of files
max_index = len(sorted_files) - 1
padding_length = len(str(max_index))

# Loop through all files in the sorted list
for index, filename in enumerate(sorted_files):
    img_path = os.path.join(source_dir, filename)
    img = Image.open(img_path)
    grayscale_img = img.convert("L")
    resized_img = grayscale_img.resize((200, 200))

    # Create a new filename with IMG_ prefix and zero-padded index
    formatted_index = str(index).zfill(padding_length)
    new_filename = f'IMG_{formatted_index}.jpg'
    dest_path = os.path.join(dest_dir, new_filename)

    # Save the image
    resized_img.save(dest_path, format='JPEG')

print("Custom sorting, conversion, and saving of images completed.")
# Check the first few saved images
image_files = [f for f in os.listdir(dest_dir) if f.lower().endswith('.jpg')]
print("First few saved images:", image_files[:10])


for index, filename in enumerate(image_files):
    new_file_name=f"IMG_{index}.jpg"
    os.rename(os.path.join(dest_dir,filename), os.path.join(dest_dir,new_file_name))

image_files = [f for f in os.listdir(dest_dir) if f.lower().endswith('.jpg')]
print("First few saved images:", image_files[:10])
