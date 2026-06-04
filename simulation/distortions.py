import cv2
import os
import numpy as np

"""
Input: image
Output: image with strong blur
"""
def gaussian_m (image):


    blurred_img=image
    for i in range(25):
        # Increase sigma for stronger blurring
        sigma_x = 10+2*i
        #Use in GaussianBlur
        blurred_img = cv2.GaussianBlur(blurred_img, (15,15), sigma_x, cv2.BORDER_TRANSPARENT)
        #use also in blur
        blurred_img=cv2.blur(blurred_img,(11,11))
    return blurred_img

# The method classifier the images to blur and original to different dir.
def classifier_to_folders(images_array):

    current_path = os.getcwd()
    path_blur = os.path.join(current_path, "image_blur")
    path_org = os.path.join(current_path, "image_org")

    # Create directories if they don't exist
    os.makedirs(path_blur, exist_ok=True)
    os.makedirs(path_org, exist_ok=True)

    for index, image in enumerate(images_array):
        org_image = image.copy()
        blur_img = gaussian_m(org_image)

        # Name of image wth index (will help to identity connection between original to blur.
        #org_filename = f"org_image_{index}.jpg"
        #blur_filename = f"blur_image_{index}.jpg"
        org_filename = f"image_{index}.jpg"
        blur_filename = f"image_{index}.jpg"
        # Save the original and blurred images in their dir.
        cv2.imwrite(os.path.join(path_org, org_filename), org_image)
        cv2.imwrite(os.path.join(path_blur, blur_filename), blur_img)


