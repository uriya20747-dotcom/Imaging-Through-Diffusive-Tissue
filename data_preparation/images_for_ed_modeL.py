import os
from PIL import Image

# Specify the directory containing the images
input_dir = r'C:\project final\crop_images\pythonProject\Images_exp\crop_encoder_decoder'
output_dir = os.path.join(os.getcwd(),'blur')

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get the list of image files and sort them if needed
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg'))]

# Loop through all files in the input directory
for filename in image_files:
    # Open an image file
    img_path = os.path.join(input_dir, filename)
    img = Image.open(img_path)

    # Convert image to grayscale (Mode L)
    grayscale_img = img.convert("L")

    # Resize the image to 200x200
    resized_img = grayscale_img.resize((200, 200))

    # Save the resized grayscale image
    resized_img.save(os.path.join(output_dir, filename))

print("Conversion completed.")
