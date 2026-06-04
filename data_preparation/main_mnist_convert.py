import os
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2


def save_mnist_images_as_jpg(images, save_dir, re_size_img=(750, 600)):
    os.makedirs(save_dir, exist_ok=True)

    for i, img in enumerate(images):
        # Resize image using PIL
        img_pil = Image.fromarray(img)
        img_resized = img_pil.resize(re_size_img, Image.LANCZOS)

        # Convert to 8-bit grayscale image (mode 'L')
        img_gray = img_resized.convert('L')

        # Convert grayscale to binary image
        _, img_bw = cv2.threshold(np.array(img_gray), 127, 255, cv2.THRESH_BINARY)

        # Invert the binary image to have black digits on white background
        img_bw = cv2.bitwise_not(img_bw)

        # Convert binary image back to PIL image and ensure 24-bit depth
        img_bw_pil = Image.fromarray(cv2.cvtColor(img_bw, cv2.COLOR_GRAY2RGB))

        # Save the image as JPG format
        save_path = os.path.join(save_dir, f"{i}.jpg")
        cv2.imwrite(save_path, cv2.cvtColor(img_bw, cv2.COLOR_GRAY2RGB))
        # img_bw_pil.save(save_path, format='JPEG')
        print(f"Saved {save_path}")


if __name__ == "__main__":
    # Load MNIST dataset
    mnist = tf.keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    # Resize and save the first 2 training images as JPG in the desired format
    save_dir = os.path.join(os.getcwd(), 'mnist_converted')
    re_size_img = (600, 600)

    # Save the first 30000O images for demonstration
    save_mnist_images_as_jpg(train_images[:30000], save_dir, re_size_img)