import os
from PIL import Image

# Define source and destination directories
source_dir = r"C:\project final\crop_images\pythonProject\Images_exp\encoder_decoder_images"
dest_dir = r"C:\project final\crop_images\pythonProject\Images_exp\crop_encoder_decoder"

# Desired crop and resize size
crop_width, crop_height = 944, 850
resize_width, resize_height = 600, 600

# Ensure the destination directory exists
os.makedirs(dest_dir, exist_ok=True)

# Iterate over all files in the source directory
for filename in os.listdir(source_dir):
    if filename.lower().endswith(".png"):  # Filter for PNG files
        source_path = os.path.join(source_dir, filename)

        # Change the file extension to .jpg
        dest_filename = os.path.splitext(filename)[0] + ".jpg"
        dest_path = os.path.join(dest_dir, dest_filename)

        # Open the image
        with Image.open(source_path) as img:
            # Get the dimensions of the image
            img_width, img_height = img.size

            # Calculate the coordinates to center the crop box
            left = (img_width - crop_width) // 2
            top = (img_height - crop_height) // 2
            right = left + crop_width
            bottom = top + crop_height

            # Ensure the crop box is within image bounds
            left = max(left, 0)
            top = max(top, 0)
            right = min(right, img_width)
            bottom = min(bottom, img_height)

            # Crop the image
            crop_box = (left, top, right, bottom)
            cropped_img = img.crop(crop_box)

            # Resize the cropped image to 600x600
            resized_img = cropped_img.resize((resize_width, resize_height), Image.LANCZOS)

            # Save the cropped and resized image to the destination directory as JPG
            resized_img = resized_img.convert("RGB")  # Convert to RGB to ensure JPG format compatibility
            resized_img.save(dest_path, format="JPEG")

print("Cropping to 944x850 and resizing to 600x600, then saving as JPG completed.")
